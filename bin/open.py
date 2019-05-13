"""this is a script that let you look into the DAG and modify cards"""
import sys
import csv
from utils import Logger, Loader
sys.path.append('../TODAG')
from card import card
import uuid
import argparse
CARDS = None
logger = None
buffer_location = "./buffer.csv" # move this to a conflig and implement on cloud 

def print_cards():
    """
    calls the pretty_print( method on every card in the CARDS dict
    """
    print("\n=====cards=====")
    for _, _card in CARDS.items():
        _card.pretty_print()

def find_rewards(cards):
    """
    traverse the DAG and find all nodes with a reward

    return: list[uuid] with reward cards
    """
    return [card_id for card_id, _card in cards.items()
            if (_card.is_reward and not _card.done)]

def validate(parent_id):
    """
    returns True if parent is valid

    data is often corrupted, because of deletion of cards
    there are some id that point to non-exisiting cards.
    This procedure validate that the parent exists
    """
    if CARDS.get(parent_id) is None:
        return False
    return True

def backward_bfs(cards, todo):
    """
    given a todo launches a BFS backward and returns
    the other cards layered by distance

    Args:
        cards: global dict of card instances
        todo: (uuid) of the todo

    Returns:
        ordered_parents: list[list[int], list[int], ..]
            every member is a layer of the DAG seen
            backward from the input todo, where a layer is a set
            of cards with same distance from starting point
            of the bfs
    """

    ordered_parents = []
    queue = [todo]
    distances = {todo: 0}
    while queue:
        elem = queue.pop()

        # here we populate ordered_parents
        if distances.get(elem) is None:
            exit("error: distances in bfs was not assigned")
        distance = distances[elem]
        if distance < len(ordered_parents):
            # every layer is a elem of the list indexed by its distance
            ordered_parents[distance].append(elem)
        else:
            ordered_parents.append([elem])

        for parent in cards[elem].parents:
            if validate(parent) and not cards[parent].done:
                distances[parent] = distances[elem] + 1
                queue.insert(0, parent)

    return ordered_parents

def read_card(cards):
    """utiliy to handle read card exceptions"""
    _read_id = input()
    _read_card = cards.get(uuid.UUID(_read_id))
    if not _read_card:
        exit("error: CARD NOT EXISTING")
    return _read_card

def read_buffer():
    """
    return iterator on buffer items

    buffer location ./buffer.csv
    format name,priority
    """
    with open(buffer_location, "r") as bufferfile:
        _reader = csv.reader(bufferfile)
        return iter([row for row in _reader])

def write_buffer(buffer_list):
    """
    write unused items inside buffer
    """
    with open(buffer_location, "w") as bufferfile:
        _writer = csv.writer(bufferfile)
        for row in buffer_list:
            _writer.writerow(row)

if __name__ == "__main__":
    # argparse 
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--location', type=float, help='0.1 to force home, 0.13 to force work', nargs='?')
    args = parser.parse_args()

    # external IO downloaders
    logger = Logger(args.location)
    loader = Loader()
    buffer_iterator = read_buffer()
    CARDS = loader.cards

    print_cards()
    try:
        while True:
            print("\n\n=====prompt====="+
                    "\n[A] new card"+
                    "\n[B] add parent"+
                    "\n[C] delete card"+
                    "\n[D] explore decision tree"+
                    "\n[E] edit card"+
                    "\n[F] check next item from todo buffer"+
                    "\n[G] print cards"+
                    "\n[H] examine single card"+
                    "\n[I] mood dashboard")

            got = input()
            if got == 'A':
                new_card = card()
                new_card.populate()
                CARDS[new_card.uuid] = new_card
                print("Card added succesfully")
                logger.log_action("add_card",new_card.uuid)
            elif got == 'B':
                print( "Input UUID of children card:")
                child = read_card(CARDS)
                print( "\nAdding new parent to '{}'\n".format(child.name))
                print( "\n\n[A] -> Existing Card\n[B] -> New Card\n")
                gott = input()
                if gott == 'B':
                    new_card = child.add_parent()
                    CARDS[new_card.uuid] = new_card
                    logger.log_action("add_card",new_card.uuid)
                elif gott == 'A':
                    print( "Input UUID of parent card:")
                    parent = read_card(CARDS)
                    parent.children.append(child.uuid)
                    child.parents.append(parent.uuid)
                    logger.log_action("add_edge",parent.uuid)
                else:
                    exit("Error: not implemented")
                print( "Parent added succesfully")
            elif got == 'C':
                print( "Input UUID of card to delete")
                read_id = input()
                read_card = CARDS.get(uuid.UUID(read_id))
                if not read_card:
                    exit("error: CARD NOT EXISTING")
                logger.log_action("delete_card",read_card.name)
                del(CARDS[uuid.UUID(read_id)])
                print( "Card deleted succesfully")
            elif got == 'D':
                print( "Rewards on the DAG:\n")
                rewards = find_rewards(CARDS)
                for index, reward in enumerate(rewards):
                    print( "[{}]".format(index))
                    CARDS[reward].detail()
                print( "\n")
                print( "Choose card you want backtrack from")
                got_index = int(input())
                if got_index in range(len(rewards)):
                    reward_id = rewards[got_index]
                    print( "\n[REWARD]")
                    logger.log_action("explore_tree",CARDS[reward_id].uuid)
                    CARDS[reward_id].detail()
                    parents = backward_bfs(CARDS, reward_id)
                    parents = parents[1:]
                    ITEM_SIZE = 30
                    for layer in parents:
                        separator = (("="*ITEM_SIZE)+"|")*len(layer)
                        content = ""
                        for parent in layer:
                            name = CARDS[parent].name
                            content += name[:ITEM_SIZE] + \
                                " "*(ITEM_SIZE - min(len(name), ITEM_SIZE))+"|"
                        print((" "*(int(ITEM_SIZE/2))+"^"+" "*(int(ITEM_SIZE/2)))*len(layer))
                        print(separator)
                        print(content)
                        print(separator)
                else:
                    exit("error: reward index out of range")
            elif got == 'E':
                print( "Input UUID of card to edit")
                read_id = input()
                read_card = CARDS.get(uuid.UUID(read_id))
                if not read_card:
                    exit("error: CARD NOT EXISTING")
                read_card.edit()
                logger.log_action("edit_card",read_card.uuid)
                print( "Card edited succesfully")
            elif got == 'F':
                try:
                    buffer_next = next(buffer_iterator)
                    print("\nNext item on the TODO buffer (item will be deleted from buffer)\n"+
                            "\nitem: "+str(buffer_next[0])+
                            "\npriority: "+str(buffer_next[1])+
                            "\n\n")
                    logger.log_action("pop_buffer",buffer_next[0])
                except StopIteration:
                    buffer_next = None
                    print("Buffer empty")
            elif got == 'G':
                print_cards()
            elif got == 'H':
                print("card id you want to examine")
                read_id = input()
                read_card = CARDS.get(uuid.UUID(read_id))
                if not read_card:
                    exit("error: CARD NOT EXISTING")
                read_card.detail()
            elif got == 'I':
                print("How is mood right now?")
                mood_value = int(input())
                logger.log_action("mood",mood_value,verbose=True)


            else:
                print("[bin:open.py] {} choice not implemented, quitting program".format(got))
                break
    except Exception as e:
        import pdb;pdb.set_trace()
        print(e)
        print("[bin:open.py] you did something illegal")
    # external IO uploaders
    logger.log_action("quit","open.py")
    loader.write()
    write_buffer(list(buffer_iterator))
