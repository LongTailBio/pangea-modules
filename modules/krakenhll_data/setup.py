from setuptools import setup

microlib_name = 'pangea_modules.krakenhll_data'

requirements = ['pangea_modules.base', 'mongoengine']

setup(
    name=microlib_name,
    version='0.1.2',
    author='Longtail Biotech',
    author_email='dev@longtailbio.com',
    description='Raw data for KrakenHLL.',
    license='Restricted',
    classifiers=[
        'Private :: Do Not Upload to pypi server',
    ],
    namespace_packages=['pangea_modules'],
    packages=[microlib_name],
    install_requires=requirements,
)
