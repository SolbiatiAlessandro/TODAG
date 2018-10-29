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


def get_parents(cards, todo):
    """
    given a todo find all the parents of the todo and return them
    i.e. backtrack on the DAG

    Args:
        cards: global dict of card instances
        todo: (uuid) of the todo

    Returns:
        parents: list[int, list[int, list[int]], ..]
            the format for the return value is unusual, for
            visualization reason every time the DAG branches during the
            backtrack, one whole branch (list[int]) while be a single
            element of the list, instead of appending all the elements
            in the branch to the parents list
    """
    res = []
    curr = todo
    while CARDS.get(curr) and CARDS[curr].parents:
        if len(CARDS[curr].parents) == 1:
            curr = CARDS[curr].parents[0]
            res.append(curr)
        else:
            last = []
            for parent in CARDS[curr].parents:
                last.append([parent] + get_parents(cards, parent))
            return res + [last]
    return res


if __name__ == "__main__":
    sys.path.append('../TODAG')
    from card import card
    import uuid
    CARDS = load_cards()
    print_cards()
    print "\n\n[A] new card\n[B] add parent\n[C] delete card\n\
    [D] explore decision tree\n"
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
            parents_id = get_parents(CARDS, reward_id)
            print parents_id  # TODO: figure out how to print this stuff
        else:
            exit("error: reward index out of range")

    else:
        exit("error: NOT IMPLEMENTED")
    write_cards(CARDS)
