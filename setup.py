#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools

if __name__ == '__main__':
    package_name = 'adhoc_slcsp'

    description = 'Solution to the Ad Hoc "slcsp" problem.'

    with open('./COMMENTS.md', 'r') as file:
        long_description = file.read()

    install_requires = [
        # This package is needed by the application layer for its
        # primitive NaN type.
        'numpy==1.13.3',
        # This package is needed by the application layer to implement
        # data IO and pipelines.
        'pandas==0.21.0']

    setuptools.setup(name=package_name,
                     version='0.1.0',
                     description=description,
                     long_description=long_description,
                     url='https://github.com/dnguyen0304/adhoc_slcsp.git',
                     author='Duy Nguyen',
                     author_email='dnguyen0304@gmail.com',
                     license='MIT',
                     classifiers=['Programming Language :: Python :: 3.6'],
                     packages=setuptools.find_packages(exclude=['*.tests']),
                     install_requires=install_requires,
                     test_suite='nose.collector',
                     tests_require=['nose'],
                     include_package_data=True)
