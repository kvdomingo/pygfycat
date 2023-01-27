from pathlib import Path

from loguru import logger
from mako.template import Template

from .get_secret_string import get_secret_string

BASE_DIR = Path(__file__).parent.parent


def make_dotenv():
    template = Template(filename=str(BASE_DIR / "scripts" / "templates" / ".env.mako"))
    env = template.render(
        CLIENT_ID=get_secret_string("CLIENT_ID"),
        CLIENT_SECRET=get_secret_string("CLIENT_SECRET"),
        PYPI_API_TOKEN=get_secret_string("PYPI_API_TOKEN"),
    )
    with open(BASE_DIR / ".env", "w+") as f:
        f.write(env)

    logger.info(".env ok")


if __name__ == "__main__":
    make_dotenv()
