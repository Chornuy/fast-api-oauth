from typing import Any

from app.libs.oauth_flow.exceptions import GrantTypeKeyNotFound, NotSupportedGrantTypeFlow, NoMethodForGrantTypeFound


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
            raise GrantTypeKeyNotFound(f"Key: {self.grant_type_key} was not path to method")

        if grant_type not in self.supported_grant_types:
            raise NotSupportedGrantTypeFlow("Grant type not supported")

        grant_type_method = getattr(self, grant_type)

        if not grant_type_method:
            raise NoMethodForGrantTypeFound(
                f"Method for grant_type: {grant_type} was found in class {self.__class__.__name__}"
            )

        return await grant_type_method(**kwargs)
