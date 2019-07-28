"""interactions routines"""
from datetime import datetime

def mood_interaction(logger, verbose=False):
    """
    args:
        logger -> instance of utils.Logger()

    input data for mood dashboard
    """
    print("How is mood right now? (int)")
    mood_value = float(input().replace(',','.'))
    print("Comment? (str)")
    mood_comment = input().replace(',','-')
    logger.log_action("mood",mood_value,mood_comment,verbose=verbose)

def checked_interaction(logger, card, start_time, verbose=False):
    """
    checking means working on a TODO and logging in time

    args:
        logger -> instance of utils.Logger()
        card -> instance of  <Card>
        start_time - > datetime.now()
    """
    end_time = datetime.now()
    _duration = end_time - start_time
    duration = str(_duration.days * 24 + _duration.seconds / 3600)
    print("Nice, you just logged {} hours for this card".format(duration))
    # preparing payload, more info on todo_information in log_action function
    todo_information = {
            'checked_task_uuid': str(card.uuid),
            'checked_task_name' : str(card.name),
            'checked_task_description' : str(card.description),
            }
    logger.log_action("checked_todo",
            todo_information,
            duration,
            verbose=verbose)
