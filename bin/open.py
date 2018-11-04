"""this is a script that let you look into the DAG and modify cards"""
import pickle
import sys

CARDS = None


def load_cards():
    """
    load cards from pickle to global variable CARDS

    Exception:
        to be used after having imported card, otherwise
        will raise exception
    """
    with open('cards.pkl', 'rb') as data:
        return pickle.load(data)


def print_cards():
    """
    calls the pretty_print method on every card in the CARDS dict
    """
    for _, _card in CARDS.items():
        _card.pretty_print()


def write_cards(cards):
    """
    write current cards to CARDS
    """
    with open('cards.pkl', 'wb') as data:
        pickle.dump(cards, data)


def find_rewards(cards):
    """
    traverse the DAG and find all nodes with a reward

    return: list[uuid] with reward cards
    """
    return [card_id for card_id, _card in cards.items() if _card.is_reward]


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


if __name__ == "__main__":
    sys.path.append('../TODAG')
    from card import card
    import uuid
    CARDS = load_cards()
    print_cards()
    print "\n\n[A] new card\n[B] add parent\n[C] delete card\n" + \
          "[D] explore decision tree\n"
    got = raw_input()
    if got == 'A':
        new_card = card()
        new_card.populate()
        CARDS[new_card.uuid] = new_card
        print "Card added succesfully"
    elif got == 'B':
        print "Input UUID of children card:"
        read_id = raw_input()
        read_card = CARDS.get(uuid.UUID(read_id))
        if not read_card:
            exit("error: CARD NOT EXISTING")
        else:
            print "Adding new parent to '{}'".format(read_card.name)
            new_card = read_card.add_parent()
            CARDS[new_card.uuid] = new_card
            print "Card added succesfully"
    elif got == 'C':
        print "Input UUID of card to delete"
        read_id = raw_input()
        read_card = CARDS.get(uuid.UUID(read_id))
        if not read_card:
            exit("error: CARD NOT EXISTING")
        del(CARDS[uuid.UUID(read_id)])
        print "Card deleted succesfully"
    elif got == 'D':
        print "Rewards on the DAG:\n"
        rewards = find_rewards(CARDS)
        for index, reward in enumerate(rewards):
            print "[{}]".format(index)
            CARDS[reward].detail()
        print "\n"
        print "Choose reward card you want backtrack from"
        got_index = int(raw_input())
        if got_index in range(len(rewards)):
            reward_id = rewards[got_index]
            print "\n[REWARD]"
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
                print (" "*(ITEM_SIZE/2)+"^"+" "*(ITEM_SIZE/2))*len(layer)
                print separator
                print content
                print separator
        else:
            exit("error: reward index out of range")

    else:
        exit("error: NOT IMPLEMENTED")
    write_cards(CARDS)
