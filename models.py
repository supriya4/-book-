import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Book(db.Model):
    __tablename__ = "books"
    isbn = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    year = db.Column(db.String, nullable=False)




class Users(db.Model):
    __tablename__ = "users"

    username = db.Column(db.String, primary_key=True)
    password = db.Column(db.String, nullable=False)

    #flight_id = db.Column(db.Integer, db.ForeignKey("flights.id"), nullable=False)
#title, isbn, review, user_name

class reviews(db.Model):
    __tablename__ = "reviews"

    title = db.Column(db.String, primary_key=True)
    isbn = db.Column(db.String, db.ForeignKey("books.isbn"), nullable=False)

    review = db.Column(db.String, nullable=False)
    user_name = db.Column(db.String,db.ForeignKey("users.username"), nullable=False)
