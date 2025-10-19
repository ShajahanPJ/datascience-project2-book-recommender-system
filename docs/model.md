# Model and Data (`model/`)

This project uses precomputed artifacts stored as pickle files under `model/`.

## Files

- `popular.pkl`: DataFrame of popular/top-rated books with `Book-Title`, `Book-Author`, `Image-URL-M`, `Number_of_ratings`, `avg_rating`.
- `pt.pkl`: Pivot table (e.g., user-item) with book titles as index. Used to locate a title index and align with the similarity matrix.
- `books.pkl`: Book catalog metadata. Not directly used by current routes.
- `similarity_score.pkl`: 2D array-like (NumPy or similar) of similarity scores between titles; aligned to `pt.index`.
- `famous_book_details.pkl`: DataFrame with book metadata used for rendering results (title, author, image).
- `book_titles_list.py`: Python file containing a `book_titles_list` with many titles (not used by the app at runtime).

## Data Shapes and Expectations

- The index of `pt` must match the order used by `similarity_score`.
- Titles are matched case-insensitively.
- Rendering expects author and medium image URL fields to be present in `famous_book_details`.

## Extending the Model

- Replace or regenerate the artifacts and restart the app.
- If artifacts change shape, update `app.py` accordingly.
