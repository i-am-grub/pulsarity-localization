"""
Pulsarity Language Pack
"""

import importlib.metadata
import json
from importlib.resources import files
from pathlib import Path
from typing import Sequence, TypedDict
from venv import logger

import anyio

__version__ = importlib.metadata.version(__name__)

_LOCALS_PATH = Path(files("pulsarity_localization")) / "locals"  # type:ignore
_LANGUAGES: list[str] = [file.stem for file in _LOCALS_PATH.iterdir()]
_LANGUAGES.sort()


class LocalizationData(TypedDict):
    """
    Parsed localization data
    """

    messages: dict[str, str]
    pluralization: dict[str, str]


def load_language_pack_sync(key: str) -> LocalizationData | None:
    """
    Loads the language pack synchronously

    :param key: The language pack key
    :return: The language pack data
    """

    if key in _LANGUAGES:
        path = _LOCALS_PATH / f"{key}.json"
        with path.open(encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                msg = "Failed to parse localization data"
                logger.exception(msg)

    return None


async def load_language_pack_async(key: str) -> LocalizationData | None:
    """
    Loads the language pack asynchronously

    :param key: The language pack key
    :return: The language pack data
    """

    if key in _LANGUAGES:
        path = _LOCALS_PATH / f"{key}.json"
        async with await anyio.open_file(path, encoding="utf-8") as f:
            data = await f.read()
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                msg = "Failed to parse localization data"
                logger.exception(msg)

    return None


def get_language_packs() -> Sequence[str]:
    """
    Get the keys of all the avalible language packs the system
    is able to load

    :return: The sequence of language packs
    """
    return _LANGUAGES
