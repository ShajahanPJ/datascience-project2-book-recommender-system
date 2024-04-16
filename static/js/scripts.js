const resultsBox = document.querySelector(".result-box");
const inputBox = document.querySelector('.input-text');
const errorMessage = document.querySelector('.error-message');

// Fetch book titles from Flask API endpoint
fetch('/book_titles')
    .then(response => response.json())
    .then(bookTitles => {
        const availableKeywords = bookTitles.map(title => title.trim()); // Trim all book titles

        // Function to handle input event
        inputBox.addEventListener('input', function() {
            const input = this.value.trim();
            if (input) {
                // Filter available keywords based on input
                const result = availableKeywords.filter(keyword =>
                    keyword.toLowerCase().includes(input.toLowerCase())
                );
                if (result.length > 0) {
                    // Display autocomplete results if any matching keyword is found
                    display(result);
                    resultsBox.style.display = 'block';
                    // Hide the error message
                    errorMessage.style.display = 'none';
                } else {
                    // Hide autocomplete results if no matching keyword is found
                    resultsBox.style.display = 'none';
                    // Show the error message
                    errorMessage.style.display = 'block';
                }
            } else {
                // Hide autocomplete results if input is empty
                resultsBox.style.display = 'none';
                // Show the error message if input is empty
                errorMessage.style.display = 'block';
            }
        });

        // Function to display autocomplete results
        function display(result) {
            const content = result.slice(0, 6).map(list => "<li class='autocomplete-item'>" + list + "</li>").join('');
            resultsBox.innerHTML = "<ul>" + content + "</ul>";

            // Call the breakLinesInAutoComplete function when the results are displayed
            breakLinesInAutoComplete();

            // Add click event listeners to autocomplete items
            const autocompleteItems = document.querySelectorAll('.autocomplete-item');
            autocompleteItems.forEach(item => {
                item.addEventListener('click', function() {
                    inputBox.value = item.textContent; // Update input box value with clicked item text
                    resultsBox.style.display = 'none'; // Hide autocomplete results
                    inputBox.focus(); // Set focus back to input box
                });
            });
        }
    })
    .catch(error => {
        console.error('Error fetching book titles:', error);
    });
// JavaScript function to break lines in auto-complete book names after a certain number of words for screens below 768px
function breakLinesInAutoComplete() {
    const items = document.querySelectorAll('.result-box ul li');
    const screenWidth = window.innerWidth;

    if (screenWidth < 768) {
        items.forEach(item => {
            let text = item.textContent.trim();
            const words = text.split(/\s+/); // Split text into words using whitespace as delimiter
            const maxWordsPerLine = 6; // Maximum number of words per line

            // Group words into lines
            let lines = [];
            let currentLine = '';
            for (let i = 0; i < words.length; i++) {
                // Add the current word to the current line
                currentLine += (currentLine === '' ? '' : ' ') + words[i];

                // If the current line reaches the maximum number of words, add it to the lines array
                if (i === words.length - 1 || currentLine.split(/\s+/).length === maxWordsPerLine) {
                    lines.push(currentLine);
                    currentLine = '';
                }
            }

            // Update the li element with the modified text
            item.innerHTML = lines.map(line => `<div>${line}</div>`).join('');
        });
    } else {
        // If screen width is 768px or above, remove any line breaks
        items.forEach(item => {
            item.textContent = item.textContent.replace(/\n/g, ' ');
        });
    }
}
