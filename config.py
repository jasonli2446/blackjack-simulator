import json
import os


class Config:
    """Manages configuration settings for the game."""

    DEFAULT_CONFIG = {
        "input": {
            "use_video": False,
            "display_video": True,
            "keyboard_fallback": True,
            "camera_id": 0,
        },
        "game": {
            "initial_balance": 1000.0,
            "default_bet": 100.0,
            "show_strategy": True,
        },
        "ui": {"animation_delay": 1.0},
    }

    def __init__(self, config_file="config.json"):
        """
        Initialize the configuration manager.

        Args:
            config_file (str): Path to the configuration file
        """
        self.config_file = config_file
        self.settings = self._load_config()

    def _load_config(self):
        """
        Load configuration from file or create default.

        Returns:
            dict: Configuration settings
        """
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as f:
                    config = json.load(f)

                # Ensure all default keys exist
                for section, values in self.DEFAULT_CONFIG.items():
                    if section not in config:
                        config[section] = values
                    else:
                        for key, value in values.items():
                            if key not in config[section]:
                                config[section][key] = value

                return config
            except Exception as e:
                print(f"Error loading configuration: {e}")
                return self.DEFAULT_CONFIG.copy()
        else:
            return self.DEFAULT_CONFIG.copy()

    def save_config(self):
        """Save the current configuration to file."""
        try:
            with open(self.config_file, "w") as f:
                json.dump(self.settings, f, indent=4)
        except Exception as e:
            print(f"Error saving configuration: {e}")

    def get(self, section, key, default=None):
        """
        Get a configuration value.

        Args:
            section (str): Configuration section
            key (str): Configuration key
            default: Default value if not found

        Returns:
            The configuration value or default
        """
        if section in self.settings and key in self.settings[section]:
            return self.settings[section][key]
        return default

    def set(self, section, key, value):
        """
        Set a configuration value.

        Args:
            section (str): Configuration section
            key (str): Configuration key
            value: Value to set
        """
        if section not in self.settings:
            self.settings[section] = {}

        self.settings[section][key] = value
        self.save_config()
