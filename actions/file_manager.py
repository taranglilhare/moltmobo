"""
File Manager - ADB File Operations
Handles pulling/pushing files, organizing media, etc.
"""

import os
from datetime import datetime
from core.adb_controller import ADBController
from utils.logger import logger

class FileManager:
    def __init__(self, adb: ADBController):
        self.adb = adb
        
    def download_latest_photos(self, count: int = 10, target_dir: str = "./downloads/photos"):
        """Download latest photos from Camera folder"""
        logger.info(f"📂 Downloading latest {count} photos...")
        
        os.makedirs(target_dir, exist_ok=True)
        
        # List files in DCIM/Camera sorted by date (using ls -t)
        # Note: Android shell ls might vary, simple ls order usually works somewhat or use adb shell ls -t
        try:
            # Get list of files
            cmd = "ls -t /sdcard/DCIM/Camera/"
            files_str = self.adb.shell(cmd)
            files = [f for f in files_str.split('\n') if f.endswith('.jpg') or f.endswith('.mp4')]
            
            # Take top N
            to_download = files[:count]
            
            for filename in to_download:
                filename = filename.strip()
                if not filename: continue
                
                remote = f"/sdcard/DCIM/Camera/{filename}"
                local = os.path.join(target_dir, filename)
                
                self.adb.execute(f"pull {remote} {local}")
                logger.debug(f"Pulled: {filename}")
                
            logger.info(f"✓ Downloaded {len(to_download)} files to {target_dir}")
            return True
        except Exception as e:
            logger.error(f"File download failed: {e}")
            return False

    def list_files(self, path: str = "/sdcard/Download") -> str:
        return self.adb.shell(f"ls {path}")
