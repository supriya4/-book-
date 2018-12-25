import os

from flask import Flask, render_template, request
from models import *

app = Flask(__name__)
#app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_DATABASE_URI"]="postgres://shmhwepneylbvi:3a0e7f8640e7ddcfa9eb4223507144d14e2767bd321ecc13f49b370b50a25b0e@ec2-54-197-234-33.compute-1.amazonaws.com:5432/d6qqcov74nnqnj"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app) #tie this Database with this app

def main():
    db.create_all()

if __name__ == "__main__":
    with app.app_context():
        main()
