# Literature Crossword

An interactive web application for creating and solving literature-themed crossword puzzles. This application allows administrators to create crossword puzzles with words from literary works, including hints and additional information about each word.

## Features

- Admin interface for adding words and their positions
- Interactive 15x15 crossword grid
- Word hints organized by orientation (Across/Down)
- Additional information display when words are correctly guessed
- Responsive design for both desktop and mobile devices

## Setup

### Option 1: Local Setup

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Initialize the database:
```bash
python
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()
>>> exit()
```

4. Run the application:
```bash
python app.py
```

### Option 2: Docker Setup

1. Make sure you have Docker and Docker Compose installed on your system.

2. Build and start the containers:
```bash
docker-compose up --build
```

3. In a new terminal, initialize the database:
```bash
docker-compose exec web python
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()
>>> exit()
```

The application will be available at `http://localhost:5000`

## Usage

### Admin Interface
Access the admin interface at `http://localhost:5000/admin` to:
1. Add words with their hints, literary work information, and positions
2. Arrange words on the grid by specifying their starting positions and orientation
3. Save changes to update the crossword puzzle

### Playing the Crossword
1. Visit the play page
2. Use the hints to solve the crossword
3. Enter letters in the grid or use the word input fields
4. When a word is correctly guessed, additional information about the literary work will be displayed

## Technologies Used

- Flask
- SQLAlchemy
- Bootstrap 5
- JavaScript
- HTML/CSS
- Docker 