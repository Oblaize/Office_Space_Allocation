from unittest import TestCase
from Dojo import Dojo

class TestCaseDojo(TestCase):
    def test_create_room_with_room_type_not_string_raises_ValueError(self):
        dojo = Dojo()
        with self.assertRaises(ValueError):
            dojo.create_room(2, 'AA')

    def test_create_room_with_room_name_not_string_raises_ValueError(self):
        dojo = Dojo()
        with self.assertRaises(ValueError):
            dojo.create_room('office', 3)

    def test_if_room_type_not_office_raises_ValueError(self):
        dojo = Dojo()
        with self.assertRaises(ValueError):
            dojo.create_room('office', 'AQ')

    def test_if_room_type_not_livingspace_raises_ValueError(self):
        dojo = Dojo()
        with self.assertRaises(ValueError):
            dojo.create_room('livingspace', 'AQ')

    def test_if_room_name_exists_after_creation(self):
        dojo = Dojo()
        dojo.create_room('Office', 'AA')
        self.assertIsNotNone(dojo.get_room(room_name="AA"))

    def test_if_room_name_exists_raise_ValueError(self):
        dojo = Dojo()
        dojo.create_room('Office', 'AA')
        with self.assertRaises(ValueError):
            dojo.create_room('Office', 'AA')

if __name__ == '__main__':
    unittest.main()
    