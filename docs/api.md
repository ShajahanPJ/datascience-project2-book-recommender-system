# API Endpoints

Base URL: `http://localhost:5000`

## GET /book_titles

Returns the list of book titles available for autocomplete and discovery.

- **Method**: GET
- **Auth**: None
- **Response**: `200 OK` with JSON array of strings

### Example

```bash
curl http://localhost:5000/book_titles
```

```json
[
  "1984",
  "A Fine Balance",
  "Beloved"
]
```

## POST /recommend_books

Generates book recommendations similar to a provided book title.

- **Method**: POST (form-encoded)
- **Auth**: None
- **Body params**:
  - `user_input` (string, required): The title of a book
- **Responses**:
  - `200 OK` HTML page with recommended books rendered in the template
  - `200 OK` HTML page with `error_message` if input invalid or not found

### Example

```bash
curl -X POST http://localhost:5000/recommend_books \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'user_input=The Hobbit'
```

The response is an HTML page; recommendations appear within elements in the `#home` section. For programmatic access, prefer scraping or exposing a JSON variant (see below).

### Suggested JSON variant (optional)

To enable pure-API usage, consider adding:

- `POST /api/recommendations` -> JSON `{ recommendations: [{ title, author, imageUrl }] }`

