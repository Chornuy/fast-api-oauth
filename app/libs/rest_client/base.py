import httpx
from httpx import Auth


class BaseAsyncClient:

    def __init__(self, service_host: str, timeout: int = 60, auth: Auth | None = None, encoder = None):
        self.timeout = timeout
        self.auth = auth
        self.encoder = encoder
        self.service_host = service_host

    async def request(self, method: str, url: str, params: dict | None = None, **kwargs):
        pass



class UserRestClient(BaseAsyncClient):

    def __init__(self, base_host: str = "http://localhost:8000"):
        super().__init__(base_host)


user_client = UserRestClient(base_host="localhost")

async def test_sandbox():
    filters = {
        "active": True,
        "created_at__gte": "2023-01-01"
    }

    sorting = {
        "field": "created_at",
        "order": "desc"
    }

    pagination = {
        "size": 10
    }
    user_list = await user_client.get_user_list(filters, sorting, pagination)
    for user in user_list:
        print(user)

    data = {
        "active": False
    }
    user_client.update_user(id=10, data=data)
