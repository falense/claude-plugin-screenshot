import pytest
from pathlib import Path


@pytest.fixture
def tmp_screenshots(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    return tmp_path
