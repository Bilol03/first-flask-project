from flask import Flask, render_template, request, redirect
import psycopg2 as psql


app = Flask(__name__)

conn = psql.connect(database="user_list",
                    host="localhost",
                    user="postgres",
                    password="2003",
                    port="5432")
cursor = conn.cursor()




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
    print(users)
    return render_template("success.html", users = users)

