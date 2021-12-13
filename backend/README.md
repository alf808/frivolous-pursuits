# Backend - Full Stack Frivolous Pursuits Game API

### Installing Dependencies for the Backend

1. **Python 3.9.7** - install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - pip -m venv <folder_name> [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```

4. **Key Dependencies**
 - [Flask](http://flask.palletsprojects.com/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

### Database Setup
With Postgres running, restore a database using the data.psql file provided. From the backend folder in terminal run:
```bash
psql {database_name} < data.psql
```

### Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Functionalities
Examine the following backend files:

1. *./backend/flaskr/`__init__.py`*
2. *./backend/test_flaskr.py*


Specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.


2. endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.


3. endpoint to handle GET requests for all available categories.


4. endpoint to DELETE question using a question ID.


5. endpoint to POST a new question, which will require the question and answer text, category, and difficulty score.


6. a POST endpoint to get questions based on category.


7. a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.


8. a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.


9. error handlers for all expected errors including 400, 404, 422 and 500.



## Review
```
Documentation of endpoints. Below is an example for endpoint to get all categories.

Endpoints
GET '/api/v1.0/categories'
GET ...
POST ...
DELETE ...

GET '/api/v1.0/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs.
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

```


## Testing
To run the tests, run
```
dropdb database_test
createdb database_test
psql database_test < data.psql
python test_flaskr.py
```
