from setuptools import setup

microlib_name = 'pangea_modules.ancestry'

requirements = ['pangea_modules.base', 'pangea_modules.ancestry_data', 'mongoengine']

setup(
    name=microlib_name,
    version='0.1.0',
    author='Longtail Biotech',
    author_email='dev@longtailbio.com',
    description='Human ancestry.',
    license='Restricted',
    classifiers=[
        'Private :: Do Not Upload to pypi server',
    ],
    namespace_packages=['pangea_modules'],
    packages=[microlib_name],
    install_requires=requirements,
)