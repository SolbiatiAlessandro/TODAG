"""this is a script that traverse the TODAG to find TODOs"""
import sys
from open import load_cards, write_cards


def get_todos(cards):
    """
    traverses the DAG and find nodes with with all completed parents

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
        for component in find_components(cards, todo):
            if hasattr(cards[component], 'priority'):
                weight += cards[component].priority
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
    components = find_components(cards, todo)
    cards[todo].detail()
    print "Weight: " + str(weight) + "\n"
    for component in components:
        cards[component].pretty_print()


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
        got = raw_input()
        if got == 'done':
            card_done = cards[todos[index]]
            card_done.done = True
            write_cards(cards)
            return
        elif got == 'n':
            index += 1
            index %= len(todos)
            print_todo(cards, todos, index)
        else:
            print "\n"*60
            return


if __name__ == "__main__":
    main()
