class JotboxError(Exception):
    pass


class JWTDecodeError(JotboxError):
    pass


class RevokedTokenError(JWTDecodeError):
    pass
