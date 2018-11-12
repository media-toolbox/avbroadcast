# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(name='avbroadcast',
      version='0.0.0',
      description='republish audio/video streams for mass consumption',
      long_description='republish audio/video streams for mass consumption',
      license="AGPL 3, EUPL 1.2",
      classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "License :: OSI Approved :: European Union Public Licence 1.2 (EUPL 1.2)",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Manufacturing",
        "Intended Audience :: Science/Research",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Telecommunications Industry",
        "Topic :: Communications",
        "Topic :: Internet",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        "Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator",
        "Topic :: Software Development :: Libraries",
        "Topic :: System :: Archiving",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Operating System :: MacOS"
      ],
      author='Andreas Motl',
      author_email='andreas.motl@elmyra.de',
      url='https://github.com/daq-tools/avbroadcast',
      keywords='audio video broadcast rtmp hls http ' +
               '',
      packages=find_packages(),
      include_package_data=True,
      package_data={
      },
      zip_safe=False,
      test_suite='avbroadcast.test',
      install_requires=[
          'docopt==0.6.2',
      ],
      dependency_links=[
      ],
      entry_points={
          'console_scripts': [
              'avbroadcast = avbroadcast.commands:run',
          ],
      },
)
