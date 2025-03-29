import os
import logging
from typing import Dict, Any

# Default configuration
DEFAULT_CONFIG = {
    # Application settings
    'APP_NAME': 'AI Governance Dashboard',
    'APP_VERSION': '1.0.0',
    'DEBUG': False,
    'TESTING': False,
    'LOG_LEVEL': 'INFO',
    
    # Database settings
    'DB_TYPE': 'sqlite',  # 'sqlite' or 'postgres'
    'DB_NAME': 'ai_governance.db',
    'DB_HOST': 'localhost',
    'DB_PORT': 5432,
    'DB_USER': '',
    'DB_PASSWORD': '',
    
    # Feature flags
    'ENABLE_SMS_NOTIFICATIONS': False,
    'ENABLE_EMAIL_NOTIFICATIONS': False,
    
    # API settings
    'API_PREFIX': '/api/v1',
    
    # UI settings
    'UI_THEME': 'light',
    'RECORDS_PER_PAGE': 10
}

class AppConfig:
    """Application configuration manager."""
    
    def __init__(self):
        """Initialize with default configuration and environment overrides."""
        self._config = DEFAULT_CONFIG.copy()
        self._load_from_env()
        self._setup_logging()
    
    def _load_from_env(self):
        """Load configuration from environment variables."""
        for key in self._config:
            env_value = os.environ.get(key)
            if env_value is not None:
                # Convert string to appropriate type based on default value
                default_value = self._config[key]
                if isinstance(default_value, bool):
                    self._config[key] = env_value.lower() in ('true', 'yes', '1')
                elif isinstance(default_value, int):
                    try:
                        self._config[key] = int(env_value)
                    except ValueError:
                        # Keep default if conversion fails
                        pass
                elif isinstance(default_value, float):
                    try:
                        self._config[key] = float(env_value)
                    except ValueError:
                        # Keep default if conversion fails
                        pass
                else:
                    self._config[key] = env_value
        
        # Special handling for database URL if provided
        if 'DATABASE_URL' in os.environ:
            self._config['DB_TYPE'] = 'postgres'
    
    def _setup_logging(self):
        """Set up application logging based on configuration."""
        log_level_name = self._config['LOG_LEVEL']
        log_level = getattr(logging, log_level_name.upper(), logging.INFO)
        
        # Configure root logger
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Create a logger for this module
        self.logger = logging.getLogger('aigovernance.config')
        self.logger.setLevel(log_level)
        
        # Log initial configuration (excluding sensitive values)
        safe_config = {k: '******' if k in ('DB_PASSWORD',) else v 
                     for k, v in self._config.items()}
        self.logger.info(f"Application configured with: {safe_config}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.
        
        Args:
            key: The configuration key
            default: Default value if key is not found
            
        Returns:
            The configuration value
        """
        return self._config.get(key, default)
    
    def get_all(self) -> Dict[str, Any]:
        """
        Get all configuration values.
        
        Returns:
            Dictionary of all configuration values
        """
        return self._config.copy()
    
    def is_production(self) -> bool:
        """
        Check if the application is running in production mode.
        
        Returns:
            True if in production mode, False otherwise
        """
        return not (self.get('DEBUG') or self.get('TESTING'))
    
    def is_development(self) -> bool:
        """
        Check if the application is running in development mode.
        
        Returns:
            True if in development mode, False otherwise
        """
        return self.get('DEBUG') and not self.get('TESTING')
    
    def is_testing(self) -> bool:
        """
        Check if the application is running in testing mode.
        
        Returns:
            True if in testing mode, False otherwise
        """
        return self.get('TESTING')


# Create a singleton instance
config = AppConfig()