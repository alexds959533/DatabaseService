from fastapi.testclient import TestClient
import pytest

from server.models import ObjectIdStr


@pytest.mark.anyio
def test_get_files(
    client: TestClient
) -> None:
    data = {
        "filename": "string",
        "owner": "string"
    }
    response = client.get(
        "/file/", json=data,
    )
    assert response.status_code == 200


@pytest.mark.anyio
def test_create_file(
    client: TestClient,
    tmpdir_factory
) -> None:
    file_name = 'test.txt'
    file = tmpdir_factory.mktemp('data').join(file_name)
    with file.open('w') as f:
        f.write('Test')
    response = client.post("/file/", files={"file": (file_name, open(file, "rb"))})
    content = response.json()
    assert response.status_code == 201
    assert content['filename'] == file_name
    assert 'upload_date' in content
    assert 'user_id' in content

