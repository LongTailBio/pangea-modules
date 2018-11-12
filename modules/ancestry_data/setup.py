from setuptools import setup

microlib_name = 'pangea_modules.ancestry_data'

requirements = [
    'pangea_modules.base',
    'pangea_modeuls.base.data_tensor_models',
    'mongoengine',
]

setup(
    name=microlib_name,
    version='0.1.2',
    author='Longtail Biotech',
    author_email='dev@longtailbio.com',
    description='Data for Human Ancestry.',
    license='Restricted',
    classifiers=[
        'Private :: Do Not Upload to pypi server',
    ],
    namespace_packages=['pangea_modules'],
    packages=[microlib_name],
    install_requires=requirements,
)
