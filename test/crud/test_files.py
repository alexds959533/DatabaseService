from datetime import datetime
import pytest
import pytest_asyncio

from server import crud
from server.models import FileRetrieve, FileCreate


def test_h():
    assert 5==5


@pytest.mark.asyncio
async def test_create_file(get_db) -> None:
    create_file_data = {
        'filename': 'test.txt',
        'file_id': '622d2922aba595bf5c62ec67',
        'upload_date': datetime(2020,1,1),
        'user_id': 5
    }
    item = await crud.create_file(FileCreate(**create_file_data), get_db)
    create_file_data['_id'] = item.get('_id')
    assert item == create_file_data


@pytest.mark.asyncio
async def test_get_files(get_db) -> None:
    files = await crud.retrieve_files(get_db)

    files