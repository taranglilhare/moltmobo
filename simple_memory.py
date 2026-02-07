"""
Lightweight Memory Manager for Termux
Uses JSON instead of ChromaDB (no Rust compiler needed)
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path

from utils.logger import logger


class SimpleMemoryManager:
    """Simple JSON-based memory manager for Termux"""
    
    def __init__(self, data_dir: str = "./data/memory"):
        """
        Initialize simple memory manager
        
        Args:
            data_dir: Directory to store memory files
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.memory_file = self.data_dir / "interactions.json"
        self.memory = self._load_memory()
        
        logger.info("✓ Simple Memory Manager initialized (Termux compatible)")
    
    def _load_memory(self) -> List[Dict]:
        """Load memory from JSON file"""
        if self.memory_file.exists():
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Failed to load memory: {e}")
                return []
        return []
    
    def _save_memory(self):
        """Save memory to JSON file"""
        try:
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(self.memory, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Failed to save memory: {e}")
    
    def store_interaction(
        self,
        user_intent: str,
        observation: Dict,
        plan: Dict,
        success: bool
    ):
        """
        Store interaction in memory
        
        Args:
            user_intent: User's command
            observation: Screen observation
            plan: Action plan
            success: Whether execution succeeded
        """
        interaction = {
            'timestamp': datetime.now().isoformat(),
            'user_intent': user_intent,
            'current_app': observation.get('current_app', ''),
            'actions': [a.get('action') for a in plan.get('actions', [])],
            'success': success
        }
        
        self.memory.append(interaction)
        
        # Keep only last 100 interactions
        if len(self.memory) > 100:
            self.memory = self.memory[-100:]
        
        self._save_memory()
        logger.info(f"✓ Stored interaction: {user_intent[:50]}...")
    
    def get_recent_interactions(self, limit: int = 5) -> List[Dict]:
        """Get recent interactions"""
        return self.memory[-limit:]
    
    def search_by_intent(self, query: str, limit: int = 5) -> List[Dict]:
        """
        Search interactions by user intent
        
        Args:
            query: Search query
            limit: Max results
        
        Returns:
            List of matching interactions
        """
        query_lower = query.lower()
        results = []
        
        for interaction in reversed(self.memory):
            if query_lower in interaction['user_intent'].lower():
                results.append(interaction)
                if len(results) >= limit:
                    break
        
        return results
    
    def search_by_app(self, app_name: str, limit: int = 5) -> List[Dict]:
        """Search interactions by app name"""
        app_lower = app_name.lower()
        results = []
        
        for interaction in reversed(self.memory):
            if app_lower in interaction.get('current_app', '').lower():
                results.append(interaction)
                if len(results) >= limit:
                    break
        
        return results
    
    def get_context_for_llm(self, current_intent: str, limit: int = 3) -> str:
        """
        Get relevant context for LLM
        
        Args:
            current_intent: Current user intent
            limit: Number of past interactions to include
        
        Returns:
            Formatted context string
        """
        # Get recent interactions
        recent = self.get_recent_interactions(limit)
        
        if not recent:
            return "No previous interactions."
        
        context_parts = ["Recent interactions:"]
        
        for i, interaction in enumerate(recent, 1):
            timestamp = interaction['timestamp'][:19]  # Remove microseconds
            intent = interaction['user_intent']
            success = "✓" if interaction['success'] else "✗"
            
            context_parts.append(
                f"{i}. [{timestamp}] {success} {intent}"
            )
        
        return "\n".join(context_parts)
    
    def clear_memory(self):
        """Clear all memory"""
        self.memory = []
        self._save_memory()
        logger.info("Memory cleared")
    
    def get_stats(self) -> Dict:
        """Get memory statistics"""
        total = len(self.memory)
        successful = sum(1 for i in self.memory if i['success'])
        
        return {
            'total_interactions': total,
            'successful': successful,
            'failed': total - successful,
            'success_rate': f"{(successful/total*100):.1f}%" if total > 0 else "0%"
        }
