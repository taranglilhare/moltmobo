"""
Memory Manager - Persistent Memory using Vector Database
Stores and retrieves conversation history and context
"""

from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
import json

try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False

from utils.logger import logger


class MemoryManager:
    """Manages persistent memory using ChromaDB"""
    
    def __init__(self, config: Dict):
        """
        Initialize memory manager
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        memory_config = config.get('memory', {})
        
        self.persist_directory = Path(memory_config.get('persist_directory', './data/memory'))
        self.collection_name = memory_config.get('collection_name', 'moltmobo_memory')
        self.max_history = memory_config.get('max_history', 100)
        
        # Create directory
        self.persist_directory.mkdir(parents=True, exist_ok=True)
        
        # Initialize ChromaDB
        if CHROMADB_AVAILABLE:
            try:
                self.client = chromadb.PersistentClient(
                    path=str(self.persist_directory)
                )
                
                # Get or create collection
                self.collection = self.client.get_or_create_collection(
                    name=self.collection_name,
                    metadata={"description": "MoltMobo agent memory"}
                )
                
                logger.info(f"✓ Memory initialized: {self.collection.count()} items")
            except Exception as e:
                logger.error(f"ChromaDB initialization failed: {e}")
                self.client = None
                self.collection = None
        else:
            logger.warning("⚠️  ChromaDB not available, using fallback memory")
            self.client = None
            self.collection = None
            self._fallback_memory = []
    
    def store_interaction(self, user_intent: str, observation: Dict, 
                         action_plan: Dict, result: Dict):
        """
        Store an interaction in memory
        
        Args:
            user_intent: What user wanted to do
            observation: Screen observation
            action_plan: Generated action plan
            result: Execution result
        """
        try:
            # Create memory entry
            entry = {
                'timestamp': datetime.now().isoformat(),
                'user_intent': user_intent,
                'app': observation.get('current_app'),
                'actions': action_plan.get('actions', []),
                'reasoning': action_plan.get('reasoning', ''),
                'success': result.get('success', False),
                'result_message': result.get('message', '')
            }
            
            # Store in ChromaDB
            if self.collection:
                doc_id = f"interaction_{datetime.now().timestamp()}"
                
                self.collection.add(
                    documents=[json.dumps(entry)],
                    metadatas=[{
                        'timestamp': entry['timestamp'],
                        'app': entry['app'] or 'unknown',
                        'success': str(entry['success'])
                    }],
                    ids=[doc_id]
                )
                
                logger.debug(f"Stored interaction: {doc_id}")
            else:
                # Fallback: store in memory list
                self._fallback_memory.append(entry)
                
                # Limit size
                if len(self._fallback_memory) > self.max_history:
                    self._fallback_memory.pop(0)
        
        except Exception as e:
            logger.error(f"Failed to store interaction: {e}")
    
    def retrieve_similar(self, query: str, n_results: int = 5) -> List[Dict]:
        """
        Retrieve similar past interactions
        
        Args:
            query: Query string
            n_results: Number of results to return
        
        Returns:
            List of similar interactions
        """
        try:
            if self.collection:
                results = self.collection.query(
                    query_texts=[query],
                    n_results=min(n_results, self.collection.count())
                )
                
                # Parse results
                interactions = []
                if results['documents']:
                    for doc in results['documents'][0]:
                        interactions.append(json.loads(doc))
                
                logger.debug(f"Retrieved {len(interactions)} similar interactions")
                return interactions
            else:
                # Fallback: return recent interactions
                return self._fallback_memory[-n_results:]
        
        except Exception as e:
            logger.error(f"Failed to retrieve similar interactions: {e}")
            return []
    
    def get_recent_history(self, n: int = 10) -> List[Dict]:
        """
        Get recent interaction history
        
        Args:
            n: Number of recent interactions
        
        Returns:
            List of recent interactions
        """
        try:
            if self.collection:
                # Get all and sort by timestamp
                all_items = self.collection.get()
                
                if all_items['documents']:
                    interactions = [json.loads(doc) for doc in all_items['documents']]
                    interactions.sort(key=lambda x: x['timestamp'], reverse=True)
                    return interactions[:n]
                
                return []
            else:
                # Fallback
                return self._fallback_memory[-n:]
        
        except Exception as e:
            logger.error(f"Failed to get recent history: {e}")
            return []
    
    def get_app_history(self, app_package: str, n: int = 5) -> List[Dict]:
        """
        Get history for specific app
        
        Args:
            app_package: App package name
            n: Number of interactions
        
        Returns:
            List of interactions for this app
        """
        try:
            if self.collection:
                results = self.collection.get(
                    where={"app": app_package},
                    limit=n
                )
                
                if results['documents']:
                    return [json.loads(doc) for doc in results['documents']]
                
                return []
            else:
                # Fallback: filter in-memory list
                app_interactions = [
                    entry for entry in self._fallback_memory
                    if entry.get('app') == app_package
                ]
                return app_interactions[-n:]
        
        except Exception as e:
            logger.error(f"Failed to get app history: {e}")
            return []
    
    def get_context_for_llm(self, current_app: str = None) -> str:
        """
        Get relevant context for LLM
        
        Args:
            current_app: Current app package (optional)
        
        Returns:
            Formatted context string
        """
        context_parts = []
        
        # Get recent history
        recent = self.get_recent_history(5)
        
        if recent:
            context_parts.append("Recent Interactions:")
            for i, entry in enumerate(recent, 1):
                context_parts.append(
                    f"{i}. {entry['user_intent']} in {entry.get('app', 'unknown')} "
                    f"- {'Success' if entry['success'] else 'Failed'}"
                )
        
        # Get app-specific history if current app known
        if current_app:
            app_history = self.get_app_history(current_app, 3)
            
            if app_history:
                context_parts.append(f"\nPrevious actions in {current_app}:")
                for i, entry in enumerate(app_history, 1):
                    context_parts.append(
                        f"{i}. {entry['user_intent']} - "
                        f"{'Success' if entry['success'] else 'Failed'}"
                    )
        
        return "\n".join(context_parts) if context_parts else "No previous context"
    
    def clear_memory(self):
        """Clear all memory"""
        try:
            if self.collection:
                self.client.delete_collection(self.collection_name)
                self.collection = self.client.create_collection(self.collection_name)
                logger.info("Memory cleared")
            else:
                self._fallback_memory = []
        
        except Exception as e:
            logger.error(f"Failed to clear memory: {e}")
