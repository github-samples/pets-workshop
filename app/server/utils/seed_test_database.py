"""Seed a test database with deterministic data for e2e tests.

Creates a fresh SQLite database with a small set of known dogs and breeds.
The database path defaults to server/e2e_test_dogshelter.db but can be
overridden via the DATABASE_PATH environment variable.
"""
import os
import sys

# Add the parent directory to sys.path to allow importing from models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask
from models import init_db, db, Breed, Dog, User
from models.dog import AdoptionStatus

# Server directory (parent of utils/)
_server_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Test breeds
TEST_BREEDS = [
    {'name': 'Golden Retriever', 'description': 'Family-friendly, smart, and easy to train.'},
    {'name': 'Husky', 'description': 'Beautiful and energetic, but needs lots of exercise.'},
    {'name': 'German Shepherd', 'description': 'Intelligent, loyal, great family protector.'},
]

# Test dogs — deterministic data matching e2e test expectations
# First 3 dogs (Buddy, Luna, Max) must stay in order for existing homepage tests
TEST_DOGS = [
    {
        'name': 'Buddy',
        'breed': 'Golden Retriever',
        'age': 3,
        'gender': 'Male',
        'status': AdoptionStatus.AVAILABLE,
        'description': 'A friendly and loyal companion who loves to play fetch.',
    },
    {
        'name': 'Luna',
        'breed': 'Husky',
        'age': 2,
        'gender': 'Female',
        'status': AdoptionStatus.PENDING,
        'description': 'An energetic and playful dog who loves the outdoors.',
    },
    {
        'name': 'Max',
        'breed': 'German Shepherd',
        'age': 5,
        'gender': 'Male',
        'status': AdoptionStatus.ADOPTED,
        'description': 'A loyal and protective dog, great with families.',
    },
    {
        'name': 'Bella',
        'breed': 'Golden Retriever',
        'age': 1,
        'gender': 'Female',
        'status': AdoptionStatus.AVAILABLE,
        'description': 'A playful puppy who loves belly rubs.',
    },
    {
        'name': 'Charlie',
        'breed': 'Husky',
        'age': 4,
        'gender': 'Male',
        'status': AdoptionStatus.AVAILABLE,
        'description': 'A gentle giant who gets along with everyone.',
    },
    {
        'name': 'Daisy',
        'breed': 'German Shepherd',
        'age': 3,
        'gender': 'Female',
        'status': AdoptionStatus.PENDING,
        'description': 'Smart and eager to learn new tricks.',
    },
    {
        'name': 'Rocky',
        'breed': 'Golden Retriever',
        'age': 6,
        'gender': 'Male',
        'status': AdoptionStatus.AVAILABLE,
        'description': 'A calm and patient dog, perfect for families with kids.',
    },
    {
        'name': 'Sadie',
        'breed': 'Husky',
        'age': 2,
        'gender': 'Female',
        'status': AdoptionStatus.AVAILABLE,
        'description': 'Loves running and playing in the snow.',
    },
    {
        'name': 'Duke',
        'breed': 'German Shepherd',
        'age': 4,
        'gender': 'Male',
        'status': AdoptionStatus.PENDING,
        'description': 'A confident and courageous companion.',
    },
    {
        'name': 'Molly',
        'breed': 'Golden Retriever',
        'age': 5,
        'gender': 'Female',
        'status': AdoptionStatus.ADOPTED,
        'description': 'A sweet and affectionate dog who loves cuddles.',
    },
]


def seed_test_database():
    """Create a fresh test database with deterministic data."""
    db_path = os.environ.get('DATABASE_PATH', os.path.join(_server_dir, 'e2e_test_dogshelter.db'))

    # Remove existing test database to start fresh
    if os.path.exists(db_path):
        os.remove(db_path)

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    init_db(app)

    with app.app_context():
        # Seed breeds
        breed_map = {}
        for breed_data in TEST_BREEDS:
            breed = Breed(name=breed_data['name'], description=breed_data['description'])
            db.session.add(breed)
            db.session.flush()  # Get the ID
            breed_map[breed_data['name']] = breed.id

        # Seed dogs
        for dog_data in TEST_DOGS:
            dog = Dog(
                name=dog_data['name'],
                breed_id=breed_map[dog_data['breed']],
                age=dog_data['age'],
                gender=dog_data['gender'],
                status=dog_data['status'],
                description=dog_data['description'],
            )
            db.session.add(dog)

        staff_user = User(
            email=os.environ.get('DEMO_STAFF_EMAIL', 'staff@tailspin.example').strip().lower(),
            role='staff',
        )
        staff_user.set_password(os.environ.get('DEMO_STAFF_PASSWORD', 'TailspinDemo123!'))
        db.session.add(staff_user)

        db.session.commit()

    print(f'Test database seeded at {db_path}')
    print(f'  Breeds: {len(TEST_BREEDS)}')
    print(f'  Dogs: {len(TEST_DOGS)}')


if __name__ == '__main__':
    seed_test_database()
