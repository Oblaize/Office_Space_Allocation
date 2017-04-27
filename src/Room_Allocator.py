#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
Usage:
    create_room <room_type> <room_name> ...
    check (<rooms>|<room_availability>|<person>) <name>
    add_person <first_name> <last_name> <FELLOW>|<STAFF> [<wants_accommodation>]
    allocate_space <name> ...
    reallocate_person <first_name> <last_name> <new_room_name>
    remove_person <first_name> <last_name> [-r] [-o] [-l]
    load (<people>|<rooms>) <filename> | state <database>
    print_room <room_name> | (allocations|unallocated) [--O=filename]
    save_state [--db=database]
    clear
    quit
Arguments:
    FELLOW|STAFF           Type of person to create/employ
    wants_accommodation    Specify if person(only fellow) wants living space
Options:
    -h, --help           : Use with a command to show the command's help
                            messsage
    -r                   : Specify person to be removed from all room but
                            not Dojo
    -l                   : Specify person to be removed from assigned
                            livingspace but not Dojo
    -o                   : Specify person to be removed from assigned office
                            but not Dojo
    --O=filename         : Specify filename to save or read from
    --db=database        : Specify database to save or read from [default: dojo.sqlite]
"""
import cmd
import os
import getch

from docopt import docopt, DocoptExit
from termcolor import cprint, colored
from pyfiglet import figlet_format

from Dojo import Dojo


def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """
    def cmd_function(self, arg):
        try:
            opt = docopt(cmd_function.__doc__, arg)
        except DocoptExit as error:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.
            cprint('Invalid Command!', 'white', 'on_red')
            cprint(error, 'white', 'on_red')
            return
        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.
            return
        return func(self, opt)
    cmd_function.__name__ = func.__name__
    cmd_function.__doc__ = func.__doc__
    cmd_function.__dict__.update(func.__dict__)
    return cmd_function
BORDER = colored("*" * 20, 'green').center(80)


def introduction():
    '''Print Dojo's introduction'''
    print(BORDER)
    cprint('THE DOJO ROOM ALLOCATOR!'.center(70), 'white', 'on_cyan')
    print(__doc__)
    print(BORDER)


class DojoApplication(cmd.Cmd):
    '''Dojo's interaction point with the terminal'''
    dojo = Dojo()
    cprint("Do you want to load previous state? ",
           "white", "on_cyan")
    load_state = getch.getch().lower()
    while load_state not in ('y', 'yes', 'n', 'no'):
        cprint(
            '{} is not allowed. Type n, no, y or yes!!'.format(load_state),
            'white', 'on_cyan')
        load_state = getch.getch().lower()
    if load_state in ('y', 'yes'):
        print(dojo.load_state( 'dojo.sqlite'))
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
    cprint(figlet_format('DOJO', font='isometric3'), 'green', attrs=['bold'])
    prompt = 'ANDELA DOJO '

    @docopt_cmd
    def do_create_room(self, arg):
        '''Usage: create_room <room_type> <room_name> ...'''
        name = arg['<room_name>']
        room_type = arg['<room_type>']
        for room in name:
            try:
                print(self.dojo.create_room(room_type, room))
            except Exception as error:
                cprint(error, 'white', 'on_red')

    @docopt_cmd
    def do_check(self, arg):
        '''Usage: check room_type <type> | (room_availability |person)
            <name>...'''
        try:
            name = ' '.join(arg['<name>']).lower()
            if arg['room_type']:
                arg['<type>'] = arg['<type>'].lower()
                result = ''
                if arg['<type>']in ('office', 'livingspace'):
                    rooms = self.dojo.get_room(room_type=arg['<type>'])
                    if rooms:
                        for room in rooms:
                            result += room['name'].upper() + ', '
                        print(result[:-2])
                    else:
                        cprint(
                            'no {} created in Dojo yet.'.format(
                                arg['<type>']), 'red')
                else:
                    cprint('no such room type {} in Dojo'.format(
                        arg['<type>']), 'red')
            elif arg['room_availability']:
                print(self.dojo.check_room_availability(name))
            elif arg['person']:
                if self.dojo.person_exists(name):
                    cprint('{} exists'.format(name), 'white', 'on_green')
                else:
                    cprint("{} doesn't exist".format(name), 'white', 'on_red')
        except Exception as error:
            cprint(error, 'white', 'on_red')

    @docopt_cmd
    def do_add_person(self, arg):
        '''Usage: add_person <first_name> <last_name> (<FELLOW>|<STAFF>)
         [<wants_accommodation>]'''
        try:
            name = arg['<first_name>'] + ' ' + arg['<last_name>']
            role = arg['<FELLOW>'] or arg['<STAFF>']
            if role.lower() not in ('fellow', 'staff'):
                raise ValueError('both names must be specified')
            if arg['<wants_accommodation>']:
                accommodation = arg['<wants_accommodation>'].lower()
                if accommodation in ('y', 'yes'):
                    print(self.dojo.add_person(role, name, True))
                else:
                    raise ValueError('wants accommodation has to be y or yes')
            else:
                print(self.dojo.add_person(role, name))
        except Exception as error:
            cprint(error, 'white', 'on_red')

    @docopt_cmd
    def do_allocate_space(self, arg):
        '''Usage: allocate_space <name> ...'''
        try:
            person_name = ' '.join(arg['<name>'])
            print(self.dojo.allocate_person(person_name))
        except Exception as error:
            cprint(error, 'white', 'on_red')

    @docopt_cmd
    def do_reallocate_person(self, arg):
        '''Usage: reallocate_person <first_name> <last_name> <new_room_name>'''
        try:
            person = arg['<first_name>'] + ' ' + arg['<last_name>']
            room = arg['<new_room_name>']
            print(self.dojo.reallocate_person(person, room))
        except Exception as error:
            cprint(error, 'white', 'on_red')

    @docopt_cmd
    def do_remove_person(self, arg):
        '''Usage: remove_person <name> ... [-r] [-o] [-l]'''
        try:
            person = ' '.join(arg['<name>'])
            if arg['-r']:
                self.dojo.remove_person_from_room(person)
            elif arg['-l']:
                self.dojo.remove_person_from_room(person, livingspace=True)
            elif arg['-o']:
                self.dojo.remove_person_from_room(person, office=True)
            else:
                print(self.dojo.remove_person(person))
        except Exception as error:
            cprint(error, 'white', 'on_red')

    @docopt_cmd
    def do_load(self, arg):
        '''Usage: load (<people>|<rooms>) <filename> | state <database>'''
        print(arg)
        try:
            if arg['people']:
                self.dojo.load_people(arg['<filename>'])
            elif arg['rooms']:
                self.dojo.load_rooms(arg['<filename>'])
            elif arg['state']:
                self.dojo.load_state(arg['<database>'])
        except Exception as error:
            cprint(error, 'white', 'on_red')

    @docopt_cmd
    def do_print_room(self, arg):
        '''Usage: print_room <room_name> | (allocations|unallocated)
        [--O=filename]'''
        try:
            myfile =open("filename.txt", "w")
            if arg['room']:
                print(self.dojo.print_room(arg['<room_name>']))
                myfile.write(self.dojo.print_room(arg['<room_name>'])+"\n")
            elif arg['allocations']:
                if arg['--O']:
                    print(self.dojo.print_allocations(filename=arg['--o']))
                else:
                    print(self.dojo.print_allocations())
            elif arg['unallocated']:
                if arg['--O']:
                    print(self.dojo.print_unallocated(filename=arg['--o']))
                else:
                    print(self.dojo.print_unallocated())
                myfile.close()
        except Exception as error:
            cprint(error, 'white', 'on_red')

    @docopt_cmd
    def do_save_state(self, arg):
        '''Usage: save_state [--db=database]'''
        try:
            if arg['--db']:
                print(self.dojo.save_state(arg['--db']))
            else:
                print(self.dojo.save_state())
        except Exception as error:
            cprint(error, 'white', 'on_red')

    @docopt_cmd
    def do_quit(self, arg):
        '''Usage: quit '''
        cprint('Are you sure you want to exit from Dojo?',
               'white', 'on_cyan')
        quit_app = getch.getch().lower()
        while quit_app not in ('yes', 'y', 'no', 'n'):
            cprint(
                '{} is not allowed. Type n, no, y or yes!!'.format(quit_app),
                'white', 'on_cyan')
            quit_app = getch.getch().lower()
        if quit_app in ('n', 'no'):
            pass
        else:
            cprint('Do you wish to save the current running state?',
                   'white', 'on_cyan')
            save = getch.getch().lower()
            while save not in ('yes', 'y', 'no', 'n'):
                cprint(
                    '{} is not allowed. Type n, no, y or yes!!'.format(save),
                    'white', 'on_cyan')
                save = getch.getch().lower()
            # clear screen before exit
            self.do_clear(arg)
            if save in ('yes', 'y'):
                print(self.dojo.save_state())
            else:
                cprint(
                    'Dojo state has not been saved!'.center(70),
                    'white', 'on_cyan')
            cprint('SEE YOU WHEN YOU SEE ME!!!'.center(70), 'white', 'on_cyan')
            exit()

    @docopt_cmd
    def do_clear(self, args):
        '''Usage: clear'''
        os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == '__main__':
    introduction()
    DojoApplication().cmdloop()