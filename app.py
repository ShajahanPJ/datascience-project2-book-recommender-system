from flask import Flask, render_template, request, jsonify
import os
import pickle
import numpy as np

# Define the path to the model folder
MODEL_FOLDER = os.path.join(os.path.dirname(__file__),  'model')

# Construct the file paths
popular_file = os.path.join(MODEL_FOLDER, 'popular.pkl')
pt_file = os.path.join(MODEL_FOLDER, 'pt.pkl')
books_file = os.path.join(MODEL_FOLDER, 'books.pkl')
similarity_score_file = os.path.join(MODEL_FOLDER, 'similarity_score.pkl')
famous_book_details_file = os.path.join(MODEL_FOLDER, 'famous_book_details.pkl')

# Load the pickle files
popular_df = pickle.load(open(popular_file, 'rb'))
pt = pickle.load(open(pt_file, 'rb'))
books = pickle.load(open(books_file, 'rb'))
similarity_score = pickle.load(open(similarity_score_file, 'rb'))
famous_book_details = pickle.load(open(famous_book_details_file, 'rb'))

# Specify the absolute path to the templates folder
TEMPLATES_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'templates')

app = Flask(__name__)





def get_top_rated_books():
    return {
        'book_name': list(popular_df['Book-Title'].values),
        'author': list(popular_df['Book-Author'].values),
        'image': list(popular_df['Image-URL-M'].values),
        'votes': list(popular_df['Number_of_ratings'].values),
        'rating': list(popular_df['avg_rating'].values)
    }


# Route to get the list of book titles
@app.route('/book_titles')
def get_book_titles():
    book_titles = list(famous_book_details['Book-Title'])
    return jsonify(book_titles)



@app.route('/')
def index():
    top_rated_books = get_top_rated_books()
    return render_template('index.html', **top_rated_books)



@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')

    # Check if user input is empty
    if not user_input:
        error_message = "Please enter a book name..!!"
        top_rated_books = get_top_rated_books()
        return render_template('index.html', error_message=error_message, **top_rated_books)

    # Convert user input to lowercase
    user_input_lower = user_input.lower()

    # Check if pt is not empty before accessing its index
    if not pt.empty:
        try:
            # Convert all book titles in pt to lowercase
            pt_lower = pt.index.str.lower()

            # Find index of the lowercase user input
            index = np.where(pt_lower == user_input_lower)[0][0]

            similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:9]

            data = []
            for i in similar_items:
                item = []
                temp_df = famous_book_details[famous_book_details['Book-Title'].str.lower() == pt_lower[i[0]]]

                item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
                item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
                item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

                data.append(item)

            top_rated_books = get_top_rated_books()
            return render_template('index.html', data=data, **top_rated_books)
        except IndexError:
            # Handle the case where the user input index is not found
            error_message = "Book not found. Please try again."
            top_rated_books = get_top_rated_books()
            return render_template('index.html', error_message=error_message, **top_rated_books)
    else:
        # Handle the case where pt is empty
        error_message = "No user inputs available"
        top_rated_books = get_top_rated_books()
        return render_template('index.html', error_message=error_message, **top_rated_books)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

