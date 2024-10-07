import requests
from marzban.add_user import body
from marzban.constants import URL


class Marzban:
    @classmethod
    async def create_user(cls, username: str, user_id: str, data_limit, expire_duration):
        request_body = body(username, user_id, data_limit, expire_duration)
        response = requests.post(f"{URL}/api/user", json=request_body)
        data = response.json()
        return data.subscription_url
