from datetime import datetime
import pytest
import pytest_asyncio

from server import crud
from server.models import FileRetrieve, FileCreate


# @pytest.mark.asyncio
@pytest_asyncio.fixture
async def test_create_item(conn) -> None:
    create_file_data = {
        'filename': 'test.txt',
        'file_id': '622d2922aba595bf5c62ec67',
        'upload_date': datetime(2020,1,1),
        'user_id': 5
    }
    item = await crud.create_file(FileCreate(**create_file_data), conn)
    create_file_data['_id'] = item.get('_id')
    assert item == create_file_data

# def test_get_item(db: Session) -> None:
#     title = random_lower_string()
#     description = random_lower_string()
#     item_in = ItemCreate(title=title, description=description)
#     user = create_random_user(db)
#     item = crud.item.create_with_owner(db=db, obj_in=item_in, owner_id=user.id)
#     stored_item = crud.item.get(db=db, id=item.id)
#     assert stored_item
#     assert item.id == stored_item.id
#     assert item.title == stored_item.title
#     assert item.description == stored_item.description
#     assert item.owner_id == stored_item.owner_id