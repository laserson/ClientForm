#!/usr/bin/env python
"""Client-side HTML form handling.

ClientForm is a Python module for handling HTML forms on the client
side, useful for parsing HTML forms, filling them in and returning the
completed forms to the server.  It developed from a port of Gisle Aas'
Perl module HTML::Form, from the libwww-perl library, but the
interface is not the same.
"""

try: True
except NameError:
    False, True = 0, 1

import re
#VERSION_MATCH = re.search(r'VERSION = "(.*)"', open("ClientForm.py").read())
#VERSION = VERSION_MATCH.group(1)
VERSION = '0.2.10'
INSTALL_REQUIRES = []
NAME = "ClientForm"
PACKAGE = False
LICENSE = "BSD"  # or ZPL 2.1
PLATFORMS = ["any"]
ZIP_SAFE = True
CLASSIFIERS = """\
Development Status :: 5 - Production/Stable
Intended Audience :: Developers
Intended Audience :: System Administrators
License :: OSI Approved :: BSD License
License :: OSI Approved :: Zope Public License
Natural Language :: English
Operating System :: OS Independent
Programming Language :: Python
Programming Language :: Python :: 2
Programming Language :: Python :: 2.3
Programming Language :: Python :: 2.4
Programming Language :: Python :: 2.5
Programming Language :: Python :: 2.6
Topic :: Internet
Topic :: Internet :: WWW/HTTP
Topic :: Internet :: WWW/HTTP :: Site Management
Topic :: Internet :: WWW/HTTP :: Site Management :: Link Checking
Topic :: Software Development :: Libraries
Topic :: Software Development :: Libraries :: Python Modules
Topic :: Software Development :: Testing
Topic :: Software Development :: Testing :: Traffic Generation
Topic :: System :: Networking :: Monitoring
Topic :: System :: Systems Administration
Topic :: Text Processing
Topic :: Text Processing :: Markup
Topic :: Text Processing :: Markup :: HTML
Topic :: Text Processing :: Markup :: XML
"""

#-------------------------------------------------------
# the rest is constant for most of my released packages:

import sys

if PACKAGE:
    packages, py_modules = [NAME], None
else:
    packages, py_modules = None, [NAME]

doclines = __doc__.split("\n")

if not hasattr(sys, "version_info") or sys.version_info < (2, 3):
    from distutils.core import setup
    _setup = setup
    def setup(**kwargs):
        ignore_keys = [
            # distutils >= Python 2.3 args
            # XXX probably download_url came in earlier than 2.3
            "classifiers", "download_url",
            # setuptools args
            "install_requires", "zip_safe", "test_suite",
            ]
        if sys.version_info < (2, 1):
            ignore_keys.append("platforms")
        for key in ignore_keys:
            if kwargs.has_key(key):
                del kwargs[key]
        # Only want packages keyword if this is a package,
        # only want py_modules keyword if this is a single-file module,
        # so get rid of packages or py_modules keyword as appropriate.
        if kwargs["packages"] is None:
            del kwargs["packages"]
        else:
            del kwargs["py_modules"]
        apply(_setup, (), kwargs)
else:
    import ez_setup
    ez_setup.use_setuptools()
    from setuptools import setup

setup(
    name = NAME,
    version = VERSION,
    license = LICENSE,
    platforms = PLATFORMS,
    classifiers = [c for c in CLASSIFIERS.split("\n") if c],
    install_requires = INSTALL_REQUIRES,
    zip_safe = ZIP_SAFE,
    test_suite = "test",
    author = "John J. Lee",
    author_email = "jjl@pobox.com",
    description = doclines[0],
    long_description = "\n".join(doclines[2:]),
    url = "http://wwwsearch.sourceforge.net/%s/" % NAME,
    download_url = ("http://wwwsearch.sourceforge.net/%s/src/"
                    "%s-%s.tar.gz" % (NAME, NAME, VERSION)),
    py_modules = py_modules,
    packages = packages,
    )
