import yaml
import os
import time
from assistant.skills import system_hooks, media_skill, system_skill
from assistant import speaker

SCENES_FILE = os.path.join(os.path.dirname(__file__), "scenes.yaml")

class SceneEngine:
    def __init__(self):
        self.scenes = {}
        self.load_scenes()

    def load_scenes(self):
        """Load scenes from the YAML file."""
        if not os.path.exists(SCENES_FILE):
            print(f"⚠️  Scene file not found: {SCENES_FILE}")
            return

        try:
            with open(SCENES_FILE, "r") as f:
                data = yaml.safe_load(f)
                self.scenes = data.get("scenes", {})
                print(f"🎭  Loaded {len(self.scenes)} scenes from {SCENES_FILE}")
        except Exception as e:
            print(f"❌  Error loading scenes: {e}")

    def get_scene_by_trigger(self, text: str):
        """Find a scene name that matches the input text."""
        text_lower = text.lower()
        for scene_id, scene_data in self.scenes.items():
            triggers = scene_data.get("trigger_words", [])
            for trigger in triggers:
                if trigger.lower() in text_lower:
                    return scene_id
        return None

    def execute_scene(self, scene_id):
        """Execute all actions defined in a scene."""
        if scene_id not in self.scenes:
            print(f"⚠️  Scene {scene_id} not found.")
            return False

        scene = self.scenes[scene_id]
        print(f"🎬  Activating Scene: {scene.get('name', scene_id)}")
        
        actions = scene.get("actions", [])
        for action_data in actions:
            self._run_action(action_data)
            time.sleep(0.5) # Staggered execution to prevent Mac lag
            
        return True

    def _run_action(self, data):
        """Route a single YAML action to a Python skill."""
        action = data.get("action")
        value = data.get("value")

        print(f"⚙️  Executing Action: {action} ({value})")

        if action == "say":
            speaker.speak(value)
        elif action == "open_app":
            media_skill.open_app(value)
        elif action == "set_volume":
            # Map value to a string for set_volume helper
            system_hooks.set_volume(str(value))
        elif action == "mute_slack":
            system_hooks.mute_slack()
        elif action == "toggle_dark_mode":
            system_hooks.toggle_dark_mode()
        elif action == "mute":
            system_hooks.mute_volume()
        else:
            print(f"⚠️  Unknown scene action: {action}")

# Global instance
engine = SceneEngine()
