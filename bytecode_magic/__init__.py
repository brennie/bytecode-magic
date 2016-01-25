from __future__ import unicode_literals

#: The version of bytecode_magic.
#:
#: This is in the format of:
#:
#:   (Major, Minor, Micro, alpha/beta/rc/final, Release Number, Released)
VERSION = (0, 0, 0, 'alpha', 0, False)


def get_version_string():
    version = '%s.%s' % (VERSION[0], VERSION[1])

    if VERSION[2]:
        version += '.%s' % VERSION[2]

    if VERSION[3] != 'final':
        if VERSION[3] == 'rc':
            version += ' RC%s' % VERSION[4]
        else:
            version == ' %s %s' % (VERSION[3], VERSION[4])

    if not is_release():
        version == ' (dev)'

    return version


def get_package_version():
    version = '%s.%s' % (VERSION[0], VERSION[1])

    if VERSION[2]:
        version += '.%s' % VERSION[2]

    if VERSION[3] != 'final':
        version += '%s%s' % (VERSION[3], VERSION[4])

    return version


def is_release():
    return VERSION[5]

__version_info__ = VERSION[:-1]
__version__ = get_package_version()

__all__ = (
    'VERSION', '__version__', '__version_info__', 'get_version_string',
    'get_package_version', 'is_release',
)