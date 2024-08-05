from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Book, book_schema, books_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'soo': 'I am almost finished with all my Module work!!!'}


# ------------------------------------------------------------------------------------------------------------------------------------------->

# Create a book
@api.route('/books', methods = ['POST'])
@token_required
def create_book(current_user_token):
    title = request.json['title']
    author = request.json['author']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    book = Book(title, author, user_token = user_token )

    db.session.add(book)
    db.session.commit()

    response = book_schema.dump(book)
    return jsonify(response)

# ------------------------------------------------------------------------------------------------------------------------------------------->

# Fetch all books
@api.route('/books', methods = ['GET'])
@token_required
def get_books(current_user_token):
    a_user = current_user_token.token
    books = Book.query.filter_by(user_token = a_user).all()
    response = books_schema.dump(books)
    return jsonify(response)

# ------------------------------------------------------------------------------------------------------------------------------------------->

# Fetch a single book
@api.route('/books/<id>', methods = ['GET'])
@token_required
def get_book(current_user_token, id):
    fan = current_user_token.token
    if fan == current_user_token.token:
        book = Book.query.get(id)
        response = book_schema.dump(book)
        return jsonify(response)
    else:
        return jsonify({"message": "Valid Token Required"}),401


# ------------------------------------------------------------------------------------------------------------------------------------------->

# Update a single book
@api.route('/books/<id>', methods = ['POST','PUT'])
@token_required
def update_book(current_user_token,id):
    book = Book.query.get(id)
    book.title = request.json['title']
    book.author = request.json['author']
    book.user_token = current_user_token.token

    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)

# ------------------------------------------------------------------------------------------------------------------------------------------->

# Delete a single book
@api.route('/books/<id>', methods = ['DELETE'])
@token_required
def delete_book(current_user_token, id):
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)