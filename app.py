from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)

# security key
app.config['SECRET_KEY'] = "Bekeromo151"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///users.db"
app.config['JWT_SECRET_KEY'] = "Bekeromo151"
db = SQLAlchemy(app)
jwt = JWTManager(app)

#user class
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# create tables
with app.app_context():
    db.create_all()

# register new user
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    new_user = User(username=data['username'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'})

#registeration and get JWT
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()

    if user and user.password == data['password']:
        access_token = create_access_token(identity=user.username)
        return jsonify(access_token=access_token)

    return jsonify({'message': 'Invalid credentials'}), 401

#secure JWT
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

if __name__ == '__main__':
    app.run(debug=True)
