from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "Secret Key"

# Configures with mysqp
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/cmsc447project'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Creates data table
class Data(db.Model):
    county = db.Column(db.String(100), primary_key = True)
    vacs_complete = db.Column(db.String(100))
    vacs_complete_per = db.Column(db.String(100))
    house = db.Column(db.String(100))

    def __init__(self, county, vacs_complete, vacs_complete_per, house):
        self.county = county
        self.vacs_complete = vacs_complete
        self.vacs_complete_per = vacs_complete_per
        self.house = house

# Route path for all CRUD queries
@app.route('/')
def Index():
    all_data = Data.query.all()
    return render_template("index.html", county = all_data)

# Adds county
@app.route('/add', methods = ['POST'])
def add():
    if request.method == 'POST':
        county = request.form['county']
        vacs_complete = request.form['vacs_complete']
        vacs_complete_per = request.form['vacs_complete_per']
        house = request.form['house']
        my_data = Data(county, vacs_complete, vacs_complete_per, house)
        db.session.add(my_data)
        db.session.commit()
        return redirect(url_for('Index'))

# Updates county
@app.route('/update', methods = ['GET', 'POST'])
def update():
    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('county'))
        my_data.vacs_complete = request.form['vacs_complete']
        my_data.vacs_complete_per = request.form['vacs_complete_per']
        house = request.form['house']
        db.session.commit()
        return redirect(url_for('Index'))

# Deletes county
@app.route('/delete/<county>/', methods = ['GET', 'POST'])
def delete(county):
    my_data = Data.query.get(county)
    db.session.delete(my_data)
    db.session.commit()
    return redirect(url_for('Index'))

if __name__ == "__main__":
    app.run(debug=True)