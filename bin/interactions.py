"""interactions routines"""

def mood_interaction(logger, verbose=False):
    """
    args:
        logger -> instance of utils.Logger()

    input data for mood dashboard
    """
    print("How is mood right now? (int)")
    mood_value = int(input())
    print("Comment? (str)")
    mood_comment = input().replace(',','-')
    logger.log_action("mood",mood_value,mood_comment,verbose=verbose)
