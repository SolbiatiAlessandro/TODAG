"""this is the main module that contains the OOP structure for the cards"""
from uuid import uuid4
from datetime import datetime, timedelta
from card_utils import multiline_input
from utils import TIME_FORMAT
import pandas as pd
from time import ctime
import logging
import sys, tempfile, os
from subprocess import call

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
        self.debug_string = ""

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

        print( "Edit description? [a (add), r (reset), e (editor edit), else (no)] {}".format(self.description))
        edit = input()
        if edit == "r" or edit == "reset":
            print( "reset description(str):")
            self.description = multiline_input()
        if edit == "a" or edit == "add":
            print( "add description(str):")
            self.description += "\n\n(added on {})\n".format(ctime())
            self.description += multiline_input()
        if edit == "e" or edit == "edit":
            EDITOR = os.environ.get('EDITOR','vim') #that easy!
            initial_message = bytes(str(self.description),encoding='utf8')

            with open("temp.txt","wb") as tf: 
              tf.write(initial_message)
              tf.flush()
              call([EDITOR, tf.name])

              # do the parsing with `tf` using regular File operations.
              # for instance:
              with open(tf.name,"r") as edited_file:
                  self.description = edited_file.read()
            

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

    def get_deadline_priority(self, k=100):
        """
        k is the constant for the inverse proportionality of time_priority

        return deadline priority as hour delta
        """
        if not hasattr(self, 'deadline') or self.deadline is None:
            return 0

        # the formula is: priority ~ k / (hours left)
        datetime_left = self.deadline - datetime.now()
        hours_left = datetime_left.days * 24 + datetime_left.seconds/3600
        if hours_left < (0 + 1e-6):
            hours_left = (k/100)
        time_priority = k / hours_left

        return time_priority

    def get_reshake_priority(self) -> float:
        """
        return priority from not being checked for a long time

        return hours of last update of query_uuid card, in orderd
        - last checked
        - last created
        - beginning of logs

        args:
            query_uuid -> (str)

        FIX: funny bug with type annotation,
        if you annotate str: query_uuid it 'memoize' last variable
        """
        query_uuid = str(self.uuid)
        logs = pd.read_csv(open("logs.csv","r"), encoding="ISO-8859-1")

        # this used to be logs.arg1 == query_uuid, but we changed
        # the logging to send signal to google calendar, now the 
        # reshake priority is computed with name. If two cards had
        # the same name this would create a bug where they account
        # for the same reshake priority
        checked = list(logs[logs.arg1 == self.name][logs.action == "checked_todo"]["date"])

        if checked: # set last checked as last update
            last_updated = checked[-1]
        else:
            created = list(logs[logs.arg1 == query_uuid][logs.action == "add_card"]["date"])
            if created: # set creation time as last update
                last_updated = created[0]
            else: # set beginning time as last update
                start_time = logs.iloc[0]['date']
                last_updated = start_time

        datetime_last_updated = datetime.strptime(last_updated, TIME_FORMAT)
        datetime_delta = datetime.now() - datetime_last_updated
        hours_delta = datetime_delta.days * 24 + datetime_delta.seconds/3600
        return hours_delta

    def get_priority(self,k=100):
        """
        evaluate priority of the task, return non-negative ints 
        the higher the int the higher the priority
        """
        baseline_priority = self.priority 
        deadline_priority = self.get_deadline_priority()
        return sum([baseline_priority, deadline_priority])

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
        self.description = multiline_input()
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

        # find links in the description and open them with browser
        links = []
        def get_link_start(description): 
            LINK_STRING = 'http'
            return description.find(LINK_STRING)
        def get_link_end(description):
            END_STRINGS = ["\n",","," "]
            ends = [description.find(token) for token in END_STRINGS if description.find(token) != -1]
            return min(ends) if ends else -1

        logging.info("parsing links in description")
        offset = 0
        match_start = get_link_start(self.description)
        match_end = get_link_end(self.description[match_start:])
        while match_start != -1 and match_end != -1:
            index_start = offset + match_start
            index_end = offset + match_start + match_end
            link = self.description[index_start:index_end]
            logging.info([match_start, match_end, offset,\
                    index_start, index_end, link])
            links.append(link)

            offset = index_end
            match_start = get_link_start(self.description[offset:])
            match_end = get_link_end(self.description[offset+match_start:])

        logging.info("opening links")
        for link in links:
            os.system("open {}".format(link))





        
