#!/usr/bin/env python

import os, sys
import glob
from distutils.core import setup

MOD_NAME = 'mic'

try:
    import mic
    version = mic.__version__
except (ImportError, AttributeError):
    version = "dev"

# --install-layout is recognized after 2.5
if sys.version_info[:2] > (2, 5):
    if len(sys.argv) > 1 and 'install' in sys.argv:
        try:
            import platform
            (dist, ver, id) = platform.linux_distribution()

            # for debian-like distros, mods will be installed to
            # ${PYTHONLIB}/dist-packages
            if dist in ('debian', 'Ubuntu'):
                sys.argv.append('--install-layout=deb')
        except:
            pass

PACKAGES = [MOD_NAME,
            MOD_NAME + '/utils',
            MOD_NAME + '/imager',
            MOD_NAME + '/kickstart',
            MOD_NAME + '/kickstart/custom_commands',
            MOD_NAME + '/3rdparty/pykickstart',
            MOD_NAME + '/3rdparty/pykickstart/commands',
            MOD_NAME + '/3rdparty/pykickstart/handlers',
            MOD_NAME + '/3rdparty/pykickstart/urlgrabber',
           ]

IMAGER_PLUGINS = glob.glob(os.path.join("plugins", "imager", "*.py"))
BACKEND_PLUGINS = glob.glob(os.path.join("plugins", "backend", "*.py"))

prefix = sys.prefix
# if real_prefix, it must be in virtualenv, use prefix as root
root = sys.prefix if hasattr(sys, 'real_prefix') else ''

conffile = 'etc/mic.conf'
# apply prefix to mic.conf.in to generate actual mic.conf
conf_str = file('etc/mic.conf.in').read()
conf_str = conf_str.replace('@PREFIX@', prefix)
with file(conffile, 'w') as wf:
    wf.write(conf_str)

setup(name=MOD_NAME,
  version = version,
  description = 'Image Creator for Linux Distributions',
  author='Jian-feng Ding, Qiang Zhang, Gui Chen',
  author_email='jian-feng.ding@intel.com, qiang.z.zhang@intel.com, gui.chen@intel.com',
  url='https://github.com/01org/mic',
  scripts=[
      'tools/mic',
      ],
  packages = PACKAGES,
  data_files = [("%s/lib/mic/plugins/imager" % prefix, IMAGER_PLUGINS),
                ("%s/lib/mic/plugins/backend" % prefix, BACKEND_PLUGINS),
                ("%s/etc/mic" % root, [conffile])]
)
