import csv
import os
import pandas as pd
from sqlalchemy import create_engine
from flask import Flask, render_template, request
from models import *
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)
#app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
#app.config["SQLALCHEMY_DATABASE_URI"]="postgres://shmhwepneylbvi:3a0e7f8640e7ddcfa9eb4223507144d14e2767bd321ecc13f49b370b50a25b0e@ec2-54-197-234-33.compute-1.amazonaws.com:5432/d6qqcov74nnqnj"

#app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#here use your postgre database url
engine = create_engine(
"postgres://shmhwepneylbvi:3a0e7f8640e7ddcfa9eb4223507144d14e2767bd321ecc13f49b370b50a25b0e@ec2-54-197-234-33.compute-1.amazonaws.com:5432/d6qqcov74nnqnj")
db = scoped_session(sessionmaker(bind=engine))



#db.init_app(app)

def main():
    chunksize = 100
    i = 0
    j = 1
    for df in pd.read_csv("books.csv", chunksize=chunksize, iterator=True):
        #df = df.rename(columns={c: c.replace(' ', '') for c in df.columns})
        print(df)
        df.index += j
        i+=1
        df.to_sql('books', engine, if_exists='append',index=False)
        j = df.index[-1] + 1

if __name__ == "__main__":
    with app.app_context():
        main()
