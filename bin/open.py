"""this is a script that let you look into the DAG and modify cards"""
import sys
from utils import Logger, Loader
CARDS = None
logger = None

def print_cards():
    """
    calls the pretty_print( method on every card in the CARDS dict
    """
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


if __name__ == "__main__":
    sys.path.append('../TODAG')
    from card import card
    import uuid
    logger = Logger()
    loader = Loader()
    CARDS = loader.cards
    print_cards()
    print("\n\n[A] new card\n[B] add parent\n[C] delete card\n" + \
          "[D] explore decision tree\n[E] edit card\n")
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
    else:
        exit("error: NOT IMPLEMENTED")
    logger.log_action("quit","open.py")
    loader.write_cards()
