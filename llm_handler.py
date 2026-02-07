"""
LLM Handler - Manages interactions with LLMs
Supports both cloud (Claude) and local (Ollama) LLMs
"""

import os
from typing import Dict, List, Optional
from anthropic import Anthropic
import json

from privacy_firewall import PrivacyFirewall
from utils.logger import logger


class LLMHandler:
    """Handles LLM interactions with cloud and local fallback"""
    
    def __init__(self, config: Dict):
        """
        Initialize LLM handler
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.privacy_firewall = PrivacyFirewall(
            config.get('privacy', {}).get('sensitivity_level', 'high')
        )
        
        # Initialize Claude client
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if api_key:
            self.claude_client = Anthropic(api_key=api_key)
            logger.info("✓ Claude API initialized")
        else:
            self.claude_client = None
            logger.warning("⚠️  No Claude API key found")
        
        # Ollama config
        self.ollama_enabled = config.get('llm', {}).get('fallback', {}).get('enabled', False)
        self.ollama_endpoint = os.getenv('OLLAMA_ENDPOINT', 'http://localhost:11434')
        
        if self.ollama_enabled:
            logger.info(f"✓ Ollama fallback enabled: {self.ollama_endpoint}")
    
    def generate_action_plan(self, observation: Dict, user_intent: str) -> Dict:
        """
        Generate action plan based on observation and user intent
        
        Args:
            observation: Current screen observation
            user_intent: What the user wants to do
        
        Returns:
            Dict with 'actions' list and 'reasoning' string
        """
        try:
            # Determine which LLM to use
            use_local = self.privacy_firewall.should_use_local_llm(observation)
            
            if use_local and self.ollama_enabled:
                logger.info("🔒 Using local LLM for privacy")
                return self._generate_with_ollama(observation, user_intent)
            elif self.claude_client:
                logger.info("☁️  Using Claude API")
                # Sanitize data before sending to cloud
                sanitized_obs = self.privacy_firewall.sanitize_for_cloud(observation)
                return self._generate_with_claude(sanitized_obs, user_intent)
            else:
                logger.error("No LLM available")
                return {
                    'actions': [],
                    'reasoning': 'No LLM available',
                    'error': 'No LLM configured'
                }
        
        except Exception as e:
            logger.error(f"Action plan generation failed: {e}")
            return {
                'actions': [],
                'reasoning': f'Error: {e}',
                'error': str(e)
            }
    
    def _generate_with_claude(self, observation: Dict, user_intent: str) -> Dict:
        """Generate action plan using Claude"""
        # Build prompt
        prompt = self._build_prompt(observation, user_intent)
        
        try:
            # Call Claude API
            response = self.claude_client.messages.create(
                model=self.config.get('llm', {}).get('primary', {}).get('model', 'claude-3-5-sonnet-20241022'),
                max_tokens=self.config.get('llm', {}).get('primary', {}).get('max_tokens', 4096),
                temperature=self.config.get('llm', {}).get('primary', {}).get('temperature', 0.7),
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            # Parse response
            response_text = response.content[0].text
            logger.debug(f"Claude response: {response_text[:200]}...")
            
            return self._parse_llm_response(response_text)
        
        except Exception as e:
            logger.error(f"Claude API error: {e}")
            
            # Fallback to local if available
            if self.ollama_enabled:
                logger.info("Falling back to local LLM")
                return self._generate_with_ollama(observation, user_intent)
            
            return {
                'actions': [],
                'reasoning': f'Claude API error: {e}',
                'error': str(e)
            }
    
    def _generate_with_ollama(self, observation: Dict, user_intent: str) -> Dict:
        """Generate action plan using local Ollama"""
        import requests
        
        prompt = self._build_prompt(observation, user_intent)
        
        try:
            response = requests.post(
                f"{self.ollama_endpoint}/api/generate",
                json={
                    "model": self.config.get('llm', {}).get('fallback', {}).get('model', 'llama3.2'),
                    "prompt": prompt,
                    "stream": False
                },
                timeout=30
            )
            
            response.raise_for_status()
            response_text = response.json().get('response', '')
            
            logger.debug(f"Ollama response: {response_text[:200]}...")
            
            return self._parse_llm_response(response_text)
        
        except Exception as e:
            logger.error(f"Ollama error: {e}")
            return {
                'actions': [],
                'reasoning': f'Local LLM error: {e}',
                'error': str(e)
            }
    
    def _build_prompt(self, observation: Dict, user_intent: str) -> str:
        """Build prompt for LLM"""
        current_app = observation.get('current_app', 'Unknown')
        ui_context = observation.get('ui_context', 'No UI data')
        
        prompt = f"""You are an AI agent controlling an Android device. Your task is to help the user accomplish their goal.

Current State:
- App: {current_app}
- Screen Elements:
{ui_context}

User Intent: {user_intent}

Your task: Generate a sequence of actions to accomplish the user's intent.

Available Actions:
1. tap - Tap at coordinates: {{"type": "tap", "x": 100, "y": 200}}
2. swipe - Swipe gesture: {{"type": "swipe", "x1": 100, "y1": 200, "x2": 300, "y2": 400}}
3. input_text - Type text: {{"type": "input_text", "text": "hello"}}
4. press_key - Press key: {{"type": "press_key", "key": "BACK"}} (BACK, HOME, ENTER)
5. open_app - Open app: {{"type": "open_app", "package": "com.android.chrome"}}
6. scroll - Scroll screen: {{"type": "scroll", "direction": "down"}} (up/down)

Respond with a JSON object containing:
1. "reasoning": Brief explanation of your plan
2. "actions": Array of action objects to execute in sequence

Example response:
{{
  "reasoning": "Need to click the search button and type the query",
  "actions": [
    {{"type": "tap", "x": 540, "y": 100}},
    {{"type": "input_text", "text": "weather today"}},
    {{"type": "press_key", "key": "ENTER"}}
  ]
}}

Respond ONLY with valid JSON, no additional text.
"""
        
        return prompt
    
    def _parse_llm_response(self, response_text: str) -> Dict:
        """Parse LLM response into action plan"""
        try:
            # Try to extract JSON from response
            # Sometimes LLMs add extra text, so we need to find the JSON block
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx == -1 or end_idx == 0:
                raise ValueError("No JSON found in response")
            
            json_str = response_text[start_idx:end_idx]
            parsed = json.loads(json_str)
            
            # Validate structure
            if 'actions' not in parsed:
                parsed['actions'] = []
            if 'reasoning' not in parsed:
                parsed['reasoning'] = 'No reasoning provided'
            
            logger.info(f"Parsed {len(parsed['actions'])} actions")
            logger.debug(f"Reasoning: {parsed['reasoning']}")
            
            return parsed
        
        except Exception as e:
            logger.error(f"Failed to parse LLM response: {e}")
            logger.debug(f"Raw response: {response_text}")
            
            return {
                'actions': [],
                'reasoning': 'Failed to parse response',
                'error': str(e),
                'raw_response': response_text
            }
