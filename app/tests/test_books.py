def test_create_book(client):
    author_response = client.post(
        "/authors",
        json={
            "name": "Pushkin"
        }
    )

    author_id = author_response.json()["id"]

    response = client.post(
        "/books",
        json={
            "title": "Eugene Onegin",
            "years": 1833,
            "author_id": author_id
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Eugene Onegin"
    assert data["years"] == 1833
    assert data["author_id"] == author_id
    assert data["author"]["id"] == author_id
    assert data["author"]["name"] == "Pushkin"
    assert "id" in data


def test_get_all_books_empty(client):
    response = client.get("/books")

    assert response.status_code == 200
    assert response.json() == []

def test_get_all_books_with_pagination(client):
    author_response = client.post(
        "/authors",
        json={
            "name": "Pushkin"
        }
    )

    author_id = author_response.json()["id"]

    for i in range(3):
        client.post(
            "/books",
            json={
                "title": f"Book {i}",
                "years": 2000 + i,
                "author_id": author_id
            }
        )

    response = client.get("/books?skip=0&limit=2")

    assert response.status_code == 200

    books = response.json()

    assert len(books) == 2

    # BookListResponse содержит только id и title
    assert "id" in books[0]
    assert "title" in books[0]

def test_get_book_by_id(client):
    author_response = client.post(
        "/authors",
        json={
            "name": "Tolstoy"
        }
    )

    author_id = author_response.json()["id"]

    create_response = client.post(
        "/books",
        json={
            "title": "War and Peace",
            "years": 1869,
            "author_id": author_id
        }
    )

    book_id = create_response.json()["id"]

    response = client.get(f"/books/{book_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == book_id
    assert data["title"] == "War and Peace"
    assert data["years"] == 1869
    assert data["author_id"] == author_id
    assert data["author"]["name"] == "Tolstoy"

def test_get_book_not_found(client):
    response = client.get("/books/999")

    assert response.status_code == 404

def test_search_book_by_title(client):
    author_response = client.post(
        "/authors",
        json={
            "name": "Dostoevsky"
        }
    )

    author_id = author_response.json()["id"]

    client.post(
        "/books",
        json={
            "title": "Crime and Punishment",
            "years": 1866,
            "author_id": author_id
        }
    )

    response = client.get(
        "/books/search_by_title?title=Crime"
    )

    assert response.status_code == 200

    books = response.json()

    assert len(books) == 1
    assert books[0]["title"] == "Crime and Punishment"

def test_get_books_by_author(client):
    author_response = client.post(
        "/authors",
        json={
            "name": "Pushkin"
        }
    )

    author_id = author_response.json()["id"]

    for i in range(3):
        client.post(
            "/books",
            json={
                "title": f"Book {i}",
                "years": 1800 + i,
                "author_id": author_id
            }
        )

    response = client.get(
        f"/books/by-author/{author_id}?skip=0&limit=2"
    )

    assert response.status_code == 200

    books = response.json()

    assert len(books) == 2

def test_update_book(client):
    author_response = client.post(
        "/authors",
        json={
            "name": "Author"
        }
    )

    author_id = author_response.json()["id"]

    create_response = client.post(
        "/books",
        json={
            "title": "Old Title",
            "years": 1900,
            "author_id": author_id
        }
    )

    book_id = create_response.json()["id"]

    response = client.put(
        f"/books/{book_id}",
        json={
            "title": "New Title",
            "years": 2000,
            "author_id": author_id
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "New Title"
    assert data["years"] == 2000
    assert data["author_id"] == author_id

def test_delete_book(client):
    author_response = client.post(
        "/authors",
        json={
            "name": "Author"
        }
    )

    author_id = author_response.json()["id"]

    create_response = client.post(
        "/books",
        json={
            "title": "Book",
            "years": 2000,
            "author_id": author_id
        }
    )

    book_id = create_response.json()["id"]

    response = client.delete(f"/books/{book_id}")

    assert response.status_code == 204

    get_response = client.get(f"/books/{book_id}")

    assert get_response.status_code == 404

def test_book_pagination_limit_validation(client):
    response = client.get("/books?limit=200")

    assert response.status_code == 422

def test_book_pagination_skip_validation(client):
    response = client.get("/books?skip=-1")

    assert response.status_code == 422