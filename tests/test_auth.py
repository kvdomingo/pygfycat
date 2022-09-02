import os

from dotenv import load_dotenv

from gpycat import gpycat

load_dotenv()


def test_auth():
    gpycat.auth(
        grant_type="password",
        client_id=os.environ.get("CLIENT_ID"),
        client_secret=os.environ.get("CLIENT_SECRET"),
        username=os.environ.get("USERNAME"),
        password=os.environ.get("PASSWORD"),
    )
    assert gpycat.last_request_status == 200
    assert len(gpycat.credentials.keys()) > 0
    assert len(gpycat.client_id) > 0
