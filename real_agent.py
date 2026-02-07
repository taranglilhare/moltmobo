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
    
    # 7. Social & Creative
    from social.translator import MultiversalTranslator
    translator = MultiversalTranslator()
    from social.weaver import SocialWeaver
    weaver = SocialWeaver()
    from social.empathy_trainer import EmpathyTrainer
    empathy = EmpathyTrainer()
    from creative.fusion_generator import CreativeFusion
    fusion = CreativeFusion()
    
    # 8. God Mode Features
    from quantum.decision_sim import QuantumDecisionSim
    quantum = QuantumDecisionSim()
    from security.ethical_auditor import EthicalAuditor
    auditor = EthicalAuditor(adb)
    from core.crisis_oracle import CrisisOracle
    oracle = CrisisOracle()
    from core.energy_harvester import EnergyHarvester
    harvester = EnergyHarvester(adb)
    from core.evolution_engine import EvolutionEngine
    evolver = EvolutionEngine()
    
    print(Fore.GREEN + "✓ System Online. Ready for tasks." + Style.RESET_ALL)
    
    # Background Checks
    status = oracle.check_global_status()
    if status == "RED":
        print(Fore.RED + "🚨 EMERGENCY PROTOCOL ACTIVE" + Style.RESET_ALL)
    
    harvester.simulate_harvesting()

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
        
        # Quantum Decision Check
        if "decide" in task_str.lower() or "choice" in task_str.lower():
             q_res = quantum.simulate_decision("Option A", "Option B") # Mock extraction
             print(q_res)

        # Audit Check
        if "audit" in task_str.lower():
             report = auditor.audit_app("com.example.app") # Mock package
             print(report)

        # Creative Fusion Check
        if "mix" in task_str.lower() or "fuse" in task_str.lower():
            # simple parsing for demo
            parts = task_str.split("and")
            if len(parts) >= 2:
                res = fusion.generate_fusion(parts[0], parts[1])
                print(f"🎨 Creative Fusion: {res}")
                
        # Translator Check
        if "translate" in task_str.lower():
             # Mock target language detection
             res = translator.translate_with_nuance(task_str, "Spanish") 
             print(f"🌐 Translation: {res}")

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
