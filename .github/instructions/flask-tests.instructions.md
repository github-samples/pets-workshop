---
applyTo: "**/test_*.py"
---

# Flask Testing Guidelines for Tailspin Shelter

Essential patterns for writing unit tests for Flask APIs using Python's unittest framework.

## Core Principles

1. **Mock Database Queries** - Use `unittest.mock` to isolate API logic
2. **Test HTTP Responses** - Verify status codes, JSON structure, error messages
3. **Helper Methods** - Create reusable mock objects and setup methods

## Basic Test Structure

```python
import unittest
from unittest.mock import patch, MagicMock
import json
from app import app

class TestDogAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        app.config['TESTING'] = True
```

## Testing GET Endpoints

### List Endpoint
```python
@patch('app.db.session.query')
def test_get_dogs_success(self, mock_query):
    # Setup mock
    mock_dog = MagicMock()
    mock_dog.id = 1
    mock_dog.name = "Buddy"
    mock_dog.breed = "Golden Retriever"
    
    mock_query_instance = MagicMock()
    mock_query.return_value = mock_query_instance
    mock_query_instance.join.return_value = mock_query_instance
    mock_query_instance.all.return_value = [mock_dog]
    
    response = self.app.get('/api/dogs')
    
    self.assertEqual(response.status_code, 200)
    data = json.loads(response.data)
    self.assertEqual(len(data), 1)
    self.assertEqual(data[0]['name'], "Buddy")
```

### Single Resource
```python
@patch('app.db.session.query')
def test_get_dog_by_id_success(self, mock_query):
    mock_dog = MagicMock()
    mock_dog.id = 1
    mock_dog.name = "Buddy"
    mock_dog.status.name = "AVAILABLE"
    
    mock_query_instance = MagicMock()
    mock_query.return_value = mock_query_instance
    mock_query_instance.join.return_value = mock_query_instance
    mock_query_instance.filter.return_value = mock_query_instance
    mock_query_instance.first.return_value = mock_dog
    
    response = self.app.get('/api/dogs/1')
    
    self.assertEqual(response.status_code, 200)
    data = json.loads(response.data)
    self.assertEqual(data['name'], "Buddy")

@patch('app.db.session.query')
def test_get_dog_not_found(self, mock_query):
    mock_query_instance = MagicMock()
    mock_query.return_value = mock_query_instance
    mock_query_instance.join.return_value = mock_query_instance
    mock_query_instance.filter.return_value = mock_query_instance
    mock_query_instance.first.return_value = None
    
    response = self.app.get('/api/dogs/999')
    
    self.assertEqual(response.status_code, 404)
    data = json.loads(response.data)
    self.assertEqual(data['error'], "Dog not found")
```

## Testing POST Endpoints

```python
@patch('app.db.session')
@patch('app.Dog')
def test_create_dog_success(self, mock_dog_class, mock_session):
    mock_dog_instance = MagicMock()
    mock_dog_instance.id = 1
    mock_dog_instance.name = "New Dog"
    mock_dog_class.return_value = mock_dog_instance
    
    dog_data = {'name': 'New Dog', 'breed_id': 1, 'age': 2}
    
    response = self.app.post('/api/dogs', 
                           data=json.dumps(dog_data),
                           content_type='application/json')
    
    self.assertEqual(response.status_code, 201)
    data = json.loads(response.data)
    self.assertEqual(data['name'], "New Dog")
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()

def test_create_dog_missing_fields(self):
    dog_data = {'name': 'Incomplete Dog'}  # Missing breed_id
    
    response = self.app.post('/api/dogs',
                           data=json.dumps(dog_data),
                           content_type='application/json')
    
    self.assertEqual(response.status_code, 400)
    data = json.loads(response.data)
    self.assertIn('Missing required fields', data['error'])
```

## Testing PUT/DELETE Endpoints

```python
@patch('app.Dog.query')
@patch('app.db.session')
def test_update_dog_success(self, mock_session, mock_query):
    mock_dog = MagicMock()
    mock_dog.id = 1
    mock_query.get.return_value = mock_dog
    
    update_data = {'name': 'Updated Name', 'age': 4}
    
    response = self.app.put('/api/dogs/1',
                          data=json.dumps(update_data),
                          content_type='application/json')
    
    self.assertEqual(response.status_code, 200)
    self.assertEqual(mock_dog.name, "Updated Name")
    mock_session.commit.assert_called_once()

@patch('app.Dog.query')
@patch('app.db.session')
def test_delete_dog_success(self, mock_session, mock_query):
    mock_dog = MagicMock()
    mock_query.get.return_value = mock_dog
    
    response = self.app.delete('/api/dogs/1')
    
    self.assertEqual(response.status_code, 200)
    mock_session.delete.assert_called_once_with(mock_dog)
    mock_session.commit.assert_called_once()
```

## Error Handling Tests

```python
@patch('app.db.session')
def test_database_error_handling(self, mock_session):
    mock_session.commit.side_effect = Exception("Database error")
    
    dog_data = {'name': 'Test Dog', 'breed_id': 1}
    
    response = self.app.post('/api/dogs',
                           data=json.dumps(dog_data),
                           content_type='application/json')
    
    self.assertEqual(response.status_code, 500)
    data = json.loads(response.data)
    self.assertIn('Internal server error', data['error'])
    mock_session.rollback.assert_called_once()
```

## Helper Methods

```python
def _create_mock_dog(self, dog_id: int, name: str, breed: str):
    mock_dog = MagicMock()
    mock_dog.id = dog_id
    mock_dog.name = name
    mock_dog.breed = breed
    mock_dog.status.name = "AVAILABLE"
    return mock_dog

def _setup_query_mock(self, mock_query, return_data):
    mock_query_instance = MagicMock()
    mock_query.return_value = mock_query_instance
    mock_query_instance.join.return_value = mock_query_instance
    mock_query_instance.filter.return_value = mock_query_instance
    mock_query_instance.all.return_value = return_data
    mock_query_instance.first.return_value = return_data[0] if return_data else None
    return mock_query_instance
```

## Running Tests

```bash
# Run all tests
python -m unittest discover tests/

# Run with project script
./scripts/run-server-tests.sh
```

## Key Testing Patterns

- **Mock database operations** to isolate API logic
- **Test both success and error cases** for each endpoint
- **Verify HTTP status codes** and response JSON structure
- **Use helper methods** to reduce code duplication
- **Assert database operations** like `add()`, `commit()`, `rollback()`
