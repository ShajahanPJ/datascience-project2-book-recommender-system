# Frontend Integration

The UI is server-rendered via `templates/index.html` with static assets under `static/`.

## Template (`templates/index.html`)

- Search form posts to `/recommend_books` with `user_input`.
- Top-rated books loop over `book_name`, `author`, `image`, `votes`, `rating`.
- Recommendation results render a grid when `data` is present.

## Scripts

### `static/js/scripts.js`
- On load, fetches `/book_titles` to get an array of titles.
- Adds `input` listener to the search input for autocomplete filtering.
- Shows/hides `.result-box` and `.error-message` accordingly.
- Clicking a suggestion fills the input.

### `static/js/custom.js`
- Handles UI embellishments (scroll to top, carousels, feather icons, counters).

## Example Flow

1. Load `/` -> page renders top-rated books.
2. Browser fetches `/book_titles` -> enables autocomplete.
3. User enters a title and submits -> server responds with recommendations rendered server-side.
