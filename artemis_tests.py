import unittest
from artemis import *


class TestArtemis(unittest.TestCase):
    def test_refine_phrase(self):
        print("Test: refine_phrase")
        phrase = "qual o maior planeta do sistema solar"
        expected_output = "maior planeta sistema solar"
        self.assertEqual(refine_phrase(phrase), expected_output)

    def test_deepScrapper(self):
        print("Test: deepScrapper")
        search_terms = "maior planeta sistema solar"
        result = deepScrapper(search_terms)
        self.assertIsNotNone(result)

    def test_isTurnOffCommand(self):
        print("Test: isTurnOffCommand")
        text = "artemis, desligar"
        self.assertTrue(isTurnOffCommand(text))

    def test_hasValidKeyword(self):
        print("Test: hasValidKeyword")
        text = "artemis, pesquisar maior planeta sistema solar"
        self.assertTrue(hasValidKeyword(text))

    def test_process_input(self):
        print("Test: process_input")
        raw_input1 = "ola"
        raw_input2 = "estou bem, e voce?"
        expected_output = "Olá"
        expected_output2 = "Estou bem, e você?"
        response1 = process_input(raw_input1)
        response2 = process_input(raw_input2)
        self.assertEqual(response1, expected_output)
        self.assertEqual(response2, expected_output2)

    def test_answer_question(self):
        print("Test: answer_question")
        question = "O que é um cometa?"
        response = answer_question(question)
        self.assertNotEqual(response, "Palavra-chave não encontrada")


if __name__ == "__main__":
    unittest.main()
