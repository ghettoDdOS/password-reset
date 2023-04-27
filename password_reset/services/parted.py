import os
import subprocess
import sys
from pathlib import Path

from password_reset.schemes import Partition


class Parted:
    mounted_parts: list[Partition] = []

    def __init__(self, base=Path("/mnt/password-reset/")):
        self._base = base
        self._mkdir(self._base)

    # def __del__(self):
    #     os.rmdir(self._base)
    #     for part in self.mounted_parts:
    #         self.umount(part)

    def _mkdir(self, path: Path) -> None:
        try:
            os.makedirs(path, exist_ok=True)
        except PermissionError:
            sys.exit("This script needs sudo rights")

    def mount(self, part: Partition) -> Path:
        mount_point = self._base / part.path.parts[-1]
        self._mkdir(mount_point)
        exit_code = subprocess.call(
            (
                "mount",
                part.path,
                mount_point,
            )
        )
        if exit_code == 0:
            self.mounted_parts.append(part)

        return mount_point

    def umount(self, part: Partition, mount_path: Path | None = None) -> None:
        exit_code = subprocess.call(("umount", part.path))

        if mount_path is not None:
            os.rmdir(mount_path)

        if exit_code == 0 and part in self.mounted_parts:
            self.mounted_parts.remove(part)
