from termcolor import cprint, colored

from unittest import TestCase
from src.Dojo import Dojo

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
            dojo.create_room('office', 7)

    def test_if_room_type_not_livingspace_raises_ValueError(self):
        dojo = Dojo()
        with self.assertRaises(ValueError):
            dojo.create_room('livingspace', 4)

    def test_if_room_name_exists_after_creation(self):
        dojo = Dojo()
        dojo.create_room('Office', 'AA')
        self.assertIsNotNone(dojo.get_room(room_name="AA"))

    def test_if_room_name_exists_raise_ValueError(self):
        dojo = Dojo()
        dojo.create_room('Office', 6)
        with self.assertRaises(ValueError):
            dojo.create_room('Office', 6)
    
    def test_cannot_operate_on_non_existent_room(self):
        dojo = Dojo()
        assert dojo.check_room_availability('hog') ==\
        colored("Room hog doesn't exist!", 'white', 'on_red')
        
    def test_room_name_and_type_must_be_specified(self):
        dojo = Dojo()
        with self.assertRaises(TypeError):
            dojo.create_room('office', 'blue')
        
    def test_room_name_and_type_cannot_be_empty(self):
        dojo = Dojo()
        with self.assertRaises(TypeError):
            dojo.create_room('office', 'blue')
        
    def test_room_name_can_only_be_string(self):
        dojo = Dojo()
        with self.assertRaises(TypeError):
            dojo.create_room('office', 'red')
        
    def test_person_is_added(self):
        dojo = Dojo()
        assert dojo.add_person('staff', 'blaize othieno') ==\
        colored('Staff blaize othieno added.', 'white', 'on_green')
        
    def test_person_exists_after_being_added(self):
        dojo = Dojo()
        assert dojo.person_exists('denis gathondu')
        
    def test_person_name_duplicates_not_allowed(self):
        dojo = Dojo()
        with self.assertRaises(ValueError):
            dojo.add_person('fellow', 'blaize othieno')
        
    def test_person_name_must_be_string(self):
        dojo = Dojo()
        with self.assertRaises(ValueError):
            dojo.add_person('fellow', '@blaize')
            
    def test_wrong_person_role_raises_error(self):
        dojo = Dojo()
        with self.assertRaises(ValueError):
            dojo.add_person('fella', 'dng')
            
    def test_person_is_automatically_allocated_space(self):
        dojo = Dojo()
        room = [room for room in dojo.rooms if 'blaize othieno'
        in room['occupants']]
        assert dojo.allocate_person('blaize othieno')
    
    def test_person_can_be_manually_allocated(self):
        dojo = Dojo()
        dojo.remove_person_from_room('dus')
        dojo.allocate_person('blaize othieno')
        assert 'blaize othieno' in dojo.print_room('dus')
        
    def test_person_who_wants_livingspace_is_allocated_livingspace(self):
        dojo = Dojo()
        dojo.add_person('fellow', 'mike andela', True)
        assert dojo.print_room('des') == 'mike andela'
        
    def test_person_is_reallocated(self):
        dojo = Dojo()
        dojo.create_room('office', 'valhalla')
        assert dojo.reallocate_person('blaize othieno', 'koko') ==\
        colored('blaize othieno reallocated to office valhalla.', 'white',
                'on_green')
                
    def test_staff_cannot_be_reallocated_to_livingspace(self):
        dojo = Dojo()
        with self.assertRaises(ValueError):
            dojo.reallocate_person('blaize othieno', 'blue')
            
    def test_person_with_allocation_cannot_be_allocated(self):
        dojo = Dojo()
        with self.assertRaises(ValueError):
            dojo.allocate_person('blaize othieno')
            
    def test_non_existent_person_cannot_be_allocated_space(self):
        dojo = Dojo()
        with self.assertRaises(ValueError):
            dojo.allocate_person('tim tom')
            
    def test_allocations_are_printed_to_file(self):
        dojo = Dojo()
        assert dojo.print_allocations('alloc.txt') ==\
        colored('Allocations have been saved to file alloc.txt.', 'white',
                'on_green')
    def test_unallocated_is_correct(self):
        dojo = Dojo()
        assert dojo.print_unallocated() ==\
        '\nUNALLOCATED\n'+'-'*20+'\n' + colored('NO UNALLOCATED PEOPLE',
                                                'white', 'on_red')
                                                
    def test_unallocated_are_printed_to_file(self):
        dojo = Dojo()
        assert dojo.print_unallocated('unalloc.txt') ==\
        colored('Unallocations have been saved to file unalloc.txt.', 'white',
                'on_green')
                
    def test_room_prints_correctly(self):
        dojo = Dojo()
        assert dojo.print_room('blue') == 'blue'
        
    def test_cannot_print_non_existent_room(self):
        dojo = Dojo()
        with self.assertRaises(ValueError):
            dojo.print_room('nana')
            
    def test_person_is_successfully_removed_from_dojo(self):
        dojo = Dojo()
        dojo.remove_person('blaize othieno')
        assert dojo.person_exists('blaize') is None
        
    def test_people_are_loaded_from_file(self):
        dojo = Dojo()
        assert dojo.load_people('people.txt') == \
        colored('People loaded from people.txt successfully.', 'white',
                'on_green')
                
    def test_rooms_are_loaded_from_file(self):
        dojo = Dojo()
        assert dojo.load_rooms('rooms.txt') == \
        colored('Rooms loaded from rooms.txt successfully.', 'white',
                'on_green')
                
    def test_state_is_saved(self):
        dojo = Dojo()
        assert dojo.save_state() ==\
        colored("Dojo's state saved successfully.", 'white', 'on_green')
        
    def test_state_is_loaded(self):
        dojo = Dojo()
        assert dojo.load_state() ==\
        colored("Dojo's previous state loaded successfully.", 'white',
                'on_green')

if __name__ == '__main__':
    unittest.main()
    