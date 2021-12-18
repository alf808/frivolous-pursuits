import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

class ValidationError(Exception):
    """Inherit exception class to use for error handling"""
    pass

def paginate_questions(request, selection):
    """Limit number of questions presented per page"""
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

def create_app(test_config=None):
    """create and configure the app"""
    app = Flask(__name__)
    setup_db(app)

    '''
    Set up CORS. Allow '*' for origins
    '''
    CORS(app, resources={'/': {'origins': '*'}})
    '''
    after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add(
        'Access-Control-Allow-Headers', 'Content-Type, Authorization,true')
        response.headers.add(
        'Access-Control-Allow-Methods', 'GET,POST,DELETE,OPTIONS')
        return response

    '''
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    '''
    @app.route('/categories')
    def get_categories():
        categories = Category.query.all()

        if len(categories) == 0:
        abort(404)

        return jsonify({
        'success': True,
        'categories': {cat.id:cat.type for cat in categories}
        })

    '''
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.
    
    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    '''
    @app.route('/questions')
    def get_questions():
        query = Question.query.all()
        categories = Category.query.all()
        current_questions = paginate_questions(request, query)

        if len(current_questions) == 0:
        abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(query),
            'current_category': 'ALL',
            'categories': {cat.id:cat.type for cat in categories}
        })
    '''
    @TODO:
    Create an endpoint to DELETE question using a question ID.
    
    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.get(question_id)
        if question is None:
        abort(404)

        try:
        question.delete()
        except:
        db.session.rollback()
        abort(422)
        else:
        return jsonify({
            'success': True,
            'deleted': question_id
            })
        finally:
        db.session.close()

    '''
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.
    
    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    '''
    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()
        question = body.get('question', None)
        answer = body.get('answer', None)
        category = int(body.get('category', None))
        difficulty = int(body.get('difficulty', None))
        try:
            if not all(body.values()) or category not in range(1,7) or difficulty not in range(1,6):
                raise ValidationError('question: not-empty string, answer: not-empty string, category: 1-6, difficulty: 1-5')

            question = Question(
                question = question,
                answer = answer,
                category = category,
                difficulty = difficulty
            )
            question.insert()
        except ValidationError as ve:
            db.session.rollback()
            abort(422, description=f'Correction needed. {ve}')
        else:
            res = f'{question.question}, id: {question.id}'
            json_obj = jsonify({
                'success': True,
                'created': res,
                'total_questions': len(Question.query.all())
            })
        finally:
            db.session.close()
            print(body)
        return json_obj
    '''
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.
    
    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    '''
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        body = request.get_json()
        search_term = body.get('searchTerm', None)
        data = Question.query.filter(Question.question.ilike(f"%{search_term}%")).all()
        current_questions = paginate_questions(request, data)
        if data:
            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(data),
                'current_category': 'ALL'
            })
        else:
            abort(404)
    '''
    @TODO:
    Create a GET endpoint to get questions based on category.
    
    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    '''
    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        category = Category.query.get(category_id)
        query = Question.query.filter(Question.category==category_id).all()
        current_questions = paginate_questions(request, query)
        if len(current_questions) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(query),
            'current_category': category.type
        })

    '''
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.
    
    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    '''
    @app.route('/quizzes', methods=['POST'])
    def get_quizzes():
        body = request.get_json()
        previous_questions = body.get('previous_questions', None)
        quiz_category = body.get('quiz_category', None)
        category_id = int(quiz_category['id'])

        try:
            if not any(body.values()):  # check if any falsy values
                raise ValueError('type not right')
                # abort(404)

            if category_id == 0:
                query = Question.query.all()
            else:
                query = Question.query.filter(Question.category==category_id).all()
            if query:
                question = random.choice(query)
                json_obj = jsonify({
                    'success': True,
                    'question': question.format()
                })
            else:
                abort(404)
        except ValueError as ve:
            abort(404, description=ve)
        finally:
            print(body)

        return json_obj
    '''
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    '''
    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "bad request"}), 400

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({"success": False,v"error": 500, "message": "Internal Server Error"}), 500

    return app
