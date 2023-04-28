import os

from password_reset.enums import FSType, UnixFSTypes, WindowsFSTypes
from password_reset.services import Parted
from password_reset.utils import (
    change_linux_password,
    get_partitions,
    is_linux_partition,
    is_windows_partition,
)


def main():
    parted = Parted()
    input_username = os.getenv("PASSWORD_RESET_USERNAME", None)
    new_password = os.getenv("PASSWORD_RESET_PASSWORD", "87654321")

    for partition in get_partitions():
        if partition.is_mounted:
            print(f"Device {partition.path} already mounted")
            continue
        if partition.fs_type is FSType.UNKNOWN:
            print(f"Device {partition.path} has unsupported file system")
            continue

        if partition.fs_type in UnixFSTypes:
            print(f"Device {partition.path} has Linux file system")
            mount_path = parted.mount(partition)

            if is_linux_partition(mount_path):
                print("Found Linux Partition")
                username = input_username or "root"
                exit_code = change_linux_password(new_password, username)
                if exit_code == 0:
                    print(
                        f"Changed password for {username} ",
                        f"on {partition.path}",
                    )

            parted.umount(partition, mount_path)
        elif partition.fs_type in WindowsFSTypes:
            print(f"Device {partition.path} has Windows file system")
            mount_path = parted.mount(partition)

            if is_windows_partition(mount_path):
                print("Found Windows Partition")

            parted.umount(partition, mount_path)


if __name__ == "__main__":
    main()
