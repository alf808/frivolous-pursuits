# Full Stack Frivolous Pursuits API

## Full Stack Frivolous Pursuits Game

Frivolous Pursuits is question and answer game:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

Writing this game app will give you the ability to structure plan, implement, and test an API - skills essential for enabling your future applications to communicate with others.

## About the Stack

The full stack application is designed with some key functional areas:

### Backend
The [./backend](backend/README.md) directory contains a Flask and SQLAlchemy server. The file `__init__.py` contains definitions of the endpoints and can reference models.py for DB and SQLAlchemy setup.


### Frontend

The [./frontend](frontend/README.md) directory contains a React frontend to consume the data from the Flask server:

1. Examine the end points and HTTP methods the frontend is expecting to consume.
2. See how are the requests from the frontend formatted.

Examine the frontend behavior to see the above information. These are the files examine in the frontend:

1. *./frontend/src/components/QuestionView.js*
2. *./frontend/src/components/FormView.js*
3. *./frontend/src/components/QuizView.js*


>View the [README within ./frontend for more details.](./frontend/README.md)
