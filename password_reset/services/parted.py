import os
import re
import subprocess
import sys
from pathlib import Path
from typing import List, Optional

from password_reset.enums import FSType
from password_reset.schemes import Partition


class Parted:
    mounted_parts: List[Partition] = []

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

    def _activate_lvm(self) -> Path:
        pattern = r'Fonud volume group "(.*)" using metadata type lvm2'
        lvm_volumes = subprocess.check_output(("vgscan",)).decode("utf-8")
        for lvm in re.search(pattern, lvm_volumes).groups():
            subprocess.call(("vgchange", "-ay", lvm))
        lvm_partitions = (
            subprocess.check_output(
                (
                    "lvdisplay",
                    "-C",
                    "-o",
                    "lv_name,lv_size",
                    "--noheadings",
                )
            )
            .decode("utf-8")
            .splitlines()
        )

        for name, path in map(lambda l: l.split(), lvm_partitions):
            print(f"Fonud LVM2 member {name} on {path}")
            if name.strip() == "root":
                return Path(path.strip())

        if len(lvm_partitions) > 0:
            return Path(lvm_partitions[0].split()[1].strip())

        return Path()

    def mount(self, part: Partition) -> Path:
        mount_point = self._base / part.path.parts[-1]
        self._mkdir(mount_point)

        device = part.path

        if part.fs_type == FSType.LVM2_MEMBER:
            device = self._activate_lvm()
            part.device = device

        exit_code = subprocess.call(
            (
                "mount",
                device,
                mount_point,
            )
        )
        if exit_code == 0:
            self.mounted_parts.append(part)

        return mount_point

    def umount(
        self,
        part: Partition,
        mount_path: Optional[Path] = None,
    ) -> None:
        device = part.device if part.fs_type == FSType.LVM2_MEMBER else part.path
        exit_code = subprocess.call(("umount", device))

        if mount_path is not None:
            os.rmdir(mount_path)

        if exit_code == 0 and part in self.mounted_parts:
            self.mounted_parts.remove(part)
