"""this is a script that traverse the TODAG to find TODOs"""
import sys
from open import load_cards, write_cards
LOCATION = None

def get_todos(cards):
    """
    traverses the DAG and find nodes with with all completed parents
    filter todos based on location contraints

    return: list[[weight,uuid]] with the todos sorted by priority of component
    """
    res = []

    # get todos traversing the DAG
    for card_id, iter_card in cards.items():
        add = 1
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
        weight = 0
        components = find_components(cards, todo)
        for component in set(components):
            #
            # cumsum of all the priorities on the branch from root to card
            #
            if hasattr(cards[component], 'priority'):
                weight += cards[component].priority

            #
            # this enable location for the TODAG
            # if a card has a location_constraint enabling the priority will be increased
            # by a factor of 100
            #
            if hasattr(cards[component], 'location_constraint'):
                if cards[component].location_constraint == LOCATION:
                    weight += 100
        
        res[index] = (weight, todo)
    res.sort()

    return res[::-1]


def print_todo(cards, todos, index):
    """
    print a given todos with a given index in the list of todos,
    also traverse the DAG to find the connected component representative
    (the last child)

    Args:
        cards: global dict of card instances
        todos: list[[weight, uuid]] with the todos
        index: int, index of the todo to print
    """
    print "\n"*55
    weight, todo = todos[index]
    cards[todo].detail()
    print "Weight: " + str(weight) + "\n"


def find_components(cards, todo):
    """
    given a todo find the connected component it belongs to,
    where the component is a card with a reward
    i.e. traverse the DAG with a DFS until the last leaf

    Args:
        cards: global dict of card instances
        todo: (uuid) of the todo

    Returns:
        components: list[uuid] of representative cards for the component
    """
    stack, res = [todo], []
    while stack:
        curr = stack.pop()
        curr_card = cards[curr]
        if curr_card.is_reward:
            res.append(curr)
        has_children = True if curr_card.children else False
        if has_children:
            for child in curr_card.children:
                stack.append(child)
    return res


def main():
    """script

    -load cards
    -look for todos
    -interactive session to print todos: input 'n' for next todo
    """
    sys.path.append('../TODAG')
    from card import card
    cards = load_cards()
    todos = get_todos(cards)
    index = 0
    print_todo(cards, todos, index)
    while True:
        try:
            got = raw_input()
            if got == 'done':
                card_done = cards[todos[index][1]]
                card_done.done = True
                write_cards(cards)
                print "GREAT!"
                return
            elif got == "why":
                _, todo = todos[index]
                components = find_components(cards, todo)
                for component in components:
                    cards[component].pretty_print()
            elif got == 'n':
                index += 1
                index %= len(todos)
                print_todo(cards, todos, index)
            else:
                print "\n"*60
                return
        except EOFError:
            exit()


if __name__ == "__main__":
    try: # reading location from phyiscal machine
        import subprocess
        read_location = subprocess.check_output('/Users/lessandro/coding/SCRIPTS/whereami')
        start = read_location.find('Longitude')+len("Longitude: -")
        end = start + 4
        LOCATION = float(read_location[start:end])
    except Exception as e:
        print("warning: couldn't get location of machine\n'")
        print(e)
    main()
