"""this is the main module that contains the OOP structure for the cards"""


class card(object):
    """
    a card is a node of the TODAG, in contains a TODO

    Args:
        uuid: uuid.uuid4()
        name: str
        description: str
        is_reward: bool, is this card a reward card
        is_optional: bool, is this card optional or necessary
        parents: list[uuid] of parents card
        children: list[uuid] of children
        done: bool, is the todo done
        repeat: int, still need to be done 'repeat' times
    """
    def __init__(self):
        from uuid import uuid4
        self.uuid = uuid4()
        self.name = ''
        self.description = ''
        self.is_reward = 0
        self.is_optional = 0
        self.parents = []
        self.children = []
        self.done = 0
        self.repeat = 0
        self.priority = -1
        self.location_constraint = None

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


    def populate(self):
        """
        this is a command line procedure to populate the card
        for the following fields

        -name
        -description
        -is_optional
        -is_reward
        """
        print( "Populate new card {}".format(self.uuid))
        print( "name(str):")
        self.name = input()
        print( "description(str):")
        self.description = input()
        print( "is_reward(int):")
        self.is_reward = int(input())
        if self.is_reward:
            print( "priority low 0 : high 10")
            self.priority = int(input())

        # not needed, need to refactor better later
        # print( "is_optional(int):")
        # self.is_optional = int(input())
        self.is_optional = 1

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
