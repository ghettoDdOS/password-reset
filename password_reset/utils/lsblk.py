import re
import subprocess
from pathlib import Path

from password_reset.schemes import Partition
from typing import List


def _lsblk() -> List[str]:
    cmd = (
        "lsblk",
        "-Pnpo",
        "name,fstype,mountpoints,type",
    )

    return subprocess.check_output(cmd).decode("utf-8").splitlines()


def get_partitions() -> List[Partition]:
    pattern = r'NAME="(.*?)" FSTYPE="(.*?)" MOUNTPOINTS="(.*?)"'

    partitions: List[Partition] = []

    for line in _lsblk():
        if "part" not in line:
            continue

        path, fs_type, is_mounted = re.search(pattern, line).groups()
        partitions.append(
            Partition(
                path=Path(path),
                fs_type=fs_type,
                is_mounted=bool(is_mounted),
            )
        )

    return partitions
