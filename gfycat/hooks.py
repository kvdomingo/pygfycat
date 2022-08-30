from loguru import logger
from requests import Response


def raise_if_not_ok(response: Response, *args, **kwargs):
    if not response.ok:
        logger.error(response.text)
        raise ConnectionError(response.text)
