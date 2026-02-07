"""
MoltMobo Demo Script
Demonstrates key features of the agent
"""

import time
from moltmobo_agent import MoltMoboAgent
from utils.logger import logger


class MoltMoboDemo:
    """Demo scenarios for MoltMobo agent"""
    
    def __init__(self):
        """Initialize demo"""
        self.agent = MoltMoboAgent()
        
    def run_all_demos(self):
        """Run all demo scenarios"""
        print("\n" + "=" * 60)
        print("🎬 MoltMobo Agent Demo")
        print("=" * 60)
        
        # Connect to device
        if not self.agent.connect():
            print("❌ Failed to connect to device")
            return
        
        demos = [
            ("Basic Navigation", self.demo_basic_navigation),
            ("Web Search", self.demo_web_search),
            ("Privacy Protection", self.demo_privacy_protection),
            ("Memory & Context", self.demo_memory_context),
            ("Policy Enforcement", self.demo_policy_enforcement),
        ]
        
        for name, demo_func in demos:
            print(f"\n{'=' * 60}")
            print(f"📍 Demo: {name}")
            print("=" * 60)
            
            try:
                demo_func()
                print(f"✅ {name} completed")
            except Exception as e:
                print(f"❌ {name} failed: {e}")
            
            time.sleep(2)
        
        # Cleanup
        self.agent.disconnect()
        
        print("\n" + "=" * 60)
        print("🎉 Demo Complete!")
        print("=" * 60)
    
    def demo_basic_navigation(self):
        """Demo basic navigation commands"""
        print("\n📱 Testing basic navigation...")
        
        # Go home
        result = self.agent.execute_task("Go to home screen")
        print(f"Home: {result['message']}")
        
        time.sleep(1)
        
        # Open app
        result = self.agent.execute_task("Open Chrome")
        print(f"Open Chrome: {result['message']}")
    
    def demo_web_search(self):
        """Demo web search capability"""
        print("\n🔍 Testing web search...")
        
        result = self.agent.execute_task(
            "Open Chrome and search for weather in Tokyo"
        )
        
        print(f"Search result: {result['message']}")
        print(f"Actions executed: {result.get('actions_executed', 0)}")
    
    def demo_privacy_protection(self):
        """Demo privacy firewall"""
        print("\n🔒 Testing privacy protection...")
        
        # Simulate sensitive data scenario
        print("Scenario: Agent detects password field")
        print("Expected: Routes to local LLM instead of cloud")
        
        # This would normally detect sensitive content
        result = self.agent.execute_task(
            "Check if there are any password fields on screen"
        )
        
        print(f"Privacy check: {result['message']}")
    
    def demo_memory_context(self):
        """Demo memory and context awareness"""
        print("\n🧠 Testing memory and context...")
        
        # First task
        result1 = self.agent.execute_task("Open Spotify")
        print(f"Task 1: {result1['message']}")
        
        time.sleep(1)
        
        # Second task with context
        result2 = self.agent.execute_task(
            "Remember what app I just opened"
        )
        print(f"Task 2 (with memory): {result2['message']}")
        
        # Check memory
        recent = self.agent.memory.get_recent_history(3)
        print(f"\nRecent history: {len(recent)} interactions stored")
    
    def demo_policy_enforcement(self):
        """Demo policy and whitelist enforcement"""
        print("\n🛡️ Testing policy enforcement...")
        
        # Try to access allowed app
        print("Test 1: Accessing allowed app (Chrome)")
        is_allowed = self.agent.policy.is_app_allowed("com.android.chrome")
        print(f"Chrome allowed: {is_allowed}")
        
        # Try to access forbidden app
        print("\nTest 2: Accessing forbidden app (Banking)")
        is_allowed = self.agent.policy.is_app_allowed("com.example.bank")
        print(f"Banking app allowed: {is_allowed}")
        
        # Check stealth mode
        print("\nTest 3: Stealth mode activation")
        self.agent.policy.activate_stealth_mode(10)  # Simulate 10% battery
        print(f"Stealth mode active: {self.agent.policy.stealth_mode_active}")


def main():
    """Run demo"""
    demo = MoltMoboDemo()
    demo.run_all_demos()


if __name__ == "__main__":
    main()
