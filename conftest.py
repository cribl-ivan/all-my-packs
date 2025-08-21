import pytest
import pathlib
from tests.YamlFile import YamlFile
from tests.Packs import JsonFile
    
@pytest.hookimpl()
def pytest_collect_file(parent, file_path : pathlib.PosixPath):
    if (file_path.suffix == ".yml" and 'pipelines' in file_path.parts and not file_path.name == "route.yml"):
        return YamlFile.from_parent(parent, path=file_path)

    if (file_path.name == "package.json"):
        return JsonFile.from_parent(parent, path=file_path)
