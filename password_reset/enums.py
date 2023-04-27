from enum import Enum


class FSType(str, Enum):
    EXT3 = "ext3"
    EXT4 = "ext4"
    NTFS = "ntfs"
    BTRFS = "btrfs"


class SystemType(str, Enum):
    UNIX = "unix"
    WINDOWS = "windows"
    UNKNOWN = "unknown"


UnixFSTypes = (
    FSType.EXT3,
    FSType.EXT4,
    FSType.BTRFS,
)

WindowsFSTypes = (FSType.NTFS,)
