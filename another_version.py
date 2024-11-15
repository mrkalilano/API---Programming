from flask import Flask, jsonify, request
from http import HTTPStatus
import mysql.connector

app = Flask(__name__)

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'library'
}

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

@app.route('/api/books', methods=['GET'])
def get_books():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify({'success': True, 'data': books, 'total': len(books)}), HTTPStatus.OK

@app.route('/api/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM books WHERE id = %s", (book_id,))
    book = cursor.fetchone()
    cursor.close()
    conn.close()
    if book:
        return jsonify({'success': True, 'data': book}), HTTPStatus.OK
    return jsonify({'success': False, 'error': 'Book not found'}), HTTPStatus.NOT_FOUND

@app.route('/api/books', methods=['POST'])
def create_book():
    if not request.json:
        return jsonify({'success': False, 'error': 'Request must be JSON'}), HTTPStatus.BAD_REQUEST

    data = request.json
    required_fields = ['title', 'author', 'year']
    for field in required_fields:
        if field not in data:
            return jsonify({'success': False, 'error': f'{field} is required'}), HTTPStatus.BAD_REQUEST

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO books (title, author, year)
        VALUES (%s, %s, %s)
    """, (data['title'], data['author'], data['year']))
    conn.commit()
    new_book_id = cursor.lastrowid
    cursor.close()
    conn.close()

    return jsonify({'success': True, 'data': {'id': new_book_id, **data}}), HTTPStatus.CREATED