import json

from loguru import logger
from requests import Session

from .hooks import raise_if_not_ok
from .models import GfyItem

BASE_URL = "https://api.gfycat.com/v1"


class GfySession(Session):
    def post(self, *args, **kwargs):
        data = kwargs.get("data")
        if isinstance(data, dict):
            data = json.dumps(data)
            kwargs.update({"data": data})
        return super().post(*args, **kwargs)


def transform_gfyitem_content_url_keys(gfyitem: dict):
    transform = {
        **gfyitem,
        "content_urls": {
            **gfyitem["content_urls"],
            "gif100px": gfyitem["content_urls"]["100pxGif"],
        },
    }
    return transform


class Gfycat:
    client_id: str = ""
    client_secret: str = ""
    credentials: dict[str, str | int] = {}
    last_request_status: int = None
    session = GfySession()
    session.hooks.update({"response": raise_if_not_ok})

    def auth(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        res = self.session.post(
            f"{BASE_URL}/oauth/token",
            data={
                "grant_type": "client_credentials",
                "client_id": client_id,
                "client_secret": client_secret,
            },
        )
        self.last_request_status = res.status_code
        data = res.json()
        self.credentials = data
        self.session.headers.update(
            {"Authorization": f"{self.credentials['token_type']} {self.credentials['access_token']}"}
        )
        logger.info("Logged in.")

    def get_gfycat(self, gfyid: str):
        res = self.session.get(f"{BASE_URL}/gfycats/{gfyid}")
        data = res.json()
        return GfyItem(**transform_gfyitem_content_url_keys(data["gfyItem"]))


gfycat = Gfycat()
