from httpx import AsyncClient
from ..conftest import app

import pytest

from server.models import ObjectIdStr


@pytest.mark.asyncio
async def test_get_files(
) -> None:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/file/")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_file(
    tmpdir_factory
) -> None:
    file_name = 'test.txt'
    file = tmpdir_factory.mktemp('data').join(file_name)
    with file.open('w') as f:
        f.write('Test')
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/file/", files={"file": (file_name, open(file, "rb"))})
    content = response.json()
    assert response.status_code == 201
    assert content['filename'] == file_name
    assert 'upload_date' in content
    assert 'user_id' in content

