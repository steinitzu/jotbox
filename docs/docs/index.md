# Jotbox

`Jotbox` is a library for generating and verifying JWTs in python

It provides a common interface for working with purely 
stateless JWTs or revokable tokens stored in a central whitelist.

## Features

* All JWT encoding and decoding is done using the de-facto standard [PyJWT](https://pyjwt.readthedocs.io) under the hood
* Optional JWT whitelist for revokable tokens (pluggable storage backend)
* Redis whitelist support is built in using [aredis](https://aredis.readthedocs.io/en/latest/)
* Optional idle timeout support to revoke tokens that are not accessed for a given interval
* Type safe, using generics for an extendable JWT payload model


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
