import unittest
from DataGestor import DataGestor

class TestDataGestor(unittest.TestCase):

    def setUp(self):
        self.data_gestor = DataGestor()

    def test_add_data(self):
        self.data_gestor.add_data('key1', 'value1')
        self.assertEqual(self.data_gestor.get_data('key1'), 'value1')

    def test_get_data_nonexistent_key(self):
        self.assertIsNone(self.data_gestor.get_data('nonexistent_key'))

    def test_remove_data(self):
        self.data_gestor.add_data('key1', 'value1')
        self.data_gestor.remove_data('key1')
        self.assertIsNone(self.data_gestor.get_data('key1'))

    def test_update_data(self):
        self.data_gestor.add_data('key1', 'value1')
        self.data_gestor.update_data('key1', 'value2')
        self.assertEqual(self.data_gestor.get_data('key1'), 'value2')

    def test_get_all_data(self):
        self.data_gestor.add_data('key1', 'value1')
        self.data_gestor.add_data('key2', 'value2')
        all_data = self.data_gestor.get_all_data()
        self.assertEqual(all_data, {'key1': 'value1', 'key2': 'value2'})

if __name__ == '__main__':
    unittest.main()