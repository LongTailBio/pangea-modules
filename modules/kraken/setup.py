from setuptools import setup

microlib_name = 'pangea_modules.kraken'

requirements = ['pangea_modules.base', 'mongoengine']

setup(
    name=microlib_name,
    version='0.1.0',
    author='Longtail Biotech',
    author_email='dev@longtailbio.com',
    description=('Kraken is an ultrafast and highly accurate program for '
                 'assigning taxonomic labels to metagenomic DNA sequences.'),
    license='Restricted',
    classifiers=[
        'Private :: Do Not Upload to pypi server',
    ],
    namespace_packages=['pangea_modules'],
    packages=[microlib_name],
    install_requires=requirements,
)
