from unittest import TestCase
from src.Room import Room, Office, LivingSpace


class RoomTestCase(TestCase):
    def test_office_room_type_is_correct(self):
        room = Office('A1')
        self.assertEqual(room.room_type, 'office')

    def test_livingspace_room_type_is_correct(self):
        room = LivingSpace('A1')
        self.assertEqual(room.room_type, 'livingspace')

    def test_office_maximum_space(self):
        room = Office('A1')
        self.assertEqual(room.max_space, 6, msg='Sorry! Office Full')

    def test_livingspace_maximum_space(self):
        room = LivingSpace('A1')
        self.assertEqual(room.max_space, 4, msg='Livingspace Full')

    def test_office_has_room_name(self):
        room = Office(name='A2')
        self.assertIsNotNone(room.name)

    def test_livingspace_has_room_name(self):
        room = LivingSpace(name='L2')
        self.assertIsNotNone(room.name)

    def test_office_initialization_without_name_raises_ValueError(self):
        with self.assertRaises(TypeError):
            room = Office()

    def test_livingspace_initialization_without_name_raises_ValueError(self):
        with self.assertRaises(TypeError):
            room = LivingSpace()

    def test_office_pass_non_int_max_space_value_raises_valueError(self):
        room = Office('A1')
        with self.assertRaises(ValueError):
            room.set_max_space('t')

    def test_livingspace_pass_non_int_max_space_value_raises_valueError(self):
        room = LivingSpace('L1')
        with self.assertRaises(ValueError):
            room.set_max_space('t')