from flask import Flask, render_template, request, redirect
import psycopg2 as psql
import os
# from dotenv import load_dotenv

# load_dotenv()

database = os.getenv('DATABASE')
host = os.getenv('HOST')
db_user = os.getenv('DB_USER')
password = os.getenv('PASSWORD')
port = os.getenv('PORT')

password = int(password)
print(database, host, db_user, password, port)
app = Flask(__name__)

conn = psql.connect(database=database,
                    host=host,
                    user=db_user,
                    password=password,
                    port=port)



cursor = conn.cursor()

print('*Connected to the Database!')



SPORTS = ["Basketball", "Valleyball", "Football"]


@app.route("/")
def index():
    return render_template("index.html", sport=SPORTS)



@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("name")
    sport = request.form.get("sport")

    if not name and sport not in SPORTS:
        return render_template('failure.html', message="Enter your name and choose one sport please!!")
    if not name:
        return render_template('failure.html', message="Enter your name please!!")
    if not sport:
        return render_template("failure.html", message="Please choose one sport type!!!")
    if sport not in SPORTS:
        return render_template("failure.html", message="Please choose correct sport type!!!")

    cursor.execute(f"INSERT INTO users(username, sports) VALUES('{name}', '{sport}');")
    conn.commit()
    return redirect("/registered")



@app.route("/registered")
def registered():
    cursor.execute("select * from users;")
    users = cursor.fetchall()

    return render_template("success.html", users = users)


@app.route('/deregister', methods=["POST"])
def drop_user():
    user_id = request.form.get("id")
    cursor.execute(f"DELETE FROM users WHERE id={user_id};")
    return redirect("/registered")


