
Built by https://www.blackbox.ai

---

# Bingo Card Generator

## Project Overview

The Bingo Card Generator is a simple web application built using Flask that generates and displays bingo cards. The application creates a database of bingo cards with unique serial numbers and production batches, each containing a set of randomly generated bingo numbers. Users can view different pages of bingo cards, and search for specific card numbers.

## Installation

To run this project locally, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/bingo-card-generator.git
    cd bingo-card-generator
    ```

2. Create a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```bash
    pip install Flask
    ```

4. Run the application:
    ```bash
    python app.py
    ```

5. Open your web browser and go to `http://127.0.0.1:8000`.

## Usage

- When you first run the application, it initializes a SQLite database and generates 63,000 bingo cards automatically.
- You can view the bingo cards organized in pages. Each page contains 36 cards displayed in a 6x6 format.
- You can search for a specific card using the search feature by entering the card number, and it will redirect you to the corresponding page.

## Features

- Random generation of bingo numbers organized by B-I-N-G-O.
- Unique serial numbers and production batches for each bingo card.
- The ability to search for specific bingo cards.
- A friendly web interface that allows easy navigation between pages of cards.

## Dependencies

This project relies on the following dependencies:

- Flask: A micro web framework for Python.
- SQLite3: Built into Python for database management.

Make sure you have the correct version of Python installed, as Flask requires Python 3.5 or higher.

## Project Structure

```
bingo-card-generator/
│
├── app.py                # Main application file
├── bingo_cards.db        # SQLite database file (generated automatically)
└── templates/
    └── index.html        # HTML template for rendering bingo cards
```

### Explanation of Key Files

- **app.py**: This is the primary script where the Flask application is defined. This file contains the logic for generating bingo numbers, initializing the database, and serving the web pages.
- **bingo_cards.db**: The SQLite database file where all bingo cards are stored. The application creates this file on the first run.
- **templates/index.html**: The HTML file used to display the bingo cards in a web interface.

## Contributing

Feel free to fork the repository, make changes, and submit a pull request. Any contributions or suggestions for improvement are welcome!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.