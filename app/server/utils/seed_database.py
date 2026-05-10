import csv
import os
import sys
import random
from datetime import datetime, timedelta
from collections import defaultdict

# Add the parent directory to sys.path to allow importing from models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask
from models import init_db, db, Breed, Dog, User
from models.dog import AdoptionStatus

def create_app():
    """Create and configure Flask app for database operations"""
    app = Flask(__name__)
    
    # Get the server directory path (one level up from utils)
    server_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    db_path = os.environ.get('DATABASE_PATH', os.path.join(server_dir, 'dogshelter.db'))
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize the database with the app
    init_db(app)
    
    return app

def create_breeds():
    """Seed the database with breeds from the CSV file"""
    app = create_app()
    
    # Path to the CSV file
    csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                           'models', 'breeds.csv')
    
    with app.app_context():
        # Check if breeds already exist
        existing_breeds = Breed.query.count()
        if existing_breeds > 0:
            print(f"Database already contains {existing_breeds} breeds. Skipping seed.")
            return
        
        # Read the CSV file and add breeds to the database
        with open(csv_path, 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                breed = Breed(name=row['Breed'], description=row['Description'])
                db.session.add(breed)
            
            # Commit the changes
            db.session.commit()
            
        # Verify the seeding
        breed_count = Breed.query.count()
        print(f"Successfully seeded {breed_count} breeds to the database.")

def create_dogs():
    """Seed the database with dogs from the CSV file, ensuring at least 3 dogs per breed"""
    app = create_app()
    
    # Path to the CSV file
    csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                           'models', 'dogs.csv')
    
    with app.app_context():
        # Check if dogs already exist
        existing_dogs = Dog.query.count()
        if existing_dogs > 0:
            print(f"Database already contains {existing_dogs} dogs. Skipping seed.")
            return
        
        # Get all breeds from the database
        breeds = Breed.query.all()
        if not breeds:
            print("No breeds found in database. Please seed breeds first.")
            return
        
        # Track how many dogs are assigned to each breed
        breed_counts = defaultdict(int)
        
        # Read the CSV file
        dogs_data = []
        with open(csv_path, 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                dogs_data.append(row)
        
        def create_dog(dog_info, breed_id):
            """Helper function to create a dog with consistent attributes"""
            dog = Dog(
                name=dog_info['Name'],
                description=dog_info['Description'],
                breed_id=breed_id,
                age=int(dog_info['Age']),
                gender=dog_info['Gender'],
                status=random.choice(list(AdoptionStatus)),
                intake_date=datetime.now() - timedelta(days=random.randint(1, 365))
            )
            db.session.add(dog)
            breed_counts[breed_id] += 1
            return dog
        
        # First pass: assign at least 3 dogs to each breed
        for breed in breeds:
            # Get 3 random dogs that haven't been assigned yet
            for _ in range(3):
                if not dogs_data:
                    break
                
                dog_info = random.choice(dogs_data)
                dogs_data.remove(dog_info)
                
                create_dog(dog_info, breed.id)
        
        # Second pass: assign remaining dogs randomly
        for dog_info in dogs_data:
            breed = random.choice(breeds)
            create_dog(dog_info, breed.id)
        
        # Commit all the changes
        db.session.commit()
        
        # Verify the seeding
        dog_count = Dog.query.count()
        print(f"Successfully seeded {dog_count} dogs to the database.")
        
        # Print distribution of dogs across breeds
        for breed in breeds:
            count = breed_counts[breed.id]
            print(f"Breed '{breed.name}': {count} dogs")

def create_staff_user():
    """Seed a staff user for the upload demo."""
    app = create_app()
    email = os.environ.get('DEMO_STAFF_EMAIL', 'staff@tailspin.example').strip().lower()
    password = os.environ.get('DEMO_STAFF_PASSWORD', 'TailspinDemo123!')

    with app.app_context():
        user = User.query.filter_by(email=email).first()
        if user:
            user.role = 'staff'
            if os.environ.get('DEMO_STAFF_PASSWORD'):
                user.set_password(password)
            db.session.commit()
            print(f"Staff user '{email}' already exists. Ensured staff role.")
            return

        user = User(email=email, role='staff')
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        print(f"Successfully seeded staff user '{email}'.")

def seed_database():
    """Run all seeding functions in the correct order"""
    create_breeds()
    create_dogs()
    create_staff_user()

if __name__ == '__main__':
    seed_database()
