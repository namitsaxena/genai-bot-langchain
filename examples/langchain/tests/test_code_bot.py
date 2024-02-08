import unittest
from CodeApi import CodeBot


class TestCodeBot(unittest.TestCase):

    @unittest.skip("only for manual execution")
    def test_with_user_input(self):
        temperature = 0
        max_output_tokens = 2048
        bot = CodeBot(temperature=temperature, max_output_tokens=max_output_tokens)

        prompt = input('enter prompt >: ')
        while prompt:
            bot.chat(prompt)
            prompt = input('enter prompt >: ')

        print("Chat finished.")
        bot.chat(None)

    def test_code_chat(self):
        bot = CodeBot()

        prompt = "Please help write a function to calculate the min of two numbers in python"
        bot.chat(prompt)

        prompt = "can you explain the code line by line?"
        bot.chat(prompt)

        prompt = "can you add docstring, typehints and pep8 formating to the code?"
        bot.chat(prompt)

        prompt = None
        bot.chat(prompt)

    def test_code_debugging(self):
        temperature = 0
        max_output_tokens = 2048
        bot = CodeBot(temperature=temperature, max_output_tokens=max_output_tokens)

        prompt = '''
        Debug the following scenario based on the problem statement, logic, code and error. Suggest possible cause of error and how to fix that.
        Expalin the error in detail.

        Problem statement: I am trying to write a Python function to implement a simple recommendation system.
        The function should take a list of users and a list of items as input and return a list of recommended items for each user.
        The recommendations should be based on the user's past ratings of items.

        Logic: The function should first create a user-item matrix, where each row represents a user and each column represents an item.
        The value of each cell in the matrix represents the user's rating of the item.
        The function should then use a recommendation algorithm, such as collaborative filtering or content-based filtering, \
        to generate a list of recommended items for each user.

        Code:
        ```
        import numpy as np

        def generate_recommendations(users, items):
          """Generates a list of recommended items for each user.

          Args:
            users: A list of users.
            items: A list of items.

          Returns:
            A list of recommended items for each user.
          """

          # Create a user-item matrix.
          user_item_matrix = np.zeros((len(users), len(items)))
          for user_index, user in enumerate(users):
            for item_index, item in enumerate(items):
              user_item_matrix[user_index, item_index] = user.get_rating(item)

          # Generate recommendations using a recommendation algorithm.
          # ...

          # Return the list of recommended items for each user.
          return recommended_items

        # Example usage:
        users = [User1(), User2(), User3()]
        items = [Item1(), Item2(), Item3()]

        recommended_items = generate_recommendations(users, items)

        print(recommended_items)
        ```
        Error:
        AttributeError: 'User' object has no attribute 'get_rating'

                ```
        '''
        bot.chat(prompt)
