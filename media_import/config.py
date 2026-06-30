"""
Configuration models and enums for the Media Import Tool.
"""

from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path


class SourceType(Enum):
    LOCAL = auto()
    URL = auto()


class MediaType(Enum):
    MOVIE = auto()
    TV_SHOW = auto()


class ImportType(Enum):
    MOVIE = auto()
    SINGLE_EPISODE = auto()
    FULL_SEASON = auto()


@dataclass
class ImportConfig:
    source_type: SourceType
    media_type: MediaType
    import_type: ImportType

    source: str

    title: str | None = None
    year: int | None = None
    season: int | None = None

    working_directory: Path | None = None
    downloaded: bool = False
