---
applyTo: "**/app.py"
---

# Flask API Guidelines for Tailspin Shelter

Essential patterns for writing Flask endpoints with SQLAlchemy in the Tailspin Shelter backend.

## Core Principles

1. **Type Hints** - Use Python type hints for all functions
2. **RESTful Design** - Follow `/api/` prefix conventions  
3. **Error Handling** - Return proper HTTP status codes with JSON
4. **SQLAlchemy ORM** - Use ORM queries, avoid raw SQL

## Basic Structure

```python
from typing import Dict, List, Any
from flask import Flask, jsonify, Response, request
from models import db, Dog, Breed

@app.route('/api/resource', methods=['GET'])
def get_resource() -> Response:
    try:
        results = db.session.query(Model).all()
        data: List[Dict[str, Any]] = [
            {'id': item.id, 'name': item.name} for item in results
        ]
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500
```

## GET Endpoints

### List Resources
```python
@app.route('/api/dogs', methods=['GET'])
def get_dogs() -> Response:
    query = db.session.query(
        Dog.id, Dog.name, Breed.name.label('breed')
    ).join(Breed, Dog.breed_id == Breed.id)
    
    dogs_list: List[Dict[str, Any]] = [
        {'id': dog.id, 'name': dog.name, 'breed': dog.breed}
        for dog in query.all()
    ]
    return jsonify(dogs_list)
```

### Single Resource
```python
@app.route('/api/dogs/<int:id>', methods=['GET'])
def get_dog(id: int) -> tuple[Response, int] | Response:
    dog_query = db.session.query(
        Dog.id, Dog.name, Breed.name.label('breed'),
        Dog.age, Dog.description, Dog.status
    ).join(Breed, Dog.breed_id == Breed.id).filter(Dog.id == id).first()
    
    if not dog_query:
        return jsonify({"error": "Dog not found"}), 404
    
    return jsonify({
        'id': dog_query.id,
        'name': dog_query.name,
        'breed': dog_query.breed,
        'age': dog_query.age,
        'status': dog_query.status.name
    })
```

## POST - Create Resource
```python
@app.route('/api/dogs', methods=['POST'])
def create_dog() -> tuple[Response, int] | Response:
    try:
        data = request.get_json()
        
        if not data or 'name' not in data or 'breed_id' not in data:
            return jsonify({"error": "Missing required fields: name, breed_id"}), 400
        
        new_dog = Dog(
            name=data['name'],
            breed_id=data['breed_id'],
            age=data.get('age'),
            description=data.get('description')
        )
        
        db.session.add(new_dog)
        db.session.commit()
        
        return jsonify({
            'id': new_dog.id,
            'name': new_dog.name,
            'message': 'Dog created successfully'
        }), 201
        
    except ValueError as e:
        db.session.rollback()
        return jsonify({"error": f"Validation error: {str(e)}"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500
```

## PUT - Update Resource
```python
@app.route('/api/dogs/<int:id>', methods=['PUT'])
def update_dog(id: int) -> tuple[Response, int] | Response:
    try:
        dog = Dog.query.get(id)
        if not dog:
            return jsonify({"error": "Dog not found"}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Update fields if provided
        for field in ['name', 'age', 'description']:
            if field in data:
                setattr(dog, field, data[field])
        
        db.session.commit()
        return jsonify({'id': dog.id, 'message': 'Dog updated successfully'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500
```

## DELETE - Remove Resource
```python
@app.route('/api/dogs/<int:id>', methods=['DELETE'])
def delete_dog(id: int) -> tuple[Response, int] | Response:
    try:
        dog = Dog.query.get(id)
        if not dog:
            return jsonify({"error": "Dog not found"}), 404
        
        db.session.delete(dog)
        db.session.commit()
        return jsonify({"message": "Dog deleted successfully"})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500
```

## Common Patterns

### Query Examples
```python
# Join query
query = db.session.query(Dog.id, Breed.name.label('breed')).join(Breed)

# Filtered query
dogs = Dog.query.filter(Dog.status == AdoptionStatus.AVAILABLE).all()

# Pagination
page = request.args.get('page', 1, type=int)
dogs = Dog.query.paginate(page=page, per_page=10, error_out=False)
```

### Input Validation
```python
def validate_dog_data(data: Dict[str, Any]) -> Optional[str]:
    if not data.get('name') or len(data['name'].strip()) < 2:
        return "Name must be at least 2 characters"
    if 'age' in data and (not isinstance(data['age'], int) or data['age'] < 0):
        return "Age must be a positive integer"
    return None
```

### Error Responses
```python
# Standard status codes
return jsonify({"error": "Invalid input"}), 400        # Bad Request
return jsonify({"error": "Not found"}), 404            # Not Found
return jsonify({"error": "Internal error"}), 500       # Server Error

# Transaction safety
try:
    db.session.commit()
except Exception:
    db.session.rollback()
    return jsonify({"error": "Operation failed"}), 500
```

## Key Patterns

- **Type hints** for all function parameters and returns
- **JSON responses** with `jsonify()` and proper status codes  
- **Error handling** with try/catch and rollback on failures
- **Input validation** before database operations
- **RESTful URLs** following `/api/resource` patterns
- **SQLAlchemy ORM** with joins and filters, not raw SQL
