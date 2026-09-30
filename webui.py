"""
PagePilot — WebUI Entrypoint
Run with: python webui.py --ip 127.0.0.1 --port 7788
"""

import argparse
import sys
import uvicorn
from dotenv import load_dotenv

load_dotenv()


def main():
    parser = argparse.ArgumentParser(description="PagePilot Autonomous Web Agent UI")
    parser.add_argument("--ip", type=str, default="127.0.0.1", help="IP address to bind to")
    parser.add_argument("--port", type=int, default=7788, help="Port to listen on")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload for development")
    args = parser.parse_args()

    print(f"\n=======================================================")
    print(f"  PagePilot Autonomous Browser Agent")
    print(f"  Interface running at: http://{args.ip}:{args.port}")
    print(f"=======================================================\n")

    uvicorn.run(
        "pagepilot.webui.server:app",
        host=args.ip,
        port=args.port,
        reload=args.reload,
        log_level="info"
    )


if __name__ == "__main__":
    main()
