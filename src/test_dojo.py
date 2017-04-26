

from termcolor import colored
from Dojo import Dojo


   
class TestDojo(unittest.TestCase):
    def __init__(self):
       
        self.Dojo = Dojo()
    
    def test_create_room_successfully(self):
        initial_room_count = len(Dojo.rooms)
        blue_office = Dojo.create_room('Blue', 'office')
        self.assertTrue(blue_office)
        new_room_count = len(Dojo.all_rooms)
        self.assertEqual(new_room_count - initial_room_count, 1)
        
        
    def test_add_person_before_room_creation_does_not_allocate(Dojo):
        Dojo.add_person('staff', 'Maria')
        assert Dojo.print_allocations() ==\
        '\nALLOCATIONS\n' + '-'*20+'\n' + \
        colored('NO ALLOCATIONS HAVE BEEN DONE YET', 'white', 'on_red')
        Dojo.remove_person('Maria')
        
    def test_room_is_created(Dojo):
        assert Dojo.create_room('office', 'cayene') ==\
        colored('Office cayene created.', 'white', 'on_green')
        
    def test_room_created_with_correct_values(Dojo):
        Dojo.create_room('livingspace', 'chillspot')
        assert Dojo.get_room(room_name='chillspot')['max_space'] == 4
        
if __name__ == '__main__':
    unittest.main()
    