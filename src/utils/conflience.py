from typing import Dict, Any
from requests import HTTPError
from src.vendor.atlassian import Confluence as VendorConfluence
import src.conf.atlassian_api as atlassian_conf
from src.vendor.atlassian.errors import ApiError


class ConfluenceException(HTTPError):
    pass


class Confluence():
    __client = None

    def __init__(self) -> None:
        try:
            self.__client = VendorConfluence(
                url=atlassian_conf.SERVER,
                username=atlassian_conf.USERNAME,
                password=atlassian_conf.TOKEN,
                cloud=True
            )
        except HTTPError as e:
            raise ConfluenceException(*e.response.json().get('errorMessages', None))

    def get_project_space(self, space: str) -> Dict[str, Any]:
        try:
            return self.__client.get_space(space)
        except HTTPError as e:
            raise ConfluenceException(e.response.json().get('message', None))
        except ApiError as e:
            raise ConfluenceException(e.args[0])
