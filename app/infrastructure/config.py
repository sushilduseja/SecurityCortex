import os
from dataclasses import dataclass
from typing import Dict, Any, Optional

@dataclass
class DatabaseConfig:
    db_type: str = "sqlite"
    db_path: str = 'database/data/aigovernance.db'
    postgres_url: Optional[str] = None

@dataclass
class ApplicationConfig:
    debug: bool = False
    port: int = 5000
    host: str = "0.0.0.0"
    static_folder: str = "static"

@dataclass
class Config:
    app: ApplicationConfig
    database: DatabaseConfig
    
    @classmethod
    def load(cls) -> 'Config':
        """Load configuration from environment variables or default values."""
        db_config = DatabaseConfig(
            db_type=os.environ.get("DB_TYPE", "sqlite"),
            db_path=os.environ.get("DB_PATH", 'database/data/aigovernance.db'),
            postgres_url=os.environ.get("DATABASE_URL")
        )
        
        app_config = ApplicationConfig(
            debug=os.environ.get("DEBUG", "False").lower() == "true",
            port=int(os.environ.get("PORT", 5000)),
            host=os.environ.get("HOST", "0.0.0.0"),
            static_folder=os.environ.get("STATIC_FOLDER", "static")
        )
        
        return cls(app=app_config, database=db_config)

# Global configuration instance
config = Config.load()