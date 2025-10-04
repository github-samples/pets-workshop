import unittest
from unittest.mock import patch, MagicMock
import json
from server.app import app  # Changed to absolute import for running from project root

# filepath: server/test_app.py
class TestApp(unittest.TestCase):
    def setUp(self):
        # Create a test client using Flask's test client
        self.app = app.test_client()
        self.app.testing = True
        # Turn off database initialization for tests
        app.config['TESTING'] = True
        
    def _create_mock_dog(self, dog_id, name, breed, status='AVAILABLE'):
        """Helper method to create a mock dog with standard attributes"""
        dog = MagicMock(spec=['to_dict', 'id', 'name', 'breed', 'status'])
        dog.id = dog_id
        dog.name = name
        dog.breed = breed
        dog.status = MagicMock()
        dog.status.name = status
        dog.to_dict.return_value = {'id': dog_id, 'name': name, 'breed': breed, 'status': status}
        return dog
        
    def _setup_query_mock(self, mock_query, dogs):
        """Helper method to configure the query mock"""
        mock_query_instance = MagicMock()
        mock_query.return_value = mock_query_instance
        mock_query_instance.join.return_value = mock_query_instance
        mock_query_instance.filter.return_value = mock_query_instance
        mock_query_instance.all.return_value = dogs
        return mock_query_instance

    def _create_mock_breed(self, name):
        """Helper method to create a mock breed"""
        breed = MagicMock(spec=['name'])
        breed.name = name
        return breed

    @patch('server.app.db.session.query')
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
        self.assertEqual(len(data), 2)
        
        # Verify first dog
        self.assertEqual(data[0]['id'], 1)
        self.assertEqual(data[0]['name'], "Buddy")
        self.assertEqual(data[0]['breed'], "Labrador")
        self.assertEqual(data[0]['status'], "AVAILABLE")
        
        # Verify second dog
        self.assertEqual(data[1]['id'], 2)
        self.assertEqual(data[1]['name'], "Max")
        self.assertEqual(data[1]['breed'], "German Shepherd")
        self.assertEqual(data[1]['status'], "AVAILABLE")
        
        # Verify query was called
        mock_query.assert_called_once()
        
    @patch('server.app.db.session.query')
    def test_get_dogs_empty(self, mock_query):
        """Test retrieval when no dogs are available"""
        # Arrange
        self._setup_query_mock(mock_query, [])
        
        # Act
        response = self.app.get('/api/dogs')
        
        # Assert
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data, [])
        
    @patch('server.app.db.session.query')
    def test_get_dogs_structure(self, mock_query):
        """Test the response structure for a single dog"""
        # Arrange
        dog = self._create_mock_dog(1, "Buddy", "Labrador")
        self._setup_query_mock(mock_query, [dog])
        
        # Act
        response = self.app.get('/api/dogs')
        
        # Assert
        data = json.loads(response.data)
        self.assertTrue(isinstance(data, list))
        self.assertEqual(len(data), 1)
        self.assertEqual(set(data[0].keys()), {'id', 'name', 'breed', 'status'})

    @patch('server.app.db.session.query')
    def test_get_dogs_breed_filter(self, mock_query):
        """Test filtering dogs by breed"""
        # Arrange
        beagle1 = self._create_mock_dog(1, "Buddy", "Beagle")
        beagle2 = self._create_mock_dog(2, "Max", "Beagle")
        self._setup_query_mock(mock_query, [beagle1, beagle2])
        
        # Act
        response = self.app.get('/api/dogs?breed=Beagle')
        
        # Assert
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)
        for dog in data:
            self.assertEqual(dog['breed'], 'Beagle')

    @patch('server.app.db.session.query')
    def test_get_dogs_available_filter(self, mock_query):
        """Test filtering dogs by availability"""
        # Arrange
        available_dog = self._create_mock_dog(1, "Buddy", "Labrador", "AVAILABLE")
        self._setup_query_mock(mock_query, [available_dog])
        
        # Act
        response = self.app.get('/api/dogs?available=true')
        
        # Assert
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['status'], 'AVAILABLE')

    @patch('server.app.db.session.query')
    def test_get_dogs_combined_filters(self, mock_query):
        """Test filtering dogs by both breed and availability"""
        # Arrange
        available_beagle = self._create_mock_dog(1, "Buddy", "Beagle", "AVAILABLE")
        self._setup_query_mock(mock_query, [available_beagle])
        
        # Act
        response = self.app.get('/api/dogs?breed=Beagle&available=true')
        
        # Assert
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['breed'], 'Beagle')
        self.assertEqual(data[0]['status'], 'AVAILABLE')

    @patch('server.app.db.session.query')
    def test_get_breeds_success(self, mock_query):
        """Test successful retrieval of breed list"""
        # Arrange
        breed1 = self._create_mock_breed("Labrador")
        breed2 = self._create_mock_breed("Beagle")
        mock_breeds = [breed1, breed2]
        
        mock_query_instance = MagicMock()
        mock_query.return_value = mock_query_instance
        mock_query_instance.distinct.return_value = mock_query_instance
        mock_query_instance.all.return_value = mock_breeds
        
        # Act
        response = self.app.get('/api/breeds')
        
        # Assert
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)
        self.assertIn("Labrador", data)
        self.assertIn("Beagle", data)

    @patch('server.app.db.session.query')
    def test_get_breeds_empty(self, mock_query):
        """Test retrieval when no breeds are available"""
        # Arrange
        mock_query_instance = MagicMock()
        mock_query.return_value = mock_query_instance
        mock_query_instance.distinct.return_value = mock_query_instance
        mock_query_instance.all.return_value = []
        
        # Act
        response = self.app.get('/api/breeds')
        
        # Assert
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data, [])


if __name__ == '__main__':
    unittest.main()