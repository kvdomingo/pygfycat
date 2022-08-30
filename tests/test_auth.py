import os

from dotenv import load_dotenv

from gfycat import gfycat

load_dotenv()


def test_auth():
    gfycat.auth(
        grant_type="password",
        client_id=os.environ.get("CLIENT_ID"),
        client_secret=os.environ.get("CLIENT_SECRET"),
        username=os.environ.get("USERNAME"),
        password=os.environ.get("PASSWORD"),
    )
    assert gfycat.last_request_status == 200
    assert gfycat.client_id is not None
    assert len(gfycat.client_id) > 0
