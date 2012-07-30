from setuptools import setup, find_packages

VERSION = '0.0.1-dev'

LONG_DESCRIPTION = open('README.rst').read()

setup(name='dploy-git',
    version=VERSION,
    description="dploy-git",
    long_description=LONG_DESCRIPTION,
    keywords='git',
    author='Reuven V. Gonzales',
    author_email='reuven@tobetter.us',
    url="https://github.com/ravenac95/dploy-git",
    license='MIT',
    platforms='Ubuntu',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'subwrap',
    ],
    entry_points={},
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Operating System :: POSIX',
        'Topic :: Software Development :: Build Tools',
    ],
)
