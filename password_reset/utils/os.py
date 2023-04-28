import subprocess
from pathlib import Path
from typing import List

from .crypt import shadow_password


def is_linux_partition(mount_path: Path) -> bool:
    passwd_file = mount_path / "etc/passwd"
    return passwd_file.is_file()


def is_windows_partition(mount_path: Path) -> bool:
    windows_dir = mount_path / "Windows"
    return windows_dir.is_dir()


def run_in_chroot(root: Path, cmd: List[str]) -> int:
    return subprocess.call(("chroot", root, *cmd))


def change_linux_password(
    chroot: Path,
    password: str,
    username="ghettoddos",
) -> int:
    new_password = shadow_password(password)
    return run_in_chroot(
        chroot,
        (
            "usermod",
            "--password",
            new_password,
            username,
        ),
    )
