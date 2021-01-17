"""User interface for interacting with PythonAnywhere files.
Provides a class `Path` which should be used by helper scripts
providing features for programmatic handling of user's files."""

import logging
from urllib.parse import urljoin

from pythonanywhere.api.files_api import Files
from pythonanywhere.snakesay import snakesay

logger = logging.getLogger(name=__name__)


class PAPath:
    """Class providing interface for interacting with PythonAnywhere user files.
    """

    def __init__(self, path):
        self.path = path
        self.api = Files()

    def __repr__(self):
        return self.url 

    def _make_pa_url(self, path):
        return urljoin(self.api.base_url.split("api")[0], path)

    @property
    def url(self):
        files_base = self.api.base_url.replace("/api/v0", "")
        return f"{files_base[:-1]}{self.path}"

    @property
    def contents(self):
        try:
            content = self.api.path_get(self.path)
            return content if type(content) == dict else content.decode("utf-8")
        except Exception as e:
            logger.warning(snakesay(str(e)))
            return None

    @property
    def tree(self):
        try:
            return self.api.tree_get(self.path)
        except Exception as e:
            logger.warning(snakesay(str(e)))
            return None

    def delete(self):
        try:
            self.api.path_delete(self.path)
            logger.info(snakesay(f"{self.path} deleted!"))
            return True
        except Exception as e:
            logger.warning(snakesay(str(e)))
            return False

    def upload(self, content):
        try:
            result = self.api.path_post(self.path, content)
        except Exception as e:
            logger.warning(snakesay(str(e)))
            return False

        msg = {
            200: f"{self.path} successfully updated!",
            201: f"Content successfully uploaded to {self.path}!"
        }[result]

        logger.info(snakesay(msg))
        return True

    def get_sharing_url(self):
        url = self.api.sharing_get(self.path)
        if url:
            logger.info(snakesay(f"{self.path} is shared at {url}"))
            return self._make_pa_url(url)

        logger.info(snakesay(f"{self.path} has not been shared"))
        return ""

    def share(self):
        try:
            code, shared_url = self.api.sharing_post(self.path)
        except Exception as e:
            logger.warning(snakesay(str(e)))
            return ""

        msg = {200: "was already", 201: "successfully"}[code]
        logger.info(snakesay(f"{self.path} {msg} shared at {shared_url}"))
        return self._make_pa_url(shared_url)

    def unshare(self):
        already_shared = self.get_sharing_url()
        if already_shared:
            result = self.api.sharing_delete(self.path)
            if result == 204:
                logger.info(snakesay(f"{self.path} is no longer shared!"))
                return True
            logger.warning(snakesay(f"Could not unshare {self.path}... :("))
            return False
        logger.info(snakesay(f"{self.path} is not being shared, no need to stop sharing..."))
        return True
