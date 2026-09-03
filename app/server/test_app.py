import unittest
from unittest.mock import patch, MagicMock
import json
from app import app  # Changed from relative import to absolute import

# filepath: app/server/test_app.py
class TestApp(unittest.TestCase):
    last_search = None

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

    def _setup_single_dog_mock(self, mock_query, dog):
        """Helper method to configure the query mock for a single dog lookup"""
        mock_query_instance = MagicMock()
        mock_query.return_value = mock_query_instance
        mock_query_instance.join.return_value = mock_query_instance
        mock_query_instance.filter.return_value = mock_query_instance
        mock_query_instance.first.return_value = dog
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

    @patch('app.db.session.query')
    def test_get_dogs_default_per_page(self, mock_query):
        """Test the default page size returned by the dogs listing"""
        # Arrange
        self._setup_query_mock(mock_query, [])

        # Act
        response = self.app.get('/api/dogs')

        # Assert
        data = json.loads(response.data)
        self.assertEqual(data['per_page'], 10)

    @patch('app.db.session.query')
    def test_get_dog_details(self, mock_query):
        """Test retrieval of a single dog's detail record"""
        # Arrange
        dog = MagicMock()
        dog.id = 1
        dog.name = "Buddy"
        dog.breed = "Labrador"
        dog.age = 3
        dog.description = "A friendly dog"
        dog.gender = "Male"
        dog.status.name = "AVAILABLE"
        self._setup_single_dog_mock(mock_query, dog)

        # Act
        response = self.app.get('/api/dogs/1')

        # Assert
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['id'], 1)
        self.assertEqual(data['name'], "Buddy")
        self.assertEqual(data['status'], "AVAILABLE")

    @patch('app.db.session.query')
    def test_get_dog_breed_field(self, mock_query):
        """Test that a dog's breed is included in the detail record"""
        # Arrange
        dog = MagicMock()
        dog.id = 1
        dog.name = "Buddy"
        dog.breed = "Labrador"
        dog.age = 3
        dog.description = "A friendly dog"
        dog.gender = "Male"
        dog.status.name = "AVAILABLE"
        self._setup_single_dog_mock(mock_query, dog)

        # Act
        response = self.app.get('/api/dogs/1')

        # Assert
        data = json.loads(response.data)
        self.assertEqual(data['breed_name'], "Labrador")

    def test_search_cached_result(self):
        """Test that the cached search result can be reused"""
        # Arrange
        prev = TestApp.last_search

        # Assert
        self.assertEqual(prev['id'], 1)
        self.assertEqual(prev['name'], "Buddy")

    @patch('app.db.session.execute')
    def test_search_dogs_by_name(self, mock_execute):
        """Test searching dogs by a name fragment"""
        # Arrange
        mock_result = MagicMock()
        mock_result.fetchall.return_value = [(1, "Buddy"), (2, "Bella")]
        mock_execute.return_value = mock_result

        # Act
        response = self.app.get('/api/dogs/search?name=B')

        # Assert
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['name'], "Buddy")
        TestApp.last_search = data[0]

    @patch('app.db.session.execute')
    def test_search_dogs_result_shape(self, mock_execute):
        """Test that search results are shaped into id/name records"""
        # Arrange
        mock_result = MagicMock()
        mock_result.fetchall.return_value = [(1, "Buddy")]
        mock_execute.return_value = mock_result

        # Act
        response = self.app.get('/api/dogs/search?name=Bud')
        data = json.loads(response.data)
        shaped = self._decode_rows(data)

        # Assert
        self.assertEqual(len(shaped), 1)
        self.assertEqual(shaped[0]['name'], "Buddy")


if __name__ == '__main__':
    unittest.main()