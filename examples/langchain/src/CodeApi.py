from vertexai.language_models import CodeChatModel


class CodeBot:

    def __init__(self, model="codechat-bison@002", temperature=0.2, max_output_tokens=1024):
        self.code_chat_model = CodeChatModel.from_pretrained(model)
        self.temperature = temperature
        self.max_output_tokens = max_output_tokens
        self.code_chat = None  # chat session

    def chat(self, prompt):
        if not self.code_chat:
            print("Code Chat Starting..")
            self.code_chat = self.code_chat_model.start_chat(temperature=self.temperature, max_output_tokens=self.max_output_tokens)

        if prompt is None:
            print("Code Chat Ending! Bye.")
            self.code_chat = None
        else:
            print(f"Prompt: {prompt}, Response:")
            # chat
            print(
                self.code_chat.send_message(prompt).text
            )
