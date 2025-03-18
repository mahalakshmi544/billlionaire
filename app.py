from flask import Flask, jsonify, request, render_template, redirect, url_for
from utils.db import db
from models.data import *
from flask_sqlalchemy import SQLAlchemy

flask_app = Flask(__name__)
flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

db.init_app(flask_app)

# Create tables
with flask_app.app_context():
    db.create_all()


@flask_app.route('/')
def index():
    data = Business.query.all()
    return render_template('index.html', content=data)


@flask_app.route('/help')
def help_page():
    return render_template('help.html')


@flask_app.route('/modify')
def modify():
    data = Business.query.all()
    return render_template('modify.html', content2=data)

@flask_app.route('/elon_mask')
def elon_mask():
    return render_template('elon_mask.html')

@flask_app.route('/Bernard')
def Bernard():
    return render_template('Bernard.html')

@flask_app.route('/jeffbezos')
def jeffbezos():
    return render_template('jeffbezos.html')

@flask_app.route('/larryellison')
def larryellison():
    return render_template('larryellison.html')


@flask_app.route('/warrenbuffet')
def  warrenbuffet():
    return render_template('warrenbuffet.html')

@flask_app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@flask_app.route('/about-us')
def about():
    return render_template('about-us.html')


@flask_app.route('/add_data')
def add_data():
    return render_template('add_data.html')


@flask_app.route('/register')
def register_page():
    return render_template('register.html')


@flask_app.route('/submit', methods=['POST'])
def submit():
    try:
        form_data = request.form.to_dict()
        print(f"form_data: {form_data}")

        # Person data
        personName = form_data.get('personName')
        age = form_data.get('age')
        gender = form_data.get('gender')
        birthdate = form_data.get('birthdate')
        city = form_data.get('city')
        state = form_data.get('state')
        country = form_data.get('country')

        # Business data
        rank = form_data.get('rank')
        source = form_data.get('source')
        finalWorth = form_data.get('finalWorth')
        category = form_data.get('category')
        organization = form_data.get('organization')
        industries = form_data.get('industries')
        title = form_data.get('title')

        # Check if person exists
        person = Person.query.filter_by(personName=personName).first()
        if not person:
            person = Person(
                personName=personName,
                age=age,
                gender=gender,
                birthdate=birthdate,
                city=city,
                state=state,
                country=country,
            )
            db.session.add(person)
            db.session.commit()

        # Add Business
        business = Business(
            rank=rank,
            source=source,
            finalWorth=finalWorth,
            category=category,
            organization=organization,
            industries=industries,
            title=title,
            person_id=person.id,
        )
        db.session.add(business)
        db.session.commit()
        print("Submitted successfully")
        return redirect(url_for('index'))
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@flask_app.route('/register-user', methods=['POST'])
def register_user():
    try:
        form_data = request.form.to_dict()
        print(f"form_data: {form_data}")

        name = form_data.get('name')
        mobile_no = form_data.get('mobile_no')
        email_id = form_data.get('email_id')
        password = form_data.get('password')

        # Check if user already exists
        if Register.query.filter_by(email_id=email_id).first():
            return jsonify({"message": "User already exists"}), 400

        # Register new user
        user = Register(name=name, mobile_no=mobile_no, email_id=email_id, password=password)
        db.session.add(user)
        db.session.commit()
        print("Registered successfully")
        return redirect(url_for('add_data'))
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@flask_app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    try:
        data = Business.query.get_or_404(id)
        print(data.person.id)

        if request.method == 'POST':
            # Update person data
            data.person.personName = request.form['personName']
            data.person.age = request.form['age']
            data.person.gender = request.form['gender']
            data.person.birthdate = request.form['birthdate']
            data.person.city = request.form['city']
            data.person.state = request.form['state']
            data.person.country = request.form['country']

            # Update business data
            data.rank = request.form['rank']
            data.source = request.form['source']
            data.finalWorth = request.form['finalWorth']
            data.category = request.form['category']
            data.organization = request.form['organization']
            data.industries = request.form['industries']
            data.title = request.form['title']

            db.session.commit()
            print("Updated successfully")
            return redirect(url_for('modify'))

        return render_template('update.html', data=data)
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500



@flask_app.route('/delete/<int:id>', methods=['GET', 'DELETE'])
def delete_user(id):
    data = Business.query.get(id)
    print("task: {}".format(data))

    if not data:
        return jsonify({'message': 'task not found'}), 404
    try:
        db.session.delete(data)
        db.session.commit()
        return jsonify({'message': 'task deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'An error occurred while deleting the data {}'.format(e)}), 500




if __name__ == '__main__':
    flask_app.run(host='127.0.0.1', port=8005, debug=True)
