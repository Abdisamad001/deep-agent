import argparse
from config.settings import config
from utils.logger import setup_logger

logger = setup_logger("cli")

def main():
    parser = argparse.ArgumentParser(description=f"{config.get('app_name')} CLI")
    parser.add_argument("--query", "-q", type=str, help="Query for the agent")
    args = parser.parse_args()

    if args.query:
        logger.info(f"Received query: {args.query}")
        print(f"Processing: {args.query}")
        # Placeholder logic
        print("Done.")
    else:
        logger.warning("No query provided")
        parser.print_help()

if __name__ == "__main__":
    main()
