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


def write_cards():
    """
    write current cards to CARDS
    """
    with open('cards.pkl', 'wb') as data:
        pickle.dump(CARDS, data)


if __name__ == "__main__":
    sys.path.append('../TODAG')
    from card import card
    CARDS = load_cards()
    print_cards()
    print "\n\nA: new card\nB: add parent\n"
    got = raw_input()
    if got == 'A':
        new_card = card()
        new_card.populate()
        CARDS[new_card.uuid] = new_card
    elif got == 'B':
        import uuid
        print "Input UUID of children card:"
        read_id = raw_input()
        #import pdb;pdb.set_trace() 
        read_card = CARDS.get(uuid.UUID(read_id))
        if not read_card:
            "NOT EXISTING"
        else:
            print "Adding new parent to '{}'".format(read_card.name)
            new_card = read_card.add_parent()
            CARDS[new_card.uuid] = new_card
    else:
        print 'not implemented'
    write_cards()
