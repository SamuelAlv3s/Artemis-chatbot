from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import json
from bs4 import BeautifulSoup
import requests
import chardet
import pyfiglet
from rich.console import Console
from rich.style import Style
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot import languages
from unidecode import unidecode
from spacy.cli.download import download

# download(model="en_core_web_sm")

# import nltk
# nltk.download("punkt")
# nltk.download("stopwords")

languages.ENG.ISO_639_1 = "en_core_web_sm"

figlet = pyfiglet.Figlet()

with open("config.json", mode="r", encoding="utf-8") as configFile:
    config = json.load(configFile)

prefix = config["name"]
trainingList = config["trainingList"]
astronomyKeyWords = config["keywords"]

chatbot = ChatBot(prefix)
trainer = ListTrainer(chatbot)
trainer.train(trainingList)


def refine_phrase(phrase):
    tokens = word_tokenize(phrase)

    stop_words = set(stopwords.words("portuguese"))
    filtered_tokens = [word for word in tokens if word.lower() not in stop_words]

    refined_phrase = " ".join(filtered_tokens)

    refined_phrase = refined_phrase.strip()

    return refined_phrase


def deepScrapper(search_terms, retry=0):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    }

    response = requests.get(
        f"https://www.google.com/search?q={search_terms}", headers=headers
    )

    soup = BeautifulSoup(response.text, "html.parser")

    search_results = soup.find_all("div", {"class": "g"})
    first_result = search_results[retry].find("a")["href"]

    try:
        response = requests.get(first_result, headers=headers)

        encoding = chardet.detect(response.content)["encoding"]
        decoded_response = response.content.decode(encoding)

        soup = BeautifulSoup(decoded_response, "html.parser")

        main_content = soup.find("main")
        paragraphs = main_content.find_all("p")

        paragraphs_without_class = [
            paragraph for paragraph in paragraphs if not paragraph.has_attr("class")
        ]

        finalResult = [paragraph.text for paragraph in paragraphs_without_class]

        finalResult = " ".join(finalResult)
        console = Console()
        console.print("")
        console.print(finalResult, style=Style(color="green"))
        return finalResult
    except Exception as e:
        # print(e)
        if retry + 1 > 5:
            print("Não foi possível encontrar um resultado")
            return None
        return deepScrapper(search_terms, retry + 1)


def isTurnOffCommand(text):
    return "desligar" in text.lower()


def hasValidKeyword(text):
    for keyword in astronomyKeyWords:
        if keyword.lower() in text.lower():
            return True
    return False


def welcomeMessage():
    print(figlet.renderText(prefix))
    print("Para desligar, digite desligar")
    print("")


def process_input(raw_input):
    matchQuestion = raw_input
    for question in trainingList:
        if unidecode(raw_input.lower()) == unidecode(question.lower()):
            matchQuestion = question
            break
    return matchQuestion


def answer_question(question):
    response = chatbot.get_response(question)
    if response.confidence > 0.7:
        print(response)
        return response
    else:
        if hasValidKeyword(question):
            search_terms = refine_phrase(question)
            deepScrapper(search_terms)
        else:
            print("Não entendi a pergunta...")
            return "Palavra-chave não encontrada"


def initArtemis():
    welcomeMessage()
    isRunning = True
    while isRunning:
        try:
            text = input("Digite um comando: ")
        except KeyboardInterrupt:
            print("Desligando...")
            isRunning = False
            break

        if isTurnOffCommand(text):
            print("Desligando...")
            isRunning = False
            break
        userQuestion = process_input(text)
        answer_question(userQuestion)


if __name__ == "__main__":
    initArtemis()
