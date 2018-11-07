from setuptools import setup

microlib_name = 'pangea_modules.top_taxa'

requirements = [
    'mongoengine',
    'pangea_modules.base',
    'pangea_modules.krakenhll_data',
    'pangea_modules.metaphlan2_data',
]

setup(
    name=microlib_name,
    version='0.1.0',
    author='Longtail Biotech',
    author_email='dev@longtailbio.com',
    description=('This plot shows the top taxa across different metadata '
                 'groups and kingdoms.'),
    license='Restricted',
    classifiers=[
        'Private :: Do Not Upload to pypi server',
    ],
    namespace_packages=['pangea_modules'],
    packages=[microlib_name],
    install_requires=requirements,
)
