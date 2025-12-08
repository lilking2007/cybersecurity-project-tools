#!/usr/bin/env python3
"""
Quick Start Script for Phishing URL Detector

Sets up the environment and runs the application.
"""

import os
import sys
from pathlib import Path
import subprocess


def print_header(text):
    """Print formatted header."""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)


def check_python_version():
    """Check if Python version is adequate."""
    print_header("Checking Python Version")
    
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print("❌ Error: Python 3.9 or higher is required")
        sys.exit(1)
    
    print("✅ Python version is compatible")


def create_directories():
    """Create necessary directories."""
    print_header("Creating Directories")
    
    directories = [
        'data/models',
        'data/raw',
        'data/processed',
        'logs',
        'app/static',
        'app/templates'
    ]
    
    for directory in directories:
        path = Path(directory)
        path.mkdir(parents=True, exist_ok=True)
        print(f"✅ Created: {directory}")


def install_dependencies():
    """Install Python dependencies."""
    print_header("Installing Dependencies")
    
    print("Installing required packages...")
    try:
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
        ])
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Error installing dependencies")
        sys.exit(1)


def setup_config():
    """Setup configuration file."""
    print_header("Setting Up Configuration")
    
    env_example = Path('.env.example')
    env_file = Path('.env')
    
    if not env_file.exists() and env_example.exists():
        import shutil
        shutil.copy(env_example, env_file)
        print("✅ Created .env file from template")
        print("⚠️  Please edit .env and add your API keys")
    else:
        print("✅ Configuration file already exists")


def train_initial_model():
    """Train initial model with sample data."""
    print_header("Training Initial Model")
    
    print("Training model with sample data...")
    print("⚠️  For production, provide a labeled dataset")
    
    try:
        subprocess.check_call([
            sys.executable, 'scripts/train_model.py'
        ])
        print("✅ Model trained successfully")
    except subprocess.CalledProcessError:
        print("⚠️  Model training failed (optional step)")


def start_application():
    """Start the Flask application."""
    print_header("Starting Application")
    
    print("Starting Phishing URL Detector...")
    print("Access the dashboard at: http://localhost:5000")
    print("\nPress Ctrl+C to stop the server\n")
    
    try:
        subprocess.check_call([
            sys.executable, 'app/main.py'
        ])
    except KeyboardInterrupt:
        print("\n\n✅ Application stopped")


def main():
    """Main setup and run function."""
    print("\n" + "=" * 70)
    print("  🛡️  PHISHING URL DETECTOR - QUICK START")
    print("=" * 70)
    
    # Change to project directory
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    
    # Run setup steps
    check_python_version()
    create_directories()
    
    # Ask user if they want to install dependencies
    print("\n" + "=" * 70)
    response = input("Install dependencies? (y/n): ").lower()
    if response == 'y':
        install_dependencies()
    
    setup_config()
    
    # Ask user if they want to train model
    print("\n" + "=" * 70)
    response = input("Train initial model? (y/n): ").lower()
    if response == 'y':
        train_initial_model()
    
    # Ask user if they want to start the app
    print("\n" + "=" * 70)
    response = input("Start the application now? (y/n): ").lower()
    if response == 'y':
        start_application()
    else:
        print("\n✅ Setup complete!")
        print("\nTo start the application later, run:")
        print("  python app/main.py")
        print("\nOr use Docker:")
        print("  docker-compose up")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✅ Setup cancelled")
        sys.exit(0)
