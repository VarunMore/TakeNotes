from flask import Flask, render_template, request, redirect
from flask.helpers import url_for
from mysql import connector



app = Flask(__name__)
app.config['SECRET_KEY']='supersecretKey'

db = connector.connect(
  host="localhost",
  user="root",
  password="",
  database="note_db"
)


@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method =="POST":
        title = request.form["title"]
        note = request.form["note"]
        mycursor = db.cursor()
        mycursor.execute("INSERT INTO note_table (title, note) VALUES (%s, %s)", (title, note))
        db.commit()
  
    mycursor = db.cursor()
    mycursor.execute("SELECT id, title, note FROM note_table")
    myresult = mycursor.fetchall()
    return render_template("index.html", myresult=myresult )



@app.route("/delete/<int:id>")
def delete(id):  
    mycursor = db.cursor()
    mycursor.execute("DELETE FROM note_table WHERE id = %s ", (id,))
    db.commit()
    return redirect(url_for('index'))
    # redirect(url_for('index'))

@app.route("/update/<int:id>", methods=['POST','GET'])
def update(id):  
    if request.method == "POST":
        mycursor = db.cursor()
        title = request.form["title"]
        note = request.form["note"]
        mycursor = db.cursor()
        mycursor.execute("UPDATE note_table SET title = %s  WHERE id = %s ", (title, id))
        mycursor.execute("UPDATE note_table SET note = %s  WHERE id = %s ", (note, id))
        db.commit()
        return redirect(url_for('index'))
    mycursor = db.cursor()
    mycursor.execute("SELECT title, note FROM note_table WHERE id = %s ", (id,))
    result = mycursor.fetchall()
    return render_template('update.html', result = result)  

if __name__ == "__main__":
    app.run(debug=True)