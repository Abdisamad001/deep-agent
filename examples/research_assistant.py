import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import config
from utils.logger import setup_logger

logger = setup_logger("examples")

def run_example():
    logger.info("Running research assistant example...")
    print(f"Agent Name: {config.get('app_name')}")
    print("This is where the research assistant logic would run.")

if __name__ == "__main__":
    run_example()
