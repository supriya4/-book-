import os
import json
from flask import Flask, render_template, request, session, redirect, Markup, jsonify
import requests
from flask import Flask, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import Flask, render_template, request
from models import *
from sqlalchemy import or_
from sqlalchemy import func
from xml.etree import ElementTree
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://ikkeilrtrvtsxb:583d61e9b761295c17b8243b0719d99c01f60b5659da2dea536bf8d799c85da4@ec2-54-225-92-1.compute-1.amazonaws.com:5432/desr46l1jo9bdr"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Check for environment variable
#f not os.getenv("DATABASE_URL"):
    #raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.secret_key = 'key'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
db.init_app(app)



@app.route('/', methods=['GET', 'POST'])
def index():

    if session.get('username') is None:
        return redirect('/login')

    if request.method == 'GET':

        return render_template('index.html',navbar=True)

    else:
        query = request.form.get('query')
        #print(query)





        # books = db.execute('SELECT * FROM books WHERE (LOWER(isbn) LIKE :query) OR (LOWER(title) LIKE :query) '
        #                    'OR (LOWER(author) LIKE :query)',
        #                    {'query': query_like}).fetchall()
        books= Book.query.filter(or_(Book.isbn.like(f'%{query}%'),Book.title.like(f'%{query}%'),Book.author.like(f'%{query}%'))).all()
        #print(books)
        if not books:
            return 'No Books were Found!'

        return render_template('result.html', query=query, books=books,navbar=True)

    #return "Project 1: TODO"

@app.route('/login', methods=['GET', 'POST'])
def login():

    session.clear()

    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')


        user=Users.query.filter_by(username=username,password=password).first()

        if user is None:
            return 'Entered credentials not valid!'

        session["username"] = username

        return redirect('/')

    else:
        return render_template('login.html', navbar=False)



@app.route("/register",methods=['GET', 'POST'])
def register():
    """Register Form"""
    session.clear()
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        retype_password = request.form.get('retype_password')
        if not password == retype_password:
            return 'Passwords do not match'

        #check if username is available:
        av=Users.query.filter_by(username=username,password=password).first()
        if av:
            return "Choose another username"


        new_user = Users(username=request.form['username'], password=request.form['password'])

        db.session.add(new_user)
        db.session.commit()
        session['username'] = username
        return redirect('/')

    return render_template('register.html')

@app.route('/logout')
def logout():

    session.clear()

    return redirect('/')

@app.route('/books/<isbn>')
def book(isbn):
    api_key="S9vRcJAAelj6A9qh27FDQ"
    book = Book.query.filter_by(isbn=isbn).first()
    print(book)
    if not book:
        return "Error: No such Book"
    url = "https://www.goodreads.com/book/isbn/{}?key=S9vRcJAAelj6A9qh27FDQ".format(isbn)
    res = requests.get(url)
    tree = ElementTree.fromstring(res.content)

    try:
        description = tree[1][16].text
        image_url = tree[1][8].text
        review_count = tree[1][17][3].text
        avg_score = tree[1][18].text
        link = tree[1][24].text
    except IndexError:
        return render_template('book.html', book=book, link=None, navbar=True)
    description_markup = Markup(description)

    return render_template('book.html', book=book, link=link, description=description_markup,
                           image_url=image_url, review_count=review_count, avg_score=avg_score, navbar=True)


@app.route('/api/<isbn>')
def book_api(isbn):

    book = Book.query.filter_by(isbn=isbn).first()

    if book is None:
        api = jsonify({'error': 'This book is not available'})
        return api

    url = "https://www.goodreads.com/book/isbn/{}?key=S9vRcJAAelj6A9qh27FDQ".format(isbn)
    res = requests.get(url)
    tree = ElementTree.fromstring(res.content)

    try:
        description = tree[1][16].text
        image_url = tree[1][8].text
        review_count = tree[1][17][3].text
        avg_score = tree[1][18].text
        link = tree[1][24].text

    except IndexError:
        api = jsonify({
            'title': book.title,
            'author': book.author,
            'year': book.year,
            'isbn': book.isbn,
            'link': '',
            'description': '',
            'book_cover': '',
            'review_count': '',
            'average_rating': ''
        })

        return api

    api = jsonify({
        'title': book.title,
        'author': book.author,
        'year': book.year,
        'isbn': book.isbn,
        'link': link,
        'description': description,
        'book_cover': image_url,
        'review_count': review_count,
        'average_rating': avg_score
    })

    return api

@app.route('/review', methods=['GET', 'POST'])
def review():

    if request.method == 'POST':

        isbn = request.form.get('isbn')
        review = request.form.get('review')

        username = session['username']

        book = Book.query.filter_by(isbn=isbn).first()

        if book is None:
            return "Invalid ISBN Number"

        #db.execute('INSERT INTO reviews(title, isbn, review, user_name) VALUES(:title, :isbn, :review, :username)',

        #db.commit()
        av=reviews.query.filter_by(isbn=isbn).first()
        if av:
            return "already changed"
        
        new_review = reviews(title=book.title, isbn=isbn,review=review,user_name=username)
        
        db.session.add(new_review)
        db.session.commit()

        return 'Review Successfully Submitted'

    else:
        return render_template('review.html', navbar=True)



if __name__ == '__main__':
    app.run(debug=True)
