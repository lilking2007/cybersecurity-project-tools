import os

class Config:
    PROJECT_NAME = "Sentinel"
    VERSION = "0.1.0"
    DEBUG = os.getenv("DEBUG", True)
    
    # Paths
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), 'data')
    
    # Database
    ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")

config = Config()
