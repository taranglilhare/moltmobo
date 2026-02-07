"""
Decentralized Privacy Vault
Simulates a blockchain-based secure storage for sensitive data.
Uses local encryption key management (simulating wallet).
"""

import os
import json
import hashlib
import base64
from cryptography.fernet import Fernet
from utils.logger import logger

class PrivacyVault:
    def __init__(self, storage_file="data/vault.enc"):
        self.storage_file = storage_file
        self.key_file = "data/vault.key"
        self.cipher = None
        self._load_or_generate_key()
        
    def _load_or_generate_key(self):
        """Load encryption key or generate new one (Simulating Private Key)"""
        if os.path.exists(self.key_file):
            with open(self.key_file, "rb") as f:
                self.key = f.read()
        else:
            self.key = Fernet.generate_key()
            os.makedirs("data", exist_ok=True)
            with open(self.key_file, "wb") as f:
                f.write(self.key)
        
        self.cipher = Fernet(self.key)

    def store_data(self, key: str, data: dict):
        """Encrypt and store data in the vault"""
        # 1. Serialize
        json_data = json.dumps(data)
        
        # 2. Encrypt
        encrypted_data = self.cipher.encrypt(json_data.encode())
        
        # 3. Hash for integrity (Block simulation)
        block_hash = hashlib.sha256(encrypted_data).hexdigest()
        
        # 4. Store (Simulating writing to Block)
        # In real IPFS, this would return a CID
        record = {
            "id": key,
            "data": base64.b64encode(encrypted_data).decode(),
            "hash": block_hash,
            "timestamp": time.time()
        }
        
        self._append_to_chain(record)
        logger.info(f"🔒 Data stored in Privacy Vault. Hash: {block_hash[:8]}...")

    def retrieve_data(self, key: str) -> Optional[dict]:
        """Retrieve and decrypt data"""
        chain = self._read_chain()
        for block in reversed(chain):
            if block["id"] == key:
                try:
                    encrypted_data = base64.b64decode(block["data"])
                    decrypted_json = self.cipher.decrypt(encrypted_data).decode()
                    return json.loads(decrypted_json)
                except Exception as e:
                    logger.error(f"Decryption failed: {e}")
                    return None
        return None

    def _append_to_chain(self, record: dict):
        chain = self._read_chain()
        chain.append(record)
        with open(self.storage_file, "w") as f:
            json.dump(chain, f)

    def _read_chain(self) -> list:
        if not os.path.exists(self.storage_file):
            return []
        try:
            with open(self.storage_file, "r") as f:
                return json.load(f)
        except:
            return []

import time

if __name__ == "__main__":
    vault = PrivacyVault()
    vault.store_data("health_record", {"heart_rate": 72, "steps": 10000})
    data = vault.retrieve_data("health_record")
    print(f"Decrypted: {data}")
