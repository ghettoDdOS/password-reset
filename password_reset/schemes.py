from dataclasses import dataclass
from pathlib import Path

from password_reset.enums import FSType


@dataclass
class Partition:
    path: Path
    fs_type: FSType | None
    is_mounted: bool
