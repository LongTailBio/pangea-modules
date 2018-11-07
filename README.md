# pangea-modules

Core modules for use with Longtail Biotech\'s Pangea platform.

## Release

### Configure PyPI

```
# ~/.pypirc

[distutils]
index-servers =
    pypi
    longtailbio

[pypi]
username: whoever
password: whatever

[longtailbio]
repository: https://pypi.longtailbio.com
username: johndoe
password: topsecret
```

### Build and Publish Module

Ex. KrakenHLL

```sh
$ cd modules/krakenhll/
$ python setup.py bdist_wheel --universal
$ python setup.py bdist_wheel upload -r longtailbio
```

### Use Module

**Option 1:**

```sh
$ pip install -i https://pypi.longtailbio.com/simple pangea_modules.krakenhll
```

**Option 2:**

Create pip configuration file (e.g. `~/.pip/pip.conf`):

```
[global]
extra-index-url = https://pypi.longtailbio.com/simple/
```

Then call pip without the `-i` option:

```sh
$ pip install pangea_modules.krakenhll
```

## Testing

To run tests, activate a virtual environment and run:

```sh
$ pip install -e .
```

To run all tests:

```sh
$ python -m pytest --color=yes modules -s
```

For a single module (ex. KrakenHLL):

```sh
$ python -m pytest --color=yes modules/krakenhll -s
```

## Acknowledgments

Thanks to Christian Hettlage for his post on [setting up a pypi server](https://medium.com/@christianhettlage/setting-up-a-pypi-server-679f1b55b96).

Thanks to Jorge Herrera at Shazam for a [great writeup on Python microlibs](https://blog.shazam.com/python-microlibs-5be9461ad979).
