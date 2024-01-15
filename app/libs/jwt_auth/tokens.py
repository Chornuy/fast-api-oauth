from uuid import uuid4

from datetime import timedelta, datetime
from jose import jwt, JOSEError

from app.core.security.jwt import ALGORITHM
from app.libs.utils.datetime import datetime_to_epoch, datetime_from_epoch
from app.settings.settings import settings


class Token:

    lifetime = None
    token_type = None
    leeway = 0
    jti_claim = "jti"
    secret_key = settings.SECRET_KEY
    algorithm = ALGORITHM
    token_claim = "token_type"

    def __init__(self, token=None):
        self.token = token
        self.current_time = datetime.utcnow()

        if token is not None:
            try:
                self.payload = self.decode(token)
            except JOSEError:
                raise Exception("Token is invalid or expired")

        else:
            # New token.  Skip all the verification steps.
            self.payload = {self.token_claim: self.token_type}

            # Set "exp" and "iat" claims with default value
            self.set_exp(from_time=self.current_time, lifetime=self.lifetime)
            self.set_iat(at_time=self.current_time)

            # Set "jti" claim
            self.set_jti()

    def __repr__(self):
        return repr(self.payload)

    def __getitem__(self, key):
        return self.payload[key]

    def __setitem__(self, key, value):
        self.payload[key] = value

    def __delitem__(self, key):
        del self.payload[key]

    def __contains__(self, key):
        return key in self.payload

    def __str__(self):
        return self.encode(self.payload)

    def get(self, key, default=None):
        return self.payload.get(key, default)

    def set_jti(self):
        """
        Populates the configured jti claim of a token with a string where there
        is a negligible probability that the same string will be chosen at a
        later time.

        See here:
        https://tools.ietf.org/html/rfc7519#section-4.1.7
        """
        self.payload[self.jti_claim] = uuid4().hex

    def set_exp(self, claim="exp", from_time=None, lifetime=None):
        """
        Updates the expiration time of a token.

        See here:
        https://tools.ietf.org/html/rfc7519#section-4.1.4
        """
        if from_time is None:
            from_time = self.current_time

        if lifetime is None:
            lifetime = self.lifetime

        self.payload[claim] = datetime_to_epoch(from_time + lifetime)

    def set_iat(self, claim="iat", at_time=None):
        """
        Updates the time at which the token was issued.

        See here:
        https://tools.ietf.org/html/rfc7519#section-4.1.6
        """
        if at_time is None:
            at_time = self.current_time

        self.payload[claim] = datetime_to_epoch(at_time)

    def check_exp(self, claim="exp", current_time=None):
        """
        Checks whether a timestamp value in the given claim has passed (since
        the given datetime value in `current_time`).  Raises a TokenError with
        a user-facing error message if so.
        """
        if current_time is None:
            current_time = self.current_time

        try:
            claim_value = self.payload[claim]
        except KeyError:
            raise Exception(f"Token has no '{claim}' claim")

        claim_time = datetime_from_epoch(claim_value)
        leeway = self.leeway
        if claim_time <= current_time - leeway:
            raise Exception(f"Token '{claim}' claim has expired")

    def decode(self, token: str) -> dict:
        return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])

    def encode(self, data: dict) -> str:
        return jwt.encode(data, self.secret_key, algorithm=self.algorithm)


class AccessToken(Token):

    token_type = "access"
    lifetime = timedelta(minutes=30)


class RefreshToken(Token):

    token_type = "refresh"
    lifetime = timedelta(days=30)
    access_token_class = AccessToken

    no_copy_claims = (
        Token.token_claim,
        "exp",
        # Both of these claims are included even though they may be the same.
        # It seems possible that a third party token might have a custom or
        # namespaced JTI claim as well as a default "jti" claim.  In that case,
        # we wouldn't want to copy either one.
        Token.jti_claim,
        "jti",
    )

    @property
    def access_token(self):
        """
        Returns an access token created from this refresh token.  Copies all
        claims present in this refresh token to the new access token except
        those claims listed in the `no_copy_claims` attribute.
        """
        access = self.access_token_class()

        # Use instantiation time of refresh token as relative timestamp for
        # access token "exp" claim.  This ensures that both a refresh and
        # access token expire relative to the same time if they are created as
        # a pair.
        access.set_exp(from_time=self.current_time)

        no_copy = self.no_copy_claims
        for claim, value in self.payload.items():
            if claim in no_copy:
                continue
            access[claim] = value

        return access


class UntypedToken(Token):
    token_type = "untyped"
    lifetime = timedelta(seconds=0)

    def verify_token_type(self):
        """
        Untyped tokens do not verify the "token_type" claim.  This is useful
        when performing general validation of a token's signature and other
        properties which do not relate to the token's intended use.
        """
        pass
