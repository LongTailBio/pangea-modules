from setuptools import setup

microlib_name = 'pangea_modules.metaphlan2_data'

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
    description='Metaphlan2 tool.',
    license='Restricted',
    classifiers=[
        'Private :: Do Not Upload to pypi server',
    ],
    namespace_packages=['pangea_modules'],
    packages=[microlib_name],
    install_requires=requirements,
)
