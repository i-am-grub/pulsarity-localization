"""
Pulsarity Language Pack
"""

from importlib.resources import files
from pathlib import Path
from typing import Sequence

import anyio

_LOCALS_PATH = Path(files("pulsarity_languages")) / "locals"  # type:ignore
_LANGUAGES: list[str] = [file.stem for file in _LOCALS_PATH.iterdir()]
_LANGUAGES.sort()


def load_language_pack_sync(key: str) -> str | None:
    """
    Loads the language pack synchronously

    :param key: The language pack key
    :return: The language pack data
    """

    if key in _LANGUAGES:
        path = _LOCALS_PATH / f"{key}.json"
        with path.open(encoding="utf-8") as f:
            return f.read()
    return None


async def load_language_pack_async(key: str) -> str | None:
    """
    Loads the language pack asynchronously

    :param key: The language pack key
    :return: The language pack data
    """

    if key in _LANGUAGES:
        path = _LOCALS_PATH / f"{key}.json"
        async with await anyio.open_file(path, encoding="utf-8") as f:
            return await f.read()
    return None


def get_language_packs() -> Sequence[str]:
    """
    Get the keys of all the avalible language packs the system
    is able to load

    :return: The sequence of language packs
    """
    return _LANGUAGES
