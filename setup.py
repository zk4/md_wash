# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from pathlib import Path

versionfile = Path("./version")
version = versionfile.read_text()
[mainv,modulev,minorv] = version.split(".")

VERSION = (int(mainv), int(modulev), int(minorv))
__version__ = '.'.join(map(str, VERSION[0:3]))
__description__ = '''this is a description'''
__author__ = 'zk'
__author_email__ = 'liuzq7@gmail.com'
__homepage__ = 'https://github.com/zk4/md_wash'
__download_url__ = '%s/archive/master.zip' % __homepage__
__license__ = 'BSD'

if __name__ == '__main__':
    setup(
        # used in pip install and uninstall 
        # pip install md_wash
        name='md_wash',
        version=__version__,
        author=__author__,
        author_email=__author_email__,
        url=__homepage__,
        description=__description__,
        long_description=open('README.md', 'r', encoding='utf-8').read().strip(),
        long_description_content_type='text/markdown',
        download_url=__download_url__,
        license=__license__,
        python_requires='>3.0.0',
        zip_safe=False,
        packages=find_packages(exclude=['tests', 'tests.*']),
        package_data={'md_wash.logx': ['logging.yaml']},
        install_requires=open('requirements.txt', 'r').read().strip().split(),
        entry_points={
            'console_scripts': [
                'md_wash = md_wash:entry_point'
            ]
        },
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Environment :: Console'
        ],
        keywords=(
            'best practice for python project'
        )
    )
