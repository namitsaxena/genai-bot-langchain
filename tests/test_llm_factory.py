import unittest
from src.LLMFactory import get_llm
from src.LLMFactory import PROVIDER_OPENAI, PROVIDER_VERTEX


class TestModels(unittest.TestCase):

    def setUp(self):
        print("opeai test: performing setup...")

    def test_open_ai_simple_prediction(self):
        llm = get_llm(PROVIDER_OPENAI)
        prompt = "Write a 2-day itinerary for France."
        prediction = llm.predict(prompt)
        print(f"Predication: {prediction}")

    def test_open_vertex_simple_prediction(self):
        llm = get_llm(PROVIDER_VERTEX)
        prompt = "Write a 2-day itinerary for France."
        prediction = llm.predict(prompt)
        print(f"Predication: {prediction}")
