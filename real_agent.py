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
    
    print(Fore.GREEN + "✓ System Online. Ready for tasks." + Style.RESET_ALL)

    # 2. Handle Task
    if args.task:
        task_str = " ".join(args.task)
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
                    
                executor.execute_task(user_input)
                
            except KeyboardInterrupt:
                break
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
