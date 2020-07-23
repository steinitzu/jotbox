`Jotbox` can be configured with the following arguments

* **`encode_key`**

    **Required**

    This key is used to sign your JWTs. It is also used to verify them (unless a separate `decode_key` is specified)

    You should use a strong randomly generated string for this and store it securely.

* **`decode_key`**

    Default: `encode_key`

    When specified this token is used to decode your JWTs. (for use with asymmetric signing algorithms)

* **`payload_type`**

    Default: `jotbox.Payload`

    This is the model that is used for creating token payloads. You can subclass and add extra fields that you want encoded in the token.

    The default payload has the following standard claims: `jti`, `iat`, `exp` (optional)

* **`encode_algorithm`**

    Default: `"HS512"`

    Algorithm used to sign JWTs. This can be any algorithm supported by PyJWT.

* **`decode_algorithms`**

    Default: `["HS512", ]`

    A list of algorithms that are accepted when decoding tokens. Any algorithms supported by PyJWT
    are accepted.

* **`leeway`**

    Default: `0` (no leeway)

    Number of seconds of leeway to allow when verifying things 
    like expiry times and idle timeouts.  
    It can be good to set this to a few seconds to account for clock skew.

* **`expires_in`**

    Default: `None` (no expiry)

    Number of seconds of how long new tokens are valid for. By default tokens never expire.
    
    The expiry time is encoded in the JWT as `exp` claim.

* **`idle_timeout`**

    Default: `None` (no idle timeout)

    Number of seconds before a token is deleted from whitelist due to inactivity.
    This can only be used when [whitelist](./whitelist.md) is provided.

* **`whitelist`**

    Default: `None`

    An instance of `jotbox.whitelist.base.Whitelist` use as a storage backend for whitelisted tokens.
    Whitelisting is disabled when not provided.


* **`jwt_options`**

    Default: `{}` (default pyjwt options)

    Dict of options forwarded to `PyJWT.decode` when verifying tokens.
