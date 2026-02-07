"""
MoltMobo Agent - The Real Autonomous Agent
Main entry point for the powerful device control agent.
"""

import sys
import os
import argparse
from colorama import init, Fore, Style
from core.adb_controller import ADBController
from core.screen_analyzer import ScreenAnalyzer
from core.task_executor import TaskExecutor
from utils.logger import logger

# Initialize colors
init()

def main():
    parser = argparse.ArgumentParser(description="MoltMobo - Real Autonomous Agent")
    parser.add_argument("task", nargs="*", help="Reaction task to perform (quoted)")
    parser.add_argument("--voice", action="store_true", help="Enable voice mode")
    parser.add_argument("--interactive", "-i", action="store_true", help="Interactive shell mode")
    
    args = parser.parse_args()

    print(Fore.CYAN + """
    ╔════════════════════════════════════════╗
    ║      MoltMobo - Sovereign Agent        ║
    ║      Full Device Control System        ║
    ╚════════════════════════════════════════╝
    """ + Style.RESET_ALL)

    # 1. Initialize Core
    logger.info("Initializing Core Engine...")
    adb = ADBController()
    
    if not adb.connected:
        print(Fore.RED + "❌ Fatal: No device connected via ADB." + Style.RESET_ALL)
        print("Please enable USB debugging and connect your phone.")
        print("Run 'adb devices' to verify.")
        return

    analyzer = ScreenAnalyzer(adb)
    executor = TaskExecutor(adb, analyzer)
    
    # --- REVOLUTIONARY MODULES INIT ---
    print(Fore.MAGENTA + "🔮 Initializing Sci-Fi Features..." + Style.RESET_ALL)
    
    # 1. Mood Enhancer
    from intelligence.mood_analyzer import MoodAnalyzer
    mood_ai = MoodAnalyzer()
    
    # 2. Privacy Vault
    from security.privacy_vault import PrivacyVault
    vault = PrivacyVault()
    
    # 3. Learning Tutor
    from intelligence.learning_tutor import LearningTutor
    tutor = LearningTutor()
    
    # 4. Second Brain
    from intelligence.memory_augmenter import MemoryAugmenter
    brain = MemoryAugmenter()
    
    # 5. Health & Eco
    from health.bio_sync import BioSyncOptimizer
    bio = BioSyncOptimizer()
    from core.eco_tracker import EcoTracker
    eco = EcoTracker()
    
    # 6. UI Morpher
    from core.ui_morpher import AdaptiveUIMorpher
    morpher = AdaptiveUIMorpher(adb)
    
    print(Fore.GREEN + "✓ System Online. Ready for tasks." + Style.RESET_ALL)

    # 2. Handle Task
    if args.task:
        task_str = " ".join(args.task)
        
        # Analyze mood & Track Eco Impact
        mood_ai.analyze_text_input(task_str)
        eco.track_activity("screen_time", 1) # Mock duration
        
        # Update Bio Metics
        bio.update_metrics(screen_on=True)
        
        # Store in Second Brain
        brain.capture_moment(f"User Command: {task_str}", ["command", "history"])
        
        # Check for Dream Journal context
        if "dream" in task_str.lower():
            from intelligence.dream_journal import DreamJournal
            insight = DreamJournal().log_dream(task_str)
            print(f"🌙 Dream Analysis: {insight}")
        
        # Verify Privacy for sensitive data
        if "password" in task_str.lower() or "bank" in task_str.lower():
            logger.warning("🔒 Sensitive data detected! Storing in decentralized vault.")
            vault.store_data("sensitive_cmd", {"cmd": task_str})
            print("✓ Data secured in blockchain vault.")
        
        executor.execute_task(task_str)
    
    # 3. Interactive Mode
    elif args.interactive:
        print(Fore.YELLOW + "Entering Interactive Mode (type 'exit' to quit)" + Style.RESET_ALL)
        while True:
            try:
                user_input = input(Fore.BLUE + "MoltMobo> " + Style.RESET_ALL)
                if user_input.lower() in ['exit', 'quit']:
                    break
                if not user_input.strip():
                    continue
                
                # --- Real-time Sci-Fi Analysis ---
                mood_ai.analyze_text_input(user_input)
                brain.capture_moment(user_input, ["interaction"])
                
                # Check for Tutor context (Mock)
                if "math" in user_input or "learn" in user_input:
                     tutor.generate_micro_lesson("Concept detected")

                executor.execute_task(user_input)
                
            except KeyboardInterrupt:
                break
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
