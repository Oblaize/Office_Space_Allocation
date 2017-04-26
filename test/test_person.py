from unittest import TestCase
from src.Person import Person, Staff, Fellow


class PersonTestCase(TestCase):
    def test_cannot_create_staff_without_name(self):
        with self.assertRaises(TypeError):
            person = Staff()

    def test_cannot_create_fellow_without_name(self):
        with self.assertRaises(TypeError):
            person = Fellow()


    def test_fellow_person_type_is_correct(self):
        person = Fellow('Blaize')
        self.assertTrue(person.person_type, 'fellow')

    def test_staff_person_type_is_correct(self):
        person = Staff('Blaize')
        self.assertTrue(person.person_type, 'staff')

    def test_fellow_can_opt_out_of_living_space(self):
        fellow = Fellow('Othieno')
        self.assertFalse(fellow.wants_livingspace)

    def test_fellow_can_opt_for_living_space(self):
        fellow = Fellow('Othieno', accomodation=True)
        self.assertTrue(fellow.wants_livingspace)








