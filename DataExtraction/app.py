from flask import Flask, render_template
from MarvelExtraction import extract
import json
import mysql.connector
import csv

app = Flask(__name__)


@app.route('/')
def main():
    extract()
    return render_template('index.html')


@app.route('/info')
def get_movies():
    mydb = mysql.connector.connect(
        host="mysqldb",
        user="root",
        password="p@ssw0rd1",
        database="imdb"
    )
    cursor = mydb.cursor()

    cursor.execute("SELECT * FROM info")

    row_headers = [x[0] for x in cursor.description]  # this will extract row headers

    results = cursor.fetchall()
    json_data = []
    for result in results:
        json_data.append(dict(zip(row_headers, result)))

    cursor.close()

    return json.dumps(json_data[1:])


@app.route('/initdb')
def db_init():
    # connect to mysql
    mydb = mysql.connector.connect(
        host="mysqldb",
        user="root",
        password="p@ssw0rd1"
    )
    cursor = mydb.cursor()
    # creating the IMDB database
    cursor.execute("DROP DATABASE IF EXISTS imdb")
    cursor.execute("CREATE DATABASE imdb")
    cursor.close()

    # connect to the database
    mydb = mysql.connector.connect(
        host="mysqldb",
        user="root",
        password="p@ssw0rd1",
        database="imdb"
    )
    cursor = mydb.cursor()
    # creating the table
    cursor.execute("DROP TABLE IF EXISTS info")
    cursor.execute("CREATE TABLE info (movie_name VARCHAR(255), movie_year VARCHAR(255), movie_rating_type VARCHAR(255), movie_description VARCHAR(255))")
    cursor.close()

    # Inserting to table
    mydb = mysql.connector.connect(
        host="mysqldb",
        user="root",
        password="p@ssw0rd1",
        database="imdb"
    )
    cursor = mydb.cursor()

    file = open('marvel.csv')
    csvreader = csv.reader(file)
    for row in csvreader:
        movie_name = row[0]
        movie_year = row[1]
        movie_rating_type = row[2]
        movie_description = row[3]
        sql = "INSERT INTO info (movie_name, movie_year, movie_rating_type, movie_description) VALUES (%s, %s, %s, %s)"
        val = (movie_name, movie_year, movie_rating_type, movie_description)
        cursor.execute(sql, val)
    mydb.commit()
    cursor.close()

    return 'init database'
