import subprocess
from pathlib import Path

from .crypt import shadow_password


def is_linux_partition(mount_path: Path) -> bool:
    passwd_file = mount_path / "etc/passwd"
    return passwd_file.is_file()


def is_windows_partition(mount_path: Path) -> bool:
    windows_dir = mount_path / "Windows"
    return windows_dir.is_dir()


def change_linux_password(
    password: str,
    username="root",
) -> int:
    new_password = shadow_password(password)
    return subprocess.call(
        (
            "usermod",
            "--password",
            new_password,
            username,
        )
    )
