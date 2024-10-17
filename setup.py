from setuptools import setup, find_packages

setup(
    name='mgt_downloader',
    version='0.1.1',
    description='A script to download torrents using Real Debrid',
    author='Cesar Garcia',
    author_email='celord@gmail.com',
    url='https://github.com/celord/mgt_downloader',
    packages=find_packages(),
    install_requires=[
        'requests',
        'tomllib; python_version<"3.11"',
        'curlify',
    ],
    entry_points={
        'console_scripts': [
            'mgt_downloader=mgt_dowloader:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)