#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools

setuptools
setuptools.setup(
    name='pangea_modules',
    version='0.1.0',
    description="Pangea Modules and Pipelines",
    author="Longtail Biotech",
    author_email='dev@longtailbio.com',
    url='https://github.com/longtailbio/pangea_modules',
    packages=setuptools.find_packages(),
    package_dir={'pangea_modules': 'pangea_modules'},
    install_requires=[
        'click',
        'luigi',
    ],
    entry_points={
        'console_scripts': [
            'pangea_modules=pangea_modules.cli:main'
        ]
    },
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
    ],
)
