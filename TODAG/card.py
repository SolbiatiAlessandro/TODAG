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
        parents: list[card] of parents card
        children: list[card] of children
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

    def populate(self):
        """
        this is a command line procedure to populate the card
        for the following fields

        -name
        -description
        -is_optional
        -is_reward
        """
        print "Populate new card {}".format(self.uuid)
        print "name(str):"
        self.name = raw_input()
        print "description(str):"
        self.description = raw_input()
        print "is_reward(int):"
        self.is_reward = int(raw_input())
        print "is_optional(int):"
        self.is_optional = int(raw_input())

    def _debug(self):
        """
        print debug all attributes
        """
        for attr in dir(self):
            if attr[0] != '_':
                print getattr(self, attr)

    def add_parent(self):
        """
        add a parent card to the current card with a
        command line procedure
        """
        print "Create new parent card for card {}".format(self.name)
        res = card()
        res.populate()
        self.parents.append(res.uuid)
        res.children.append(self.uuid)
        return res

    def pretty_print(self):
        """
        print card for enumeration in dictionary
        """
        print "{} | {}".format(self.uuid, self.name)
