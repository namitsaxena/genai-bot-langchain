# #######################################
# contains general tool functions
# Function must have a docstring if description not provided.
# functions can be in any class - botagent, separate, etc
# #######################################
import random

BOT_NAME = "Gort"


# expects doc string in this case
# since description is not provided above
# but didn't ask for the same in the other function(TODO)
# What's your name, who are you both work
def get_bot_name():
    """
    gets the bot's name
    the name to return when asked for your name
    This is not when asked for
    :return: the name of the agent
    """
    return BOT_NAME


def some_function():
    """
    generates a random number
    :return: random number
    """
    return random.random()


def get_current_date():
    """
    Gets the current date (today), in the format YYYY-MM-DD
    """
    from datetime import datetime
    todays_date = datetime.today().strftime("%Y-%m-%d")
    return todays_date


def get_current_time():
    """
    Gets the current date (today), in the format YYYY-MM-DD
    """
    from datetime import datetime
    current_time = datetime.today().strftime("%Y-%m-%d_%H%M%S")
    return current_time
