import json

from requests import Session


class GfySession(Session):
    @staticmethod
    def _check_json_body(**kwargs):
        data = kwargs.get("data")
        if isinstance(data, dict):
            data = json.dumps(data)
            kwargs.update({"data": data})
        return kwargs

    def post(self, *args, **kwargs):
        kwargs = self._check_json_body(**kwargs)
        return super().post(*args, **kwargs)

    def put(self, *args, **kwargs):
        kwargs = self._check_json_body(**kwargs)
        return super().put(*args, **kwargs)

    def patch(self, *args, **kwargs):
        kwargs = self._check_json_body(**kwargs)
        return super().patch(*args, **kwargs)
