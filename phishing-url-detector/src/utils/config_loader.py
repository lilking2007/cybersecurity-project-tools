"""
Configuration loader utility for the phishing detector system.
"""

import os
import yaml
from pathlib import Path
from typing import Any, Dict
from dotenv import load_dotenv


class ConfigLoader:
    """Load and manage application configuration."""
    
    def __init__(self, config_path: str = None):
        """
        Initialize configuration loader.
        
        Args:
            config_path: Path to config.yaml file
        """
        # Load environment variables
        load_dotenv()
        
        # Determine config path
        if config_path is None:
            base_dir = Path(__file__).parent.parent.parent
            config_path = base_dir / "config" / "config.yaml"
        
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self._override_with_env()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        
        with open(self.config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        return config or {}
    
    def _override_with_env(self):
        """Override config values with environment variables."""
        # Database
        if os.getenv('DATABASE_URL'):
            self.config['database']['url'] = os.getenv('DATABASE_URL')
        
        # Redis
        if os.getenv('REDIS_HOST'):
            self.config['redis']['host'] = os.getenv('REDIS_HOST')
        if os.getenv('REDIS_PORT'):
            self.config['redis']['port'] = int(os.getenv('REDIS_PORT'))
        if os.getenv('REDIS_PASSWORD'):
            self.config['redis']['password'] = os.getenv('REDIS_PASSWORD')
        
        # API Keys
        if os.getenv('PHISHTANK_API_KEY'):
            self.config['threat_intel']['phishtank']['api_key'] = os.getenv('PHISHTANK_API_KEY')
        if os.getenv('VIRUSTOTAL_API_KEY'):
            self.config['threat_intel']['virustotal']['api_key'] = os.getenv('VIRUSTOTAL_API_KEY')
        if os.getenv('GOOGLE_SAFE_BROWSING_API_KEY'):
            self.config['threat_intel']['google_safe_browsing']['api_key'] = os.getenv('GOOGLE_SAFE_BROWSING_API_KEY')
        
        # Flask
        if os.getenv('FLASK_SECRET_KEY'):
            self.config['app']['secret_key'] = os.getenv('FLASK_SECRET_KEY')
        if os.getenv('FLASK_DEBUG'):
            self.config['app']['debug'] = os.getenv('FLASK_DEBUG').lower() == 'true'
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation.
        
        Args:
            key_path: Dot-separated path to config value (e.g., 'app.debug')
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key_path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def get_all(self) -> Dict[str, Any]:
        """Get entire configuration dictionary."""
        return self.config.copy()


# Global config instance
_config = None


def get_config(config_path: str = None) -> ConfigLoader:
    """
    Get global configuration instance.
    
    Args:
        config_path: Optional path to config file
        
    Returns:
        ConfigLoader instance
    """
    global _config
    if _config is None:
        _config = ConfigLoader(config_path)
    return _config
