# App Module (`app.py`)

This Flask app powers Book World. It loads precomputed data artifacts and exposes routes for the homepage, book titles, and recommendations.

## Globals and Data Files

- `popular_df`: Loaded from `model/popular.pkl` — contains columns `Book-Title`, `Book-Author`, `Image-URL-M`, `Number_of_ratings`, `avg_rating`.
- `pt`: Loaded from `model/pt.pkl` — pivot table with book titles as index.
- `books`: Loaded from `model/books.pkl` — not directly used in routes but available for extensions.
- `similarity_score`: Loaded from `model/similarity_score.pkl` — cosine similarity matrix aligned to `pt.index`.
- `famous_book_details`: Loaded from `model/famous_book_details.pkl` — book metadata used to render author and image.

## Functions

### `get_top_rated_books()`
Returns a mapping for top-rated lists rendered on the homepage:
- `book_name`: list of strings
- `author`: list of strings
- `image`: list of URLs
- `votes`: list of numbers
- `rating`: list of numbers

### Routes

#### `GET /`
Renders `templates/index.html` with top-rated books injected as context.

#### `GET /book_titles`
Returns JSON array of titles from `famous_book_details['Book-Title']`.

#### `POST /recommend_books`
Accepts form field `user_input`. Case-insensitive match against `pt.index` is used to locate the seed title. The most similar titles are computed from `similarity_score` and rendered in the template under the `data` context as a list of `[title, author, image]` entries.

- On missing input: shows `error_message`.
- On not found: shows `error_message`.
- On empty `pt`: shows `error_message`.

## Application Flow

1. Visitor loads `/` and sees top-rated books (from `popular_df`).
2. Frontend requests `/book_titles` to power autocomplete.
3. User submits the form to `/recommend_books` -> server computes similar items and re-renders the homepage with a `data` block.
