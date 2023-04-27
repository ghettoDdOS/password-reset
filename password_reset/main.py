from password_reset.enums import UnixFSTypes, WindowsFSTypes
from password_reset.services import Parted
from password_reset.utils import get_partitions


def main():
    parted = Parted()

    for partition in get_partitions():
        if partition.fs_type in UnixFSTypes:
            print(f"Device {partition.path} has Linux file system")
            mount_path = parted.mount(partition)

            passwd_file = mount_path / "etc/passwd"
            if passwd_file.is_file():
                print("Found Linux Partition")

            parted.umount(partition, mount_path)
        elif partition.fs_type in WindowsFSTypes:
            print(f"Device {partition.path} has Windows file system")
            mount_path = parted.mount(partition)

            windows_dir = mount_path / "Windows"
            if windows_dir.is_dir():
                print("Found Windows Partition")

            parted.umount(partition, mount_path)
        else:
            print(f"Device {partition.path} has unsupported file system")
