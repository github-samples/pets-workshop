import unittest
from unittest.mock import patch, MagicMock
import json
from app import app  # Changed from relative import to absolute import

# filepath: app/server/test_app.py
class TestApp(unittest.TestCase):
    def setUp(self):
        # Create a test client using Flask's test client
        self.app = app.test_client()
        self.app.testing = True
        # Turn off database initialization for tests
        app.config['TESTING'] = True
        
    def _create_mock_dog(self, dog_id, name, breed):
        """Helper method to create a mock dog with standard attributes"""
        dog = MagicMock(spec=['to_dict', 'id', 'name', 'breed'])
        dog.id = dog_id
        dog.name = name
        dog.breed = breed
        dog.to_dict.return_value = {'id': dog_id, 'name': name, 'breed': breed}
        return dog
        
    def _setup_query_mock(self, mock_query, dogs):
        """Helper method to configure the query mock"""
        mock_query_instance = MagicMock()
        mock_query.return_value = mock_query_instance
        mock_query_instance.join.return_value = mock_query_instance
        mock_query_instance.count.return_value = len(dogs)
        mock_query_instance.offset.return_value = mock_query_instance
        mock_query_instance.limit.return_value = mock_query_instance
        mock_query_instance.all.return_value = dogs
        return mock_query_instance

    @patch('app.db.session.query')
    def test_get_dogs_success(self, mock_query):
        """Test successful retrieval of multiple dogs"""
        # Arrange
        dog1 = self._create_mock_dog(1, "Buddy", "Labrador")
        dog2 = self._create_mock_dog(2, "Max", "German Shepherd")
        mock_dogs = [dog1, dog2]
        
        self._setup_query_mock(mock_query, mock_dogs)
        
        # Act
        response = self.app.get('/api/dogs')
        
        # Assert
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(len(data['dogs']), 2)
        self.assertEqual(data['page'], 1)
        self.assertEqual(data['total'], 2)
        
        # Verify first dog
        self.assertEqual(data['dogs'][0]['id'], 1)
        self.assertEqual(data['dogs'][0]['name'], "Buddy")
        self.assertEqual(data['dogs'][0]['breed'], "Labrador")
        
        # Verify second dog
        self.assertEqual(data['dogs'][1]['id'], 2)
        self.assertEqual(data['dogs'][1]['name'], "Max")
        self.assertEqual(data['dogs'][1]['breed'], "German Shepherd")
        
        # Verify query was called
        mock_query.assert_called_once()
        
    @patch('app.db.session.query')
    def test_get_dogs_empty(self, mock_query):
        """Test retrieval when no dogs are available"""
        # Arrange
        self._setup_query_mock(mock_query, [])
        
        # Act
        response = self.app.get('/api/dogs')
        
        # Assert
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['dogs'], [])
        self.assertEqual(data['total'], 0)
        
    @patch('app.db.session.query')
    def test_get_dogs_structure(self, mock_query):
        """Test the response structure for a single dog"""
        # Arrange
        dog = self._create_mock_dog(1, "Buddy", "Labrador")
        self._setup_query_mock(mock_query, [dog])
        
        # Act
        response = self.app.get('/api/dogs')
        
        # Assert
        data = json.loads(response.data)
        self.assertIn('dogs', data)
        self.assertIn('page', data)
        self.assertIn('total', data)
        self.assertIn('total_pages', data)
        self.assertTrue(isinstance(data['dogs'], list))
        self.assertEqual(len(data['dogs']), 1)
        self.assertEqual(set(data['dogs'][0].keys()), {'id', 'name', 'breed'})

    @patch('app.User')
    def test_login_success(self, mock_user_model):
        """Test staff login with valid credentials"""
        user = MagicMock()
        user.id = 1
        user.check_password.return_value = True
        user.to_dict.return_value = {
            'id': 1,
            'email': 'staff@tailspin.example',
            'role': 'staff'
        }
        mock_user_model.query.filter_by.return_value.first.return_value = user

        response = self.app.post('/api/auth/login', json={
            'email': 'staff@tailspin.example',
            'password': 'TailspinDemo123!'
        })

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['user']['email'], 'staff@tailspin.example')

        with self.app.session_transaction() as session:
            self.assertEqual(session['user_id'], 1)

    @patch('app.User')
    def test_login_invalid_password(self, mock_user_model):
        """Test login failure with invalid credentials"""
        user = MagicMock()
        user.check_password.return_value = False
        mock_user_model.query.filter_by.return_value.first.return_value = user

        response = self.app.post('/api/auth/login', json={
            'email': 'staff@tailspin.example',
            'password': 'wrong-password'
        })

        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Invalid email or password')

    def test_me_requires_login(self):
        """Test current user endpoint rejects guests"""
        response = self.app.get('/api/auth/me')

        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Authentication required')

    @patch('app.db.session.get')
    def test_me_returns_current_user(self, mock_get):
        """Test current user endpoint returns authenticated staff user"""
        user = MagicMock()
        user.to_dict.return_value = {
            'id': 1,
            'email': 'staff@tailspin.example',
            'role': 'staff'
        }
        mock_get.return_value = user

        with self.app.session_transaction() as session:
            session['user_id'] = 1

        response = self.app.get('/api/auth/me')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['user']['role'], 'staff')

    @patch('app.db.session.get')
    def test_logout_clears_session(self, mock_get):
        """Test logout clears the authenticated session"""
        with self.app.session_transaction() as session:
            session['user_id'] = 1

        response = self.app.post('/api/auth/logout')

        self.assertEqual(response.status_code, 200)
        with self.app.session_transaction() as session:
            self.assertNotIn('user_id', session)

    def test_protected_listing_agent_rejects_guest(self):
        """Test upload analysis endpoint requires authentication"""
        response = self.app.post('/api/listing-agent/analyze', json={})

        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Authentication required')

    @patch('app.db.session.get')
    def test_protected_listing_agent_rejects_non_staff(self, mock_get):
        """Test upload analysis endpoint requires staff role"""
        user = MagicMock()
        user.role = 'viewer'
        mock_get.return_value = user

        with self.app.session_transaction() as session:
            session['user_id'] = 1

        response = self.app.post('/api/listing-agent/analyze', json={})

        self.assertEqual(response.status_code, 403)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Staff access required')


if __name__ == '__main__':
    unittest.main()
