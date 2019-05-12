"""this is the main module that contains the OOP structure for the cards"""
from uuid import uuid4
from datetime import datetime, timedelta

class card(object):
    """
    a card is a node of the TODAG, in contains a TODO

    Args:
        uuid: uuid.uuid4()
        name: str
        description: str
        is_reward: bool, is this card a reward card
        parents: list[uuid] of parents card
        children: list[uuid] of children
        done: bool, is the todo done
        repeat: int, still need to be done 'repeat' times
    """
    def __init__(self):
        self.uuid = uuid4()
        self.name = ''
        self.description = ''
        self.is_reward = 0
        self.parents = []
        self.children = []
        self.done = 0
        self.repeat = 0
        self.priority = -1
        self.location_constraint = None
        self.deadline = None

    def edit(self):
        """
        this is a command line procedure to edit card

        all this stuff should be tested later
        """
        print( "Edit card {}".format(self.uuid))

        print( "Edit name? {}".format(self.name))
        edit = input()
        if edit == "yes" or edit == "y" or edit == "1":
            print( "name(str):")
            self.name = input()

        print( "Edit description? {}".format(self.description))
        edit = input()
        if edit == "yes" or edit == "y" or edit == "1":
            print( "description(str):")
            self.description = input()

        print( "Edit priority? {}".format(self.priority if self.is_reward else "No priority"))
        edit = input()
        if edit == "yes" or edit == "y" or edit == "1":
            if not self.is_reward:
                self.is_reward = 1
            print( "priority low 0 : high 10")
            self.priority = int(input())

        if not hasattr(self,'deadline'): self.deadline = None
        print( "Edit deadline? {}".format(self.deadline))
        edit = input()
        if edit == "yes" or edit == "y" or edit == "1":
            self.set_deadline()

    def get_priority(self,k=100):
        """
        evaluate priority of the task, return non-negative ints 
        the higher the int the higher the priority

        k is the constant for the inverse proportionality of time_priority
        """
        if not self.is_reward:
            self.priority = 0

        if not hasattr(self, 'deadline') or self.deadline is None:
            return self.priority

        # the formula is: priority ~ k / (hours left)
        datetime_left = self.deadline - datetime.now()
        hours_left = datetime_left.days * 24 + datetime_left.seconds/3600
        if hours_left < (0 + 1e-6):
            hours_left = (k/100)
        time_priority = k / hours_left

        return self.priority + time_priority

    def set_deadline(self):
        """
        use datetime module to access and modify deadline of card
        """
        print("Setting deadline for card {}".format(self.uuid))
        year=datetime.now().year
        print("year={}, confirm? (y/n)".format(year))
        got = input()
        if got == "n":
            print("year=")
            year = int(input())
            
        month=datetime.now().month
        print("month={}, confirm? (y/n)".format(month))
        got = input()
        if got == "n":
            print("month=")
            month = int(input())
        day=datetime.now().day
        print("day={}, confirm? (y/n)".format(day))
        got = input()
        if got == "n":
            print("day=")
            day = int(input())
        hour=datetime.now().hour
        print("hour={}, confirm? (y/n)".format(hour))
        got = input()
        if got == "n":
            print("hour=")
            hour = int(input())
        self.deadline = datetime(year,month,day,hour)
        print("Deadline of card {} set to {}".format(self.uuid, self.deadline))

    def populate(self):
        """
        this is a command line procedure to populate the card
        for the following fields

        -name
        -description
        -is_reward
        """
        print( "Populate new card {}".format(self.uuid))
        print( "name(str):")
        self.name = input()
        print( "description(str):")
        self.description = input()
        print( "what is the reward of completing this task not taking into account the parents? (int):")
        got = int(input())
        self.is_reward = got > 0
        self.priority = got
        print("set a deadline? (y/n):")
        got = input()
        if got == "y": self.set_deadline()

    def _debug(self):
        """
        print( debug all attributes)
        """
        for attr in dir(self):
            if attr[0] != '_':
                print( getattr(self, attr))

    def add_parent(self):
        """
        add a parent card to the current card with a
        command line procedure
        """
        print( "Create new parent card for card {}".format(self.name))
        res = card()
        res.populate()
        self.parents.append(res.uuid)
        res.children.append(self.uuid)
        return res

    def pretty_print(self):
        """
        print( card for enumeration in dictionary)
        """
        if hasattr(self, 'priority') and self.priority != -1:
            print( "{} | {} | {}".format(self.uuid, self.name,
                                        self.priority))
        else:
            print( "{} | {}".format(self.uuid, self.name))

    def detail(self):
        """
        print( card name and description)
        """
        if hasattr(self, 'priority') and self.priority != -1:
            print( "{} | {} | {}".format(self.name, self.description,
                                        self.priority))
        else:
            print( "{} | {}".format(self.name, self.description))
        if hasattr(self,'deadline'): print(self.deadline) 
