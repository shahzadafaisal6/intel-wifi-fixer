from setuptools import setup, find_packages
import os
import glob

# Include data files
data_files = [
    ('data', glob.glob('data/*')),
]

setup(
    name='intel-wifi-fixer',
    version='1.0.0',
    author='Intel WiFi Fixer Team',
    author_email='support@intelwififixer.example.com',
    description='A comprehensive tool to diagnose and fix issues with the Intel Centrino Advanced-N 6205 wireless adapter.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/shahzadafaisal6/intel-wifi-fixer',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    data_files=data_files,
    install_requires=[
        'pyyaml>=5.4.1',
        'jsonschema>=3.2.0',
    ],
    entry_points={
        'console_scripts': [
            'intel-wifi-fixer=src.main:main_menu',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: System Administrators',
        'Intended Audience :: End Users/Desktop',
        'Topic :: System :: Networking',
        'Topic :: Utilities',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
    ],
    python_requires='>=3.6',
    keywords='wifi network troubleshooting intel centrino',
)