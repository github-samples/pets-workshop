import os
from functools import wraps
from typing import Dict, List, Any, Optional
from flask import Flask, jsonify, request, Response, session
from models import init_db, db, Dog, Breed, User

# Get the server directory path
base_dir: str = os.path.abspath(os.path.dirname(__file__))

app: Flask = Flask(__name__)
db_path: str = os.environ.get('DATABASE_PATH', os.path.join(base_dir, 'dogshelter.db'))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'tailspin-demo-secret-key')
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = os.environ.get('SESSION_COOKIE_SECURE', 'false').lower() == 'true'

# Initialize the database with the app
init_db(app)

def current_user() -> Optional[User]:
    user_id = session.get('user_id')
    if not user_id:
        return None
    return db.session.get(User, user_id)


def staff_required(route):
    @wraps(route)
    def wrapper(*args, **kwargs):
        user = current_user()
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        if user.role != 'staff':
            return jsonify({'error': 'Staff access required'}), 403
        return route(*args, **kwargs)
    return wrapper


@app.route('/api/auth/login', methods=['POST'])
def login() -> tuple[Response, int] | Response:
    payload = request.get_json(silent=True) or {}
    email = str(payload.get('email', '')).strip().lower()
    password = str(payload.get('password', ''))

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid email or password'}), 401

    session.clear()
    session['user_id'] = user.id
    return jsonify({'user': user.to_dict()})


@app.route('/api/auth/logout', methods=['POST'])
def logout() -> Response:
    session.clear()
    return jsonify({'ok': True})


@app.route('/api/auth/me', methods=['GET'])
def me() -> tuple[Response, int] | Response:
    user = current_user()
    if not user:
        return jsonify({'error': 'Authentication required'}), 401
    return jsonify({'user': user.to_dict()})


@app.route('/api/dogs', methods=['GET'])
def get_dogs() -> Response:
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 6, type=int)
    page = max(1, page)
    per_page = max(1, min(per_page, 100))

    query = db.session.query(
        Dog.id, 
        Dog.name, 
        Breed.name.label('breed')
    ).join(Breed, Dog.breed_id == Breed.id)
    
    total = query.count()
    dogs_query = query.offset((page - 1) * per_page).limit(per_page).all()
    
    dogs_list: List[Dict[str, Any]] = [
        {
            'id': dog.id,
            'name': dog.name,
            'breed': dog.breed
        }
        for dog in dogs_query
    ]
    
    return jsonify({
        'dogs': dogs_list,
        'page': page,
        'per_page': per_page,
        'total': total,
        'total_pages': max(1, -(-total // per_page))
    })

@app.route('/api/dogs/<int:id>', methods=['GET'])
def get_dog(id: int) -> tuple[Response, int] | Response:
    # Query the specific dog by ID and join with breed to get breed name
    dog_query = db.session.query(
        Dog.id,
        Dog.name,
        Breed.name.label('breed'),
        Dog.age,
        Dog.description,
        Dog.gender,
        Dog.status
    ).join(Breed, Dog.breed_id == Breed.id).filter(Dog.id == id).first()
    
    # Return 404 if dog not found
    if not dog_query:
        return jsonify({"error": "Dog not found"}), 404
    
    # Convert the result to a dictionary
    dog: Dict[str, Any] = {
        'id': dog_query.id,
        'name': dog_query.name,
        'breed': dog_query.breed,
        'age': dog_query.age,
        'description': dog_query.description,
        'gender': dog_query.gender,
        'status': dog_query.status.name
    }
    
    return jsonify(dog)


@app.route('/api/listing-agent/analyze', methods=['POST'])
@staff_required
def analyze_listing() -> tuple[Response, int]:
    return jsonify({'error': 'AI listing analysis is not implemented yet'}), 501


@app.route('/api/dogs', methods=['POST'])
@staff_required
def create_dog() -> tuple[Response, int]:
    return jsonify({'error': 'Listing creation is not implemented yet'}), 501

## HERE

if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('FLASK_PORT', '5100'))) # Port 5100 to avoid macOS conflicts
