from utils import Logger, Loader, open_termdown
import todo

class planning_session():
    """
    """

    def __init__(self):
        self.logger = Logger()
        self.logger.log_action("open","plan.py")
        self.loader = Loader()
        self.todos = todo.get_todos(self.loader.cards)

    def plan(self):
        """
        now just asking for number of todo,
        later will actually ask or compute the number of time available 
        and automatically select number of todos when todos will have a
        "time to complete" attribute implemented
        """
        print("="*30)
        print("Planning session for tomorrow")
        print("="*30)
        print("how many todos will you work on tomorrow? (int)")
        todos_number = int(input())
        # the planned index are the one default given by todag
        planned_indexes = range(0, todos_number)
        print("==== CURRENT PLAN ====")
        for index in planned_indexes:
            print("-----{}-----".format(index))
            todo.print_todo(self.loader.cards, self.todos, index, space=False)
