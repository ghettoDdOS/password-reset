from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from password_reset.enums import FSType


@dataclass
class Partition:
    path: Path
    fs_type: Optional[FSType]
    is_mounted: bool
