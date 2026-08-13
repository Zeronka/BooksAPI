def test_create_author(client):
    response = client.post(
        "/authors",
        json={
            "name": "Pushkin"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Pushkin"
    assert "id" in data


def test_get_all_authors_empty(client):
    response = client.get("/authors")

    assert response.status_code == 200
    assert response.json() == []


def test_get_all_authors_with_pagination(client):
    for i in range(3):
        client.post(
            "/authors",
            json={
                "name": f"Author {i}"
            }
        )

    response = client.get("/authors?skip=0&limit=2")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_author_by_id(client):
    create_response = client.post(
        "/authors",
        json={
            "name": "Tolstoy"
        }
    )

    author_id = create_response.json()["id"]

    response = client.get(f"/authors/{author_id}")

    assert response.status_code == 200
    assert response.json()["id"] == author_id
    assert response.json()["name"] == "Tolstoy"


def test_get_author_not_found(client):
    response = client.get("/authors/999")

    assert response.status_code == 404


def test_update_author(client):
    create_response = client.post(
        "/authors",
        json={
            "name": "Old Name"
        }
    )

    author_id = create_response.json()["id"]

    response = client.put(
        f"/authors/{author_id}",
        json={
            "name": "New Name"
        }
    )

    assert response.status_code == 200
    assert response.json()["name"] == "New Name"


def test_delete_author(client):
    create_response = client.post(
        "/authors",
        json={
            "name": "To Delete"
        }
    )

    author_id = create_response.json()["id"]

    response = client.delete(f"/authors/{author_id}")

    assert response.status_code == 204

    get_response = client.get(f"/authors/{author_id}")

    assert get_response.status_code == 404


def test_pagination_limit_validation(client):
    response = client.get("/authors?limit=200")

    assert response.status_code == 422


def test_pagination_skip_validation(client):
    response = client.get("/authors?skip=-1")

    assert response.status_code == 422