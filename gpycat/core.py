import io
from os import PathLike
from pathlib import Path
from typing import Any, Literal

import requests.exceptions
from loguru import logger
from pydantic import AnyHttpUrl
from requests import Response
from requests.adapters import HTTPAdapter, Retry
from requests_toolbelt import MultipartEncoder

from .models import AlbumNode, GfyItem
from .session import GfySession

BASE_URL = "https://api.gfycat.com/v1"


class Gfycat:
    client_id: str = ""
    client_secret: str = ""
    username: str = ""
    password: str = ""
    credentials: dict[str, str | int] = {}
    last_request_status: int = None

    @staticmethod
    def _raise_if_not_ok(response: Response, *args, **kwargs):
        if not response.ok:
            logger.error(response.text)
            raise requests.exceptions.HTTPError(response.text)

    @staticmethod
    def _update_last_status(self, response: Response, *args, **kwargs):
        self.last_request_status = response.status_code

    @staticmethod
    def _refresh_on_expire(response: Response, *args, **kwargs):
        raise NotImplemented

    def __init__(self):
        self.session = GfySession()
        self.session.hooks.update(
            {
                "response": [
                    self._raise_if_not_ok,
                    lambda *args, **kwargs: self._update_last_status(self, *args, **kwargs),
                ]
            }
        )

    @staticmethod
    def transform_content_url_key(gfy_item: dict):
        return {
            **gfy_item,
            "content_urls": {
                **gfy_item["content_urls"],
                "gif100px": gfy_item["content_urls"]["100pxGif"],
            },
        }

    @staticmethod
    def transform_dashed_key(node: dict):
        for k, v in node.items():
            if "-" in k:
                undashed: list[str] = k.split("-")
                undashed = [u.capitalize() for i, u in enumerate(undashed) if i > 0]
                new_k = "".join(undashed)
                node[new_k] = v
                del node[k]
        return node

    def auth(
        self,
        *,
        client_id: str,
        client_secret: str,
        username: str = "",
        password: str = "",
        grant_type: Literal[
            "client_credentials", "password", "refresh", "convert_code", "provider_token"
        ] = "client_credentials",
    ):
        data = {
            "grant_type": grant_type,
            "client_id": client_id,
            "client_secret": client_secret,
        }
        if grant_type == "client_credentials":
            pass
        elif grant_type == "password":
            if not username:
                raise ValueError("Username is blank")
            if not password:
                raise ValueError("Password is blank")
            data.update({"username": username, "password": password})
        elif grant_type == "refresh":
            data.update({"refresh_token": self.credentials["refresh_token"]})
        else:
            raise NotImplemented
        self.client_id = client_id
        self.client_secret = client_secret

        res = self.session.post(f"{BASE_URL}/oauth/token", data=data)
        data = res.json()
        self.credentials = data
        self.session.headers.update(
            {"Authorization": f"{self.credentials['token_type']} {self.credentials['access_token']}"}
        )

        if grant_type == "refresh":
            logger.info("Refreshed token.")
        else:
            logger.info("Logged in.")

    def get_gfycat(self, gfy_id: str):
        res = self.session.get(f"{BASE_URL}/gfycats/{gfy_id}")
        data = res.json()
        return GfyItem(**self.transform_content_url_key(data["gfyItem"]))

    def new_gfycat_from_url(self, url: AnyHttpUrl):
        raise NotImplemented

    def new_gfycat_from_file(
        self,
        file: str | PathLike,
        *,
        title: str = None,
        description: str = None,
        tags: list[str] = None,
        nsfw: bool = False,
        ignore_md5_check: bool = False,
        keep_audio: True,
        private: False,
    ) -> str:
        session = self.session
        file = Path(file).resolve()
        data = {
            "title": file.name if title is None else title,
            "nsfw": nsfw,
            "keepAudio": keep_audio,
            "noMd5": ignore_md5_check,
            "private": private,
        }
        if description is not None:
            data["description"] = description
        if tags is not None:
            data["tags"] = tags
        retries = Retry(total=100, backoff_factor=0.1)
        session.mount("https://", adapter=HTTPAdapter(max_retries=retries))
        res = session.post(f"{BASE_URL}/gfycats", data=data)
        metadata = res.json()
        with open(file, "rb") as f:
            new_file = io.BytesIO(f.read())
            new_file.name = metadata["gfyname"]
            new_file.seek(0)
            m = MultipartEncoder(
                fields={
                    "key": metadata["gfyname"],
                    "file": (metadata["gfyname"], new_file, "video/mp4"),
                }
            )
            res = requests.post("https://filedrop.gfycat.com", data=m, headers={"Content-Type": m.content_type})
        if res.status_code >= 400:
            raise requests.exceptions.HTTPError(res.text)
        return metadata["gfyname"]

    def check_upload_status(self, gfy_name: str):
        raise NotImplemented

    def update_gfycat(self, gfy_id: str, attribute: str, value: Any):
        self.session.put(f"{BASE_URL}/me/gfycats/{gfy_id}/{attribute}", data={"value": value})
        logger.info(f'Updated Gfycat {gfy_id} {attribute} to "{value}"')

    def delete_gfycat(self, gfy_id: str):
        self.session.delete(f"{BASE_URL}/me/gfycats/{gfy_id}")
        logger.info(f"Deleted Gfycat {gfy_id}")

    def delete_gfycat_attribute(self, gfy_id: str, attribute: str):
        self.session.delete(f"{BASE_URL}/me/gfycats/{gfy_id}/{attribute}")
        logger.info(f"Deleted Gfycat {gfy_id} {attribute}")

    def get_user_feed(self, username: str, cursor: str = None, count: int = None):
        params = {}
        if cursor is not None:
            params["cursor"] = cursor
        if count is not None:
            params["count"] = count
        res = self.session.get(f"{BASE_URL}/users/{username}/gfycats", params=params)
        data = res.json()
        next_cursor: str = data["cursor"]
        return {
            "gfycats": [GfyItem(**self.transform_content_url_key(d)) for d in data["gfycats"]],
            "cursor": next_cursor,
        }

    def get_my_feed(self, cursor: str = None):
        params = {}
        if cursor is not None:
            params["cursor"] = cursor
        res = self.session.get(f"{BASE_URL}/me/gfycats", params=params)
        data = res.json()
        next_cursor: str = data["cursor"]
        return {
            "gfycats": [GfyItem(**self.transform_content_url_key(d)) for d in data["gfycats"]],
            "cursor": next_cursor,
        }

    def get_followers_feed(self, cursor: str = None):
        params = {}
        if cursor is not None:
            params["cursor"] = cursor
        res = self.session.get(f"{BASE_URL}/me/follows/gfycats")
        data = res.json()
        next_cursor: str = data["cursor"]
        return {
            "gfycats": [GfyItem(**self.transform_content_url_key(d)) for d in data["gfycats"]],
            "cursor": next_cursor,
            "count": data["count"],
            "total_count": data["totalCount"],
        }

    def get_my_albums(self):
        res = self.session.get(f"{BASE_URL}/me/album-folders")
        data = res.json()
        return [AlbumNode(**node) for node in data[0]["nodes"]]

    def create_album(self, new_id: str, title: str, description: str = "", contents: list[str] = None):
        if contents is None:
            contents = []
        self.session.post(
            f"{BASE_URL}/me/album-folders/{new_id}",
            data=dict(
                title=title,
                description=description,
                contents=contents,
            ),
        )
        logger.info(f'Created album "{title}"')


gpycat = Gfycat()
