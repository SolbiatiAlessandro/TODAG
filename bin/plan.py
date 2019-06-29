from utils import Logger, Loader, open_termdown
try:
    import card
except:
    import sys
    sys.path.append("../TODAG")
    import card
import todo

class planning_session():
    """
    """

    def __init__(self):
        self.logger = Logger()
        self.logger.log_action("open","plan.py")
        self.loader = Loader()
        self.todos = todo.get_todos(self.loader.cards, _logger=self.logger)

    def _print_current_plan(self):
        print("==== CURRENT PLAN ====")
        for index in self.planned_indexes:
            print("-----{}-----".format(index))
            todo.print_todo(self.loader.cards, self.todos, index, space=False)
        print("====              ====")

    def _edit_current_plan(self):
        while True:
            print("this is the current plan:")
            self._print_current_plan()
            print("which item you want to edit (int), -1 for quit")
            index = int(input())
            if index == -1:
                return
            print('you are editing item number {}, \
                    what todo you want to replace it with? (UUID or query)')
            query = input()
            new_index, new_card = todo.\
                    find_todo_card_from_query(self.todos, self.cards, query)
            self.planned_indexes[self.planned_indexes.index(index)] = \
                    new_index
            print("item replaced succesfully")


    def _run_planning_session(self, todos_number):
        print("== Planning session for tomorrow ==")
        print("\nhow many todos will you work on tomorrow? (int)")
        todos_number = int(input())
        # the planned index are the one default given by todag
        self.planned_indexes = range(0, todos_number)
        self._print_current_plan()
        print("\ndo you want to change your planned items? (y/n)")
        got = input()
        if got == "yes":
            print("[plan.py] start _edit_current_plan")
            self._edit_current_plan()
            print("[plan.py] quitted _edit_current_plan")
            print("[plan.py] saving to local cards.pkl current plan:")
            print(self.planned_indexes)
            self.logger.log_action("edit_plan",\
                    ''.join(map(str, self.planned_indexes)))
            old_planned_index = self.cards.get('planning')
            if old_planned_index is not None:
                print("[plan.py] overwriting current planned_index:") 
                print(old_planned_index)
            plan_to_bump = map(lambda index: self.todos[index][1], \
                    self.planned_indexes)
            print(plan_to_bump)
            self.cards['planning'] = plan_to_bump

        else:
            print("[plan.py] quitting _run_planning_session")

    def _print_saved_plan(self):
        print("== in-memory plan ==")
        saved_plan = self.cards.get("planning")
        if saved_plan is None:
            print("no saved plan")
        else:
            for card_id in plan:
                self.cards[card_id].detail()
        print("== ==")


    def run(self):
        """
        now just asking for number of todo,
        later will actually ask or compute the number of time available 
        and automatically select number of todos when todos will have a
        "time to complete" attribute implemented
        """

        try:
            while True:
                print("\n\n=====prompt====="+
                        "\n[A] run planning session"+
                        "\n[B] print current plan (memory)"+
                        "\n[C] print saved plan (disk)")
                got = input()
                if got == "A":
                    self._run_planning_session()
                if got == "B":
                    self._print_current_plan()
                if got == "C":
                    self._print_saved_plan()
                else:
                    print("[bin:plan.py] {} choice not implemented, quitting program".format(got))
                    break
        except Exception as e:
            import traceback
            traceback.print_exc()
            import pdb;pdb.set_trace()
            print(e)
            print("[bin:plan.py] you did something illegal")
        # external IO uploaders
        self.logger.log_action("quit","plan.py")
        self.loader.write()
                
if __name__ == "__main__":
    sess = planning_session()
    sess.run()
