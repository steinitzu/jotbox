# JotBox

JotBox is an extended JWT toolkit for python.

## Features

- [x] Type safety
- [x] Secure JWT encoding and decoding using [PyJWT](https://pyjwt.readthedocs.io)
- [x] Optional token [whitelist](whitelist-and-revoke-tokens) with pluggable storage backends (redis backend included)
- [x] Idle timeout support (with whitelist)

## Install

```
pip install jotbox
```

To use the included redis whitelist, you must install `aredis` as well:

```
pip install aredis
```

## Quickstart

```python3
{!../examples/quickstart.py!}
```

See all possible settings in the [configuration](config) section
