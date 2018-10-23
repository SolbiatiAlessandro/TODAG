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


if __name__ == "__main__":
    sys.path.append('../TODAG')
    from card import card
    import uuid
    CARDS = load_cards()
    print_cards()
    print "\n\n[A] new card\n[B] add parent\n[C] delete card\n"
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
    else:
        exit("error: NOT IMPLEMENTED")
    write_cards(CARDS)
