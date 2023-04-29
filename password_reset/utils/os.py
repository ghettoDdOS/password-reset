import subprocess
from pathlib import Path
from typing import List

from .crypt import shadow_password


def is_linux_partition(mount_path: Path) -> (bool, bool):
    passwd_file = mount_path / "etc/passwd"
    one_part_os_passwd_file = mount_path / "@/etc/passwd"
    return (
        passwd_file.is_file() or one_part_os_passwd_file.is_file(),
        one_part_os_passwd_file.is_file(),
    )


def is_windows_partition(mount_path: Path) -> bool:
    windows_dir = mount_path / "Windows"
    return windows_dir.is_dir()


def run_in_chroot(root: Path, cmd: List[str]) -> int:
    return subprocess.call(("chroot", root, *cmd))


def change_linux_password(
    chroot: Path,
    password: str,
    username="root",
) -> int:
    new_password = shadow_password(password)
    return run_in_chroot(
        chroot,
        (
            "/sbin/usermod",
            "--password",
            new_password,
            username,
        ),
    )

def permit_login_root(chroot: Path) -> int:
    return run_in_chroot(
        chroot,
        (
            "/usr/bin/sed",
            "-i",
            "s/PermitRootLogin .*/PermitRootLogin yes/g",
            "/etc/ssh/sshd_config",
        ),
    )
