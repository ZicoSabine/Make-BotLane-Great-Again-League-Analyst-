from pathlib import Path

GAME_NAME = "Eunhaa"
TAG_LINE = "0994"

PLATFORM_ROUTE = "asia"
REGIONAL_ROUTE = "asia"

SCRIPT_DIRECTORY = Path(__file__).resolve().parent
DATA_DIRECTORY = SCRIPT_DIRECTORY / "data"

DATA_DIRECTORY.mkdir(exist_ok=True)