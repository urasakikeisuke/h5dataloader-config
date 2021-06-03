# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='h5dataloader_config',
    version='1.0.0',
    description='`https://github.com/shikishima-TasakiLab/h5dataloader-config`',
    long_description='`https://github.com/shikishima-TasakiLab/h5dataloader-config`',
    author='Junya Shikishima',
    author_email='160442065@ccalumni.meijo-u.ac.jp',
    url='https://github.com/shikishima-TasakiLab/h5dataloader-config',
    license='',
    packages=find_packages(),
    install_requires=[
        "numpy", "h5py==2.10.0", "PySide2"
    ],
    entry_points={
        'console_scripts': [
            'h5dataloader-config = h5dataloader_config:main',
        ]
    },
    python_requires='>=3.6'
)