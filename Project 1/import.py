import os
import csv
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy.orm import scoped_session, sessionmaker

# Set up database
engine = create_engine("postgres://yqlsjmtgyyfpom:9b2b85302178bb9ae7e0f81039c0c7434da70828cbbd0eb934ccd575306418ba@ec2-54-228-207-163.eu-west-1.compute.amazonaws.com:5432/dd6ka57go42p9n")
db = scoped_session(sessionmaker(bind=engine))


with open('books.csv', mode='r') as books:
    csv_reader = csv.DictReader(books)
    for row in csv_reader:
        ISBN = row['isbn']
        Title = row['title']
        author = row['author']
        puplishYear = row['year']
        db.get_bind().execute(text("INSERT INTO books (isbn, title, author, year)" + "VALUES(:isbn, :title, :author, :year)"), isbn=ISBN, title=Title, author=author, year=puplishYear)