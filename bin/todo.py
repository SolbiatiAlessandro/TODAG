"""this is a script that traverse the TODAG to find TODOs"""
import sys
from open import load_cards, write_cards


def get_todos(cards):
    """
    traverses the DAG and find nodes with with all completed parents

    return: list[uuid] with the todos
    """
    res = []
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
    return res


def print_todo(cards, todos, index):
    """
    print a given todos with a given index in the list of todos,
    also traverse the DAG to find the connected component representative
    (the last child)

    Args:
        cards: global dict of card instances
        todos: list[uuid] with the todos
        index: int, index of the todo to print
    """
    print "\n"*55
    todo = todos[index]
    components = find_components(cards, todo)
    cards[todo].detail()
    for component in components:
        print "\n"
        cards[component].pretty_print()


def find_components(cards, todo):
    """
    given a todo find the connected component it belongs to,
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
        has_children = True if curr_card.children else False
        if has_children:
            for child in curr_card.children:
                stack.append(child)
        else:
            res.append(curr)
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
