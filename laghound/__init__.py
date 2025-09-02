__version__ = "0.1.0"

from collections import namedtuple

VersionInfo = namedtuple("VersionInfo", "major minor micro releaselevel serial")
version_info = VersionInfo(major=0, minor=1, micro=0, releaselevel="beta", serial=0)
