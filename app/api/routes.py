from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Library, lib_schema, libs_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'read': 'books'}

# @api.route('/data')
# def viewdata():
#     data = get_contact()
#     response = jsonify(data)
#     print(response)
#     return render_template('index.html', data = data)

@api.route('/ebooks', methods = ['POST'])
@token_required
def create_book(current_user_token):
    isbn = request.json['isbn']
    book_title = request.json['book_title']
    author_name = request.json['author_name']
    book_length = request.json['book_length']
    publisher = request.json['publisher']
    book_format = request.json['book_format']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    digital_library = Library(isbn, book_title, author_name, book_length, publisher, book_format, user_token = user_token )

    db.session.add(digital_library)
    db.session.commit()

    response = lib_schema.dump(digital_library)
    return jsonify(response)

@api.route('/ebooks', methods = ['GET'])
@token_required
def retrieve_single_book(current_user_token):
    _book = current_user_token.token
    libs = Library.query.filter_by(user_token = _book).all()
    response = libs_schema.dump(libs)
    return jsonify(response)

@api.route('/ebooks/<id>', methods = ['GET'])
@token_required
def retrieve_all_books(current_user_token, id):
    fan = current_user_token.token
    if fan == current_user_token.token:
        digital_library = Library.query.get(id)
        response = lib_schema.dump(digital_library)
        return jsonify(response)
    else:
        return jsonify({"message": "Valid Token Required"}),401

# UPDATE endpoint
@api.route('/ebooks/<id>', methods = ['POST','PUT'])
@token_required
def update_book(current_user_token,id):
    digital_library = Library.query.get(id) 
    digital_library.isbn = request.json['isbn']
    digital_library.book_title = request.json['book_title']
    digital_library.author_name = request.json['author_name']
    digital_library.book_length = request.json['book_length']
    digital_library.publisher = request.json['publisher']
    digital_library.book_format = request.json['book_format']
    digital_library.user_token = current_user_token.token

    db.session.commit()
    response = lib_schema.dump(digital_library)
    return jsonify(response)


# DELETE book ENDPOINT
@api.route('/ebooks/<id>', methods = ['DELETE'])
@token_required
def delete_book(current_user_token, id):
    digital_library = Library.query.get(id)
    db.session.delete(digital_library)
    db.session.commit()
    response = lib_schema.dump(digital_library)
    return jsonify(response)