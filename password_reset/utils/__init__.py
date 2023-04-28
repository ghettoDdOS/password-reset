from .crypt import shadow_password
from .lsblk import get_partitions
from .os import change_linux_password, is_linux_partition, is_windows_partition

__all__ = (
    "get_partitions",
    "is_linux_partition",
    "is_windows_partition",
    "shadow_password",
    "change_linux_password",
)
