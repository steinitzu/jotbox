class JotboxError(Exception):
    pass


class JWTDecodeError(JotboxError):
    pass


class TokenVerificationError(JotboxError):
    pass


class RevokedTokenError(TokenVerificationError):
    pass
