import os

from dotenv import load_dotenv

from gfycat import gfycat
from gfycat.models import GfyItem

load_dotenv()

gfycat.auth(client_id=os.environ.get("CLIENT_ID"), client_secret=os.environ.get("CLIENT_SECRET"))


def test_get_gfycat():
    item = gfycat.get_gfycat("zestycreepyasiaticlesserfreshwaterclam")
    assert isinstance(item, GfyItem)
