# Full Stack API Development of a Game called Frivolous Pursuits

This is a project using a game with a series of questions and answers. It serves as a practice for API Development and Documentation. Developing this game API provides one the ability to structure plan, implement, and test an API. It has the following functionality.

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

All backend code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/). The frontend code is only used to demonstrate how the API is consumed.

## Getting Started: prerequisites and local development

Developers using this project should already have python (>3.9), pip, postgresql (>12) and node installed on their local machines. The full stack application is designed with some key functional areas:

### Backend
The [./backend](backend/README.md) directory contains a Flask and SQLAlchemy server. It contains definitions of the endpoints and can reference models.py for DB and SQLAlchemy setup. Start with the following commands:
```
pip install -r requirements.txt
```

```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```
The application is run on `http://127.0.0.1:5000/` by default and is a proxy in the frontend configuration.

### Frontend

The [./frontend](frontend/README.md) directory contains a React frontend to consume the data from the Flask server:

1. Examine the end points and HTTP methods the frontend is expecting to consume.
2. See how are the requests from the frontend formatted.

Start the frontend with the following commands:
```
npm install // only once to install dependencies
npm start
```

By default, the frontend will run on localhost:3000.

### Tests
In order to run tests navigate to the backend folder and run the following commands:

```
dropdb dbname_test
createdb dbname_test
psql dbname_test < data.psql
python test_flaskr.py
```

You can replace the dbname_test with any database name.

All tests are kept in the ```test_flaskr.py``` file and should be maintained as updates are made to app functionality.

## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration.
- Authentication: This version of the application does not require authentication or API keys.

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False,
    "error": 400,
    "message": "bad request"
}
```
The API will return five error types when requests fail:
- 400: bad request
- 404: resource not found
- 405: method not allowed
- 422: unprocessable
- 500: Internal Server Error

### Endpoints: sample CURL commands are provided for the more difficult requests

#### GET /categories
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- `curl http://127.0.0.1:5000/categories`
- Returns: An object with a single key, categories, that contains an object of id: category_string key:value pairs.
```
{
    'categories': { '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports" }
}
```

#### GET '/questions?page=${integer}'
- Fetches a paginated set of questions, a total number of questions, all categories and current category string.
- Request Arguments: page - integer
- Returns: An object with 10 paginated questions, total questions, object including all categories, and current category string
```
{
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer',
            'difficulty': 5,
            'category': 2
        },
    ],
    'totalQuestions': 100,
    'categories': { '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports" },
    'currentCategory': 'History'
}
```

#### GET '/categories/${id}/questions'
- Fetches questions for a cateogry specified by id request argument
- Request Arguments: id - integer
- Returns: An object with questions for the specified category, total questions, and current category string
```
{
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer',
            'difficulty': 5,
            'category': 4
        },
    ],
    'totalQuestions': 100,
    'currentCategory': 'History'
}
```

#### DELETE '/questions/${id}'
- Deletes a specified question using the id of the question
- Request Arguments: id - integer
- `curl -X DELETE http://127.0.0.1:5000/questions/99`
- Returns: The id of the question.

#### POST '/quizzes'
- Sends a post request in order to get the next question
- Request Body:
```
{'previous_questions':  an array of question id's such as [1, 4, 20, 15]
'quiz_category': a string of the current category }
```

- Returns: a single new question object
```
{
    'question': {
        'id': 1,
        'question': 'This is a question',
        'answer': 'This is an answer',
        'difficulty': 5,
        'category': 4
    }
}
```

#### POST '/questions'
- Sends a post request in order to add a new question
- `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"What is my name", "answer":"alf", "difficulty":"5", "category":"3"}'`
- Request Body:
```
{
    'question':  'Heres a new question string',
    'answer':  'Heres a new answer string',
    'difficulty': 1,
    'category': 3,
}
```
- Returns: Does not return any new data
```
{
    'created':  'question, id: 43',
    'total_questions': new count of questions,
}
```

#### POST '/questions/search'
- Sends a post request in order to search for a specific question by search term
- Request Body:
```
{
    'searchTerm': 'this is the term the user is looking for'
}
```

- Returns: any array of questions, a number of totalQuestions that met the search term and the current category string
```
{
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer',
            'difficulty': 5,
            'category': 5
        },
    ],
    'totalQuestions': 100,
    'currentCategory': 'Entertainment'
}
```

## Deployment: not applicable

## Authors
Alf Maglalang

## Acknowledgements
Flask, SQLAlchemy, PostgreSQL, Python (3.9.7) and their respective documentation.
