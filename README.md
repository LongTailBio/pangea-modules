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

Ex. Kraken

```sh
$ cd modules/kraken/
$ python setup.py bdist_wheel --universal
$ python setup.py bdist_wheel upload -r longtailbio
```

### Use Module

**Option 1:**

```sh
$ pip install -i https://pypi.longtailbio.com/simple pangea_modules.kraken
```

**Option 2:**

Create pip configuration file (e.g. `~/.pip/pip.conf`):

```
[global]
extra-index-url = https://pypi.longtailbio.com/simple/
```

Then call pip without the `-i` option:

```sh
$ pip install pangea_modules.kraken
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

For a single module (ex. Kraken):

```sh
$ python -m pytest --color=yes modules/kraken -s
```
