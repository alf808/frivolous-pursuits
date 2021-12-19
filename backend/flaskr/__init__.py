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

    # Set up CORS. Allow '*' for origins
    CORS(app, resources={'/': {'origins': '*'}})

    # after_request decorator to set Access-Control-Allow
    @app.after_request
    def after_request(response):
        response.headers.add(
        'Access-Control-Allow-Headers', 'Content-Type, Authorization,true')
        response.headers.add(
        'Access-Control-Allow-Methods', 'GET,POST,DELETE,OPTIONS')
        return response

    '''
    Endpoint to handle GET requests for all available categories.
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
    Endpoint to handle GET requests for questions w/ pagination (10 items)
    This endpoint returns a list of questions,
    number of total questions, current category, categories.
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
    Endpoint to DELETE question using a question ID.
    '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        query = Question.query.get(question_id)
        if not query:
            abort(422)

        try:
            query.delete()
        except:
            db.session.rollback()
            abort(422)
        else:
            res_obj = jsonify({
                'success': True,
                'deleted': question_id
                })
        finally:
            db.session.close()

        return res_obj

    '''
    Endpoint to POST a new question w/ question and answer text,
    category integer, and difficulty level integer.
    '''
    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()
        question = body.get('question', None)
        answer = body.get('answer', None)
        try:
            category = int(body.get('category', None))
            difficulty = int(body.get('difficulty', None))
            if (not all(body.values()) or
                category not in range(1,7) or difficulty not in range(1,6)):
                raise ValidationError('question/answer: text, cat/diff: int')

            question = Question(
                question = question,
                answer = answer,
                category = category,
                difficulty = difficulty
            )
            question.insert()
        except (ValidationError, TypeError) as e:
            db.session.rollback()
            abort(422, description=f'Correction needed. {e}')
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
    POST endpoint to get questions based on a search term.
    '''
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        body = request.get_json()
        search_term = body.get('searchTerm', None)
        query = Question.query.filter(
            Question.question.ilike(f"%{search_term}%")).all()
        current_questions = paginate_questions(request, query)
        if not query:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(query),
            'current_category': 'ALL'
        })

    '''
    GET endpoint to get questions based on category.
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
    POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.
    '''
    @app.route('/quizzes', methods=['POST'])
    def get_quizzes():
        body = request.get_json()
        previous_questions = body.get('previous_questions', None)
        quiz_category = body.get('quiz_category', None)

        try:
            cat_id = int(quiz_category['id'])
            if not any(body.values()):  # check if any falsy values
                raise ValidationError('prev_questions:[], quiz_category:{}')
            if cat_id == 0:
                query = Question.query.all()
            else:
                query = Question.query.filter(Question.category==cat_id).all()
            if query:
                question = random.choice(query)
                json_obj = jsonify({
                    'success': True,
                    'question': question.format()
                })
            else:
                abort(400)
        except (ValidationError, TypeError) as e:
            abort(400, description=e)
        finally:
            print(body)  # for debugging

        return json_obj

    '''
    error handlers for all expected errors
    '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'}), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'}), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'}), 400

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'method not allowed'}), 405

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal Server Error'}), 500

    return app
