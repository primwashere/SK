from flask import Flask, jsonify, request
import json

app=Flask(__name__)

#OTWARCIE PLIKU
with open('books.json') as json_data:
    result = []
    data = json.load(json_data)
    for book in data['books']:
        result.append(book['isbn'])
#PUNKT 3
@app.route("/titles", methods=['GET'])
def titles_list():
    result=[]
    for book in data['books']:
        result.append(book['title'])
    return result

# PUNKT 4
@app.errorhandler(404)
def not_found(url, error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + url,
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp


@app.route("/titles/<isbn>", methods=['GET'])
def all(isbn):
    for book in data['books']:
        if book['isbn'] == isbn:    
            return jsonify(book)

    return not_found(url=isbn)

#PUNKT 5 
@app.route('/descriptions/<expression>', methods = ['GET'])
def search_descriptions(expression):
    descriptions = [book['description'] for book in data['books'] if expression.lower() in book['title'].lower()]
    return jsonify(descriptions)

#PUNKT 6
@app.route('/titles/<isbn>', methods=['PUT'])
def change_author(isbn):
    new_author = request.args.get('author')

    if not new_author:
        response = jsonify('Prosze podac autora jako argument.')
        status_code = 400
    else:
        book_found = False
        for book in data['books']:
            if book['isbn'] == isbn:
                book['author'] = new_author
                book_found = True
                break

        if book_found:
            response = jsonify(f'Autor ksiazki zostal zmieniony na {new_author}.')
            status_code = 200
        else:
            response = jsonify(f'Ksiazka o podanym numerze nie zostala znaleziona.')
            status_code = 404

    return response, status_code


if __name__ == "__main__":
    app.run(debug=True)








