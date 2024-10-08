"""this is a script that traverse the TODAG to find TODOs"""
import logging
import sys
from utils import Logger, Loader, open_termdown
import argparse
from datetime import datetime, timedelta
import interactions
import uuid
logger = None

def get_todos(
        cards, 
        _logger=None,
        planning=True):
    """
    traverses the DAG and find nodes with with all completed parents
    filter todos based on location contraints

    return: list[[weight,uuid]] with the todos sorted by priority of component
    """
    res = []
    if _logger is None:
        # bad design, this loggers are passed as global and if I use this function from open.py logger (global on todo.py) is None so I need to pass as an arg in the function
        _logger = logger

    # get todos traversing the DAG
    for card_id, iter_card in cards.items():
        add = 1
        if type(card_id) is not uuid.UUID: continue
        for parent_id in iter_card.parents:
            # type(parent_id) = <class 'uuid.UUID'>
            parent = cards.get(parent_id)
            if not parent:
                pass  # means that parent got deleted
            elif parent.done == 0:
                add = 0
        if not iter_card.done and add:
            res.append(card_id)

    # sort todos by priority of component
    for index, todo in enumerate(res):
        cards[todo].debug_string = "======\nPRIORITY DEBUG\n\n"

        weight = cards[todo].get_priority()
        cards[todo].debug_string += "+get_priority() = {}\n".format(weight)
        components = find_components(cards, todo)
        for component in set(components):
            #
            # cumsum of all the priorities on the branch from root to card
            #
            weight += cards[component].get_priority()
            cards[todo].debug_string += "+component get_priority() {} = {}\n".format(
                    cards[component].name,
                    weight)
            #
            # this enable location for the TODAG
            # if a card has a location_constraint enabling the priority will be increased
            # by a factor of 100
            #
            if hasattr(cards[component], 'location_constraint'):
                if cards[component].location_constraint == _logger.location:
                    weight += 1000
                    cards[todo].debug_string += \
                            "+location_constraint= {}\n".format(weight)

        weight += cards[todo].get_reshake_priority()
        cards[todo].debug_string += "+get_reshake_priority() = {}\n".format(weight)
        
        res[index] = (weight, todo)

    res.sort()
    sorted_todos = res[::-1] # list(weight, UUID)

    # check if there is a plan
    plan = cards.get('planning') 
    # plan is a list of UUID
    if planning is True and plan is not None:
        for card_id in plan[::-1]:
            # from less priority to higher priority
            for index, elem in enumerate(sorted_todos):
                weight, todo_card_id = elem
                if todo_card_id == card_id:
                    # put in front
                    sorted_todos.pop(index)
                    sorted_todos = [elem] + sorted_todos

    return sorted_todos

def print_todo(
        cards, 
        todos, 
        index, 
        space=True, 
        _logger=True,
        details=True):
    """
    print( a given todos with a given index in the list of todos,
    also traverse the DAG to find the connected component representative
    (the last child)

    Args:
        cards: global dict of card instances
        todos: list[[weight, uuid]] with the todos
        index: int, index of the todo to print(
        space: print space
        _logger: log action
   
    """
    if space: print( "\n"*55)
    weight, todo = todos[index]
    if details:
        cards[todo].detail()
    else:
        #print only name
        print(cards[todo].name)
    if _logger: logger.log_action("open_todo",cards[todo].uuid)
    print( "Weight: " + str(weight) + "\n")

def find_components(cards, todo):
    """
    given a todo find the connected component it belongs to,
    where the component is a card with a reward
    i.e. traverse the DAG with a DFS until the last leaf

    Args:
        cards: global dict of card instances
        todo: (uuid) of the todo

    Returns:
        components: list[uuid] of representative cards for the component, without the todo
    """
    stack, res = [todo], []
    while stack:
        curr = stack.pop()
        curr_card = cards[curr]
        if curr_card.is_reward and curr != todo:
            res.append(curr)
        has_children = True if curr_card.children else False
        if has_children:
            for child in curr_card.children:
                stack.append(child)
    return res

def find_todo_card_from_query(todos, cards, query):
    """
    find todo card (so only on the edge not internal) from a query

    args:
    query (str) : query can be uuid or part of the name
    todos are the active cards todo, cards are all the cards

    todos = [(priority, UUID('564c7bd1-8266-4416-bdf5-ceb28405857e')]
    cards = {UUID, card.object}

    return index (todos index), card
    """
    found = "no"
    res = []
    for i, card in enumerate(todos):
        card_id = todos[i][1]
        if type(card_id) == uuid.UUID:
            card_object = cards[card_id]
            if str(card[1]) == query:
                # means that query was a todo code
                found = "yes"
                return i, card_object
            if query.lower() in card_object.name.lower():
                # query was just part of the name
                found = "some"
                res.append((i, card_object))
                # here need to choose now just returning the first
    if found == "no":
        print("[todo.py] didn't find specified task -t {}".format(query))
        return 0, None
    for choice, index_card in enumerate(res):
        print("[{}] {}".format(choice, index_card[1].name))
    print("Choose the card:")
    selected = input()
    return res[int(selected)]

def main():
    """script

    -load cards
    -look for todos
    -interactive session to print( todos: input 'n' for next todo
    """
    # argparse 
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--location', type=float, help='0.1 to force home, 0.13 to force work', nargs='?')
    parser.add_argument('-t', '--task', type=str, help='you can put a task id if you want to work specifically on that', nargs='?')
    args = parser.parse_args()

    # external IO
    global logger
    sys.path.append('../TODAG')
    from card import card
    logger = Logger(args.location)
    loader = Loader()
    cards = loader.cards
    todos = get_todos(cards)
    index = 0
    if args.task is not None:
        index, _ = find_todo_card_from_query(todos,cards,args.task)
    card = cards[todos[index][1]]
    card.load_from_notion()
    print_todo(cards, todos, index)
    open_termdown()
    start_time = datetime.now()
    # load come descriptin from notion
    while True:
        try:
            got = input()
            if got == "h" or got == "help":
                print("h, help\n"+
                        "d, done -> used when a task is finish at it will be deleted\n"+
                        "b, blocked -> I can not progress on this task for external reasons\n"+
                        "c, checked -> I worked on this task and didn't finished yet\n"+
                        "w, why -> why am I to do this task?\n"+
                        "m, mood -> right now I am feeling ..\n"+
                        "e, edit -> update the task\n"+
                        "n, notion -> sync with notion (upload text)\n"
                        "tdb, TODAG debugger\n"+
                        "")
            elif got == "d" or got == 'done':
                #check
                card_done = cards[todos[index][1]]
                interactions.checked_interaction(
                        logger, 
                        card_done, 
                        start_time)
                #done
                card_done.done = True
                logger.log_action("completed_todo",card_done.uuid)
                loader.write()
                print( "GREAT! Task is done ;)")
                return
            elif got == "c" or got == 'checked':
                card = cards[todos[index][1]]
                interactions.checked_interaction(
                        logger, 
                        card, 
                        start_time)
            elif got == "w" or got == "why":
                _, todo = todos[index]
                logger.log_action("examined_todo",cards[todo].uuid)
                components = find_components(cards, todo)
                for component in components:
                    cards[component].pretty_print()
            elif got == 'b' or got == "blocked":
                index += 1
                index %= len(todos)
                print_todo(cards, todos, index)
            elif got == "m" or got == "mood":
                interactions.mood_interaction(logger)
            elif got == "e" or got == "edit":
                _, todo = todos[index]
                cards[todo].edit()
            elif got == "n" or got == "notion":
                _, todo = todos[index]
                cards[todo].upload_to_notion()
            elif got == "tdb":
                _, todo = todos[index]
                cards[todo]._debug()
            else:
                print("CLOSING TODO")
                #uploads to notion only if there is already a notion link
                _, todo = todos[index]
                cards[todo].upload_to_notion(force=False)
                print("do you want to check? [y]/[n] -> close")
                got = input()
                if got == "y":
                    card = cards[todos[index][1]]
                    interactions.checked_interaction(
                            logger, 
                            card, 
                            start_time)
                else:
                    logger.log_action("quit","todo.py")
                    loader.write()
                    print( "\n"*60)
                    return
        except EOFError:
            exit()

if __name__ == "__main__":
    #logging.basicConfig(level=logging.INFO)
    main()
