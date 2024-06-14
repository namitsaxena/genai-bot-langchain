import os
from flask import Flask, render_template, request, jsonify


class ChatWebApp():

    # workaround to run the server inside a class instance
    # if declaring directly, it's straight forward
    def __init__(self, bot, templates_dir_path='../../resources/templates'):
        templates_dir = os.path.abspath(templates_dir_path)
        self.app = Flask(__name__, template_folder=templates_dir)
        self.bot = bot

        # This is indented at __init__'s level, so a new instance of the function
        # is defined every time __init__ runs. That means a new instance
        # is defined for each instance of the class, and so it can be wrapped with
        # the instance's "self" value.
        @self.app.route('/')
        def home():
            return render_template("index.html")

        @self.app.route("/get")
        def get_bot_response():
            userText = request.args.get('msg')
            response = self.bot.process(userText)
            print(f"Response Received: {response}")
            if response is None:
                response = "Agent didn't reply!!"
            # return str(bot.get_response(userText))
            return response

        self.home = home

    def run(self):
        self.app.run()
