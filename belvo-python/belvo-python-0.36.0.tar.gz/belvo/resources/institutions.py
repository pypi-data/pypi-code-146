from typing import Dict

from belvo.resources.base import Resource


class Institutions(Resource):
    """
    <br>
    <div style="background-color:#f9c806;padding: 6px; border-radius: 4px">
    <strong>Not implemented</strong><br>
    Although included in the SDK, the delete and resume methods for the Institutions resource will raise a <code>NotImplementedError()</code> when used.
    </div>

    """

    endpoint = "/api/institutions/"

    def delete(self, id: str) -> bool:
        raise NotImplementedError()

    def resume(
        self,
        session: str,
        token: str,
        *,
        link: str = None,
        raise_exception: bool = False,
        **kwargs: Dict,
    ) -> Dict:
        raise NotImplementedError()
