from setuptools import setup

microlib_name = 'pangea_modules.humann2'

requirements = ['pangea_modules.base', 'mongoengine']

setup(
    name=microlib_name,
    version='0.1.0',
    author='Longtail Biotech',
    author_email='dev@longtailbio.com',
    description=('HUMAnN2 is the next generation of HUMAnN '
                 '(HMP Unified Metabolic Analysis Network).'),
    license='Restricted',
    classifiers=[
        'Private :: Do Not Upload to pypi server',
    ],
    namespace_packages=['pangea_modules'],
    packages=[microlib_name],
    install_requires=requirements,
)
