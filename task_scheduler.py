"""
Task Scheduler - Free Automation System
Cron-like scheduling for automated tasks
"""

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.date import DateTrigger
from datetime import datetime, timedelta
from typing import Callable, Dict, List, Optional
import yaml
from pathlib import Path

from utils.logger import logger


class TaskScheduler:
    """Task scheduler for automation"""
    
    def __init__(self, config_path: str = "./config/tasks.yaml"):
        """
        Initialize task scheduler
        
        Args:
            config_path: Path to tasks configuration
        """
        self.scheduler = BackgroundScheduler()
        self.config_path = Path(config_path)
        self.tasks: Dict[str, Dict] = {}
        
        # Load tasks from config
        self._load_tasks()
        
        logger.info("✓ Task Scheduler initialized")
    
    def _load_tasks(self):
        """Load tasks from YAML config"""
        if not self.config_path.exists():
            logger.info("No tasks config found, creating default")
            self._create_default_config()
            return
        
        try:
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f)
            
            tasks = config.get('tasks', [])
            logger.info(f"Loaded {len(tasks)} tasks from config")
            
            # Register tasks
            for task in tasks:
                self.register_task_from_config(task)
        
        except Exception as e:
            logger.error(f"Failed to load tasks: {e}")
    
    def _create_default_config(self):
        """Create default tasks configuration"""
        default_config = {
            'tasks': [
                {
                    'name': 'morning_routine',
                    'description': 'Morning routine automation',
                    'schedule': '8:00 AM daily',
                    'enabled': False,
                    'actions': [
                        {'type': 'check_weather'},
                        {'type': 'read_news'},
                        {'type': 'check_calendar'}
                    ]
                },
                {
                    'name': 'backup_photos',
                    'description': 'Weekly photo backup',
                    'schedule': 'Sunday 11:00 PM',
                    'enabled': False,
                    'actions': [
                        {'type': 'backup_photos', 'destination': 'cloud'}
                    ]
                }
            ]
        }
        
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w') as f:
            yaml.dump(default_config, f, default_flow_style=False)
        
        logger.info(f"Created default config: {self.config_path}")
    
    def register_task_from_config(self, task_config: Dict):
        """Register task from configuration"""
        name = task_config.get('name')
        schedule = task_config.get('schedule')
        enabled = task_config.get('enabled', True)
        
        if not enabled:
            logger.info(f"Task '{name}' is disabled, skipping")
            return
        
        # Parse schedule
        trigger = self._parse_schedule(schedule)
        
        if not trigger:
            logger.error(f"Invalid schedule for task '{name}': {schedule}")
            return
        
        # Register task
        self.tasks[name] = task_config
        
        # Add job to scheduler
        self.scheduler.add_job(
            func=self._execute_task,
            trigger=trigger,
            args=[name],
            id=name,
            name=task_config.get('description', name),
            replace_existing=True
        )
        
        logger.info(f"✓ Registered task: {name} ({schedule})")
    
    def _parse_schedule(self, schedule_str: str):
        """
        Parse schedule string to trigger
        
        Formats:
        - "8:00 AM daily" -> Daily at 8 AM
        - "Monday 9:00 AM" -> Every Monday at 9 AM
        - "Every 30 minutes" -> Interval
        - "2026-02-07 10:00" -> One-time
        """
        schedule_lower = schedule_str.lower()
        
        # Daily schedule
        if 'daily' in schedule_lower:
            # Extract time
            import re
            time_match = re.search(r'(\d{1,2}):(\d{2})\s*(am|pm)?', schedule_lower)
            if time_match:
                hour = int(time_match.group(1))
                minute = int(time_match.group(2))
                am_pm = time_match.group(3)
                
                if am_pm == 'pm' and hour != 12:
                    hour += 12
                elif am_pm == 'am' and hour == 12:
                    hour = 0
                
                return CronTrigger(hour=hour, minute=minute)
        
        # Weekly schedule
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        for i, day in enumerate(days):
            if day in schedule_lower:
                # Extract time
                import re
                time_match = re.search(r'(\d{1,2}):(\d{2})\s*(am|pm)?', schedule_lower)
                if time_match:
                    hour = int(time_match.group(1))
                    minute = int(time_match.group(2))
                    am_pm = time_match.group(3)
                    
                    if am_pm == 'pm' and hour != 12:
                        hour += 12
                    elif am_pm == 'am' and hour == 12:
                        hour = 0
                    
                    return CronTrigger(day_of_week=i, hour=hour, minute=minute)
        
        # Interval schedule
        if 'every' in schedule_lower:
            import re
            interval_match = re.search(r'every\s+(\d+)\s+(minute|hour|day)', schedule_lower)
            if interval_match:
                value = int(interval_match.group(1))
                unit = interval_match.group(2)
                
                if unit == 'minute':
                    return IntervalTrigger(minutes=value)
                elif unit == 'hour':
                    return IntervalTrigger(hours=value)
                elif unit == 'day':
                    return IntervalTrigger(days=value)
        
        return None
    
    def _execute_task(self, task_name: str):
        """Execute a scheduled task"""
        logger.info(f"⏰ Executing scheduled task: {task_name}")
        
        task = self.tasks.get(task_name)
        if not task:
            logger.error(f"Task not found: {task_name}")
            return
        
        actions = task.get('actions', [])
        
        for action in actions:
            try:
                self._execute_action(action)
            except Exception as e:
                logger.error(f"Action failed: {e}")
    
    def _execute_action(self, action: Dict):
        """Execute a single action"""
        action_type = action.get('type')
        
        logger.info(f"Executing action: {action_type}")
        
        # This would integrate with the main agent
        # For now, just log
        logger.info(f"Action: {action}")
    
    def add_task(self, name: str, schedule: str, callback: Callable, **kwargs):
        """
        Add a new task programmatically
        
        Args:
            name: Task name
            schedule: Schedule string
            callback: Function to call
            **kwargs: Additional arguments for the job
        """
        trigger = self._parse_schedule(schedule)
        
        if not trigger:
            logger.error(f"Invalid schedule: {schedule}")
            return False
        
        self.scheduler.add_job(
            func=callback,
            trigger=trigger,
            id=name,
            name=name,
            replace_existing=True,
            **kwargs
        )
        
        logger.info(f"✓ Added task: {name}")
        return True
    
    def remove_task(self, name: str):
        """Remove a task"""
        try:
            self.scheduler.remove_job(name)
            if name in self.tasks:
                del self.tasks[name]
            logger.info(f"✓ Removed task: {name}")
            return True
        except Exception as e:
            logger.error(f"Failed to remove task: {e}")
            return False
    
    def list_tasks(self) -> List[Dict]:
        """List all scheduled tasks"""
        jobs = self.scheduler.get_jobs()
        
        tasks = []
        for job in jobs:
            tasks.append({
                'id': job.id,
                'name': job.name,
                'next_run': job.next_run_time,
                'trigger': str(job.trigger)
            })
        
        return tasks
    
    def start(self):
        """Start the scheduler"""
        if not self.scheduler.running:
            self.scheduler.start()
            logger.info("✓ Task Scheduler started")
    
    def stop(self):
        """Stop the scheduler"""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("Task Scheduler stopped")
    
    def pause_task(self, name: str):
        """Pause a specific task"""
        try:
            self.scheduler.pause_job(name)
            logger.info(f"Paused task: {name}")
        except Exception as e:
            logger.error(f"Failed to pause task: {e}")
    
    def resume_task(self, name: str):
        """Resume a paused task"""
        try:
            self.scheduler.resume_job(name)
            logger.info(f"Resumed task: {name}")
        except Exception as e:
            logger.error(f"Failed to resume task: {e}")
