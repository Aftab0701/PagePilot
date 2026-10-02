"""Run the PagePilot CLI with ``python -m pagepilot``."""

import sys

from pagepilot.cli import main

if __name__ == '__main__':
	result = main()
	if result is not None:
		sys.exit(result)
