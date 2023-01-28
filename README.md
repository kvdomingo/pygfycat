# gpycat
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/gpycat?style=for-the-badge)
![GitHub](https://img.shields.io/github/license/kvdomingo/pygfycat?style=for-the-badge)
![GitHub release (latest SemVer including pre-releases)](https://img.shields.io/github/v/release/kvdomingo/pygfycat?include_prereleases&style=for-the-badge)

![](./coverage.svg)

This is a WIP unofficial Python wrapper for the Gfycat web API.

## Installation
```shell
# Using pip
pip install gpycat

# OR

# Using poetry
poetry add gpycat
```

## Usage

```python
from gpycat import gpycat

# Import your client ID/secret from environment variables

gpycat.auth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
item = gpycat.get_gfycat("zestycreepyasiaticlesserfreshwaterclam")
```

Output:
```shell
> GfyItem(title="...", description="...", avgColor="...", content_urls={...}, ...)
```
