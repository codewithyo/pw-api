import json
from pathlib import Path
from typing import Any

from src.core.logger import get_logger

logger = get_logger(__name__)


def load_json(fp: Path) -> Any:
    with fp.open() as f:
        logger.info(f"Load '{fp}'")
        return json.load(f)


def dump_json(obj: object, fp: Path) -> None:
    with fp.open("w") as f:
        logger.info(f"Dump '{fp}'")
        json.dump(obj, f, indent=2)
