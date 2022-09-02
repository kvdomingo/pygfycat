import os

from dotenv import load_dotenv

from gpycat import gpycat
from gpycat.models import GfyItem

load_dotenv()

gpycat.auth(client_id=os.environ.get("CLIENT_ID"), client_secret=os.environ.get("CLIENT_SECRET"))


def test_get_gfycat():
    item = gpycat.get_gfycat("zestycreepyasiaticlesserfreshwaterclam")
    assert isinstance(item, GfyItem)
