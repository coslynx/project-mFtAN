import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """
    Handles loading and managing configuration settings from the .env file.
    """

    def __init__(self):
        self.config = {}
        self.load_config()

    def load_config(self):
        """
        Loads configuration settings from the .env file.
        """
        try:
            for key, value in os.environ.items():
                self.config[key] = value
        except FileNotFoundError:
            print("Error: .env file not found. Please create a .env file with your configuration settings.")

    def get_value(self, key):
        """
        Retrieves the value of a specific configuration setting.
        """
        try:
            return self.config[key]
        except KeyError:
            print(f"Error: Configuration setting '{key}' not found in .env file.")
            return None