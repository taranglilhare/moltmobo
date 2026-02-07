"""
Memory Augmentation Engine (Second Brain)
Captures life moments, logs, and context to create a searchable life index.
"""

import time
import json
import os
from datetime import datetime
from utils.logger import logger

class MemoryAugmenter:
    def __init__(self, db_path="data/second_brain.json"):
        self.db_path = db_path
        self.memory_index = self._load_memory()
        
    def capture_moment(self, content: str, tags: list = []):
        """Index a thought, screen text, or voice note"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "content": content,
            "tags": tags,
            "id": hash(content + str(time.time()))
        }
        self.memory_index.append(entry)
        self._save_memory()
        logger.info(f"🧠 Second Brain: Captured '{content[:30]}...'")

    def recall(self, query: str) -> list:
        """Semantic search (Simulated with keyword match for Phase 1)"""
        results = []
        query = query.lower()
        
        for entry in self.memory_index:
            if query in entry["content"].lower() or any(query in t for t in entry["tags"]):
                results.append(entry)
                
        logger.info(f"🧠 Recalled {len(results)} memories for '{query}'")
        return results

    def _load_memory(self):
        if os.path.exists(self.db_path):
            try:
                with open(self.db_path, "r") as f:
                    return json.load(f)
            except:
                return []
        return []

    def _save_memory(self):
        os.makedirs("data", exist_ok=True)
        with open(self.db_path, "w") as f:
            json.dump(self.memory_index, f, indent=2)

if __name__ == "__main__":
    ma = MemoryAugmenter()
    ma.capture_moment("Idea for MoltMobo: Add hologram support", ["idea", "app"])
    print(ma.recall("hologram"))
