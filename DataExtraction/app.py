from flask import Flask, render_template, jsonify
from MarvelExtraction import extract
import mysql.connector
import csv

app = Flask(__name__)


@app.route('/')
def main():
    extract()
    return render_template('index.html')


@app.route('/info')
def get_movies():
    cursor = None
    try:
        mydb = mysql.connector.connect(
            host="mysqldb",
            user="root",
            password="p@ssw0rd1",
            database="imdb"
        )
        cursor = mydb.cursor()

        cursor.execute("SELECT * FROM info")
        row_headers = [x[0] for x in cursor.description]

        results = cursor.fetchall()
        json_data = [dict(zip(row_headers, result)) for result in results]

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)})

    finally:
        if cursor:
            cursor.close()
        if mydb:
            mydb.close()

    return jsonify(json_data)


@app.route('/initdb')
def db_init():
    cursor = None
    mydb = None
    try:
        # connect to mysql and create the database
        mydb = mysql.connector.connect(
            host="mysqldb",
            user="root",
            password="p@ssw0rd1"
        )
        cursor = mydb.cursor()
        cursor.execute("DROP DATABASE IF EXISTS imdb")
        cursor.execute("CREATE DATABASE imdb")

        # connect to the new database and create the table
        mydb.database = "imdb"
        cursor.execute("DROP TABLE IF EXISTS info")
        cursor.execute("""
            CREATE TABLE info (
                movie_name VARCHAR(255),
                movie_year VARCHAR(255),
                movie_rating_type VARCHAR(255),
                movie_description TEXT
            )
        """)

        # Insert data from CSV
        with open('marvel.csv') as file:
            csvreader = csv.reader(file)
            # Skip header row if there is one
            next(csvreader)
            for row in csvreader:
                sql = """
                    INSERT INTO info (movie_name, movie_year, movie_rating_type, movie_description)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(sql, tuple(row))

        mydb.commit()
    except mysql.connector.Error as err:
        return f"Error: {str(err)}"
    finally:
        if cursor:
            cursor.close()
        if mydb:
            mydb.close()

    return 'Database initialized'


if __name__ == '__main__':
    app.run(debug=True)
