from typing import Any

from app.libs.oauth_flow.exceptions import (
    GrantTypeKeyNotFoundError,
    NoMethodForGrantTypeFoundError,
    NotSupportedGrantTypeFlowError,
)


class BaseOauthFlowManager:
    grant_type_key = "grant_type"

    supported_grant_types = []

    async def process_flow(self, **kwargs) -> Any:
        """

        Args:
            **kwargs:

        Returns:

        """
        grant_type = kwargs.pop(self.grant_type_key)

        if not grant_type:
            raise GrantTypeKeyNotFoundError(f"Key: {self.grant_type_key} was not path to method") from None

        if grant_type not in self.supported_grant_types:
            raise NotSupportedGrantTypeFlowError("Grant type not supported") from None

        grant_type_method = getattr(self, grant_type)

        if not grant_type_method:
            raise NoMethodForGrantTypeFoundError(
                f"Method for grant_type: {grant_type} was found in class {self.__class__.__name__}"
            ) from None

        return await grant_type_method(**kwargs)
