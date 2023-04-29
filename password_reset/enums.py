from enum import Enum


class FSType(str, Enum):
    EXT3 = "ext3"
    EXT4 = "ext4"
    NTFS = "ntfs"
    BTRFS = "btrfs"
    LVM2_MEMBER = "LVM2_member"
    UNKNOWN = "unknown"

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN


class SystemType(str, Enum):
    UNIX = "unix"
    WINDOWS = "windows"
    UNKNOWN = "unknown"


UnixFSTypes = (
    FSType.EXT3,
    FSType.EXT4,
    FSType.BTRFS,
    FSType.LVM2_MEMBER,
)

WindowsFSTypes = (FSType.NTFS,)
