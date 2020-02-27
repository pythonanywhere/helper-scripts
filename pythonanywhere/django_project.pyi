from pathlib import Path

from pythonanywhere.project import Project
from typing import Optional

class DjangoProject(Project):
    def download_repo(self, repo: str, nuke: bool) -> None: ...
    def create_virtualenv(self, django_version: Optional[str] = ..., nuke: bool = ...) -> None: ...
    def detect_requirements(self): ...
    def run_startproject(self, nuke: bool) -> None: ...
    settings_path: Path = ...
    manage_py_path: Path = ...
    def find_django_files(self) -> None: ...
    def update_settings_file(self) -> None: ...
    def run_collectstatic(self) -> None: ...
    def run_migrate(self) -> None: ...
    def update_wsgi_file(self) -> None: ...