from setuptools import setup

microlib_name = 'pangea_modules.base'

requirements = ['numpy', 'pandas', 'mongoengine']

setup(
    name=microlib_name,
    version='0.1.2',
    author='Longtail Biotech',
    author_email='dev@longtailbio.com',
    description='Base types for PangeaModules to subclass.',
    license='Restricted',
    classifiers=[
        'Private :: Do Not Upload to pypi server',
    ],
    namespace_packages=['pangea_modules'],
    packages=[microlib_name, '{}.utils'.format(microlib_name)],
    install_requires=requirements,
)