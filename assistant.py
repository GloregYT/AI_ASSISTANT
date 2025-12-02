import random
from datetime import datetime
import os

NAME = "Jarvis"
DEFAULT_PERSONALITY = "Вітаю Вас! Я Jarvis, ШІ-асистент, який допоможе у будь якій ситуації)"

def load_persona(filename="persona.txt"):
    if os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                text = f.read().strip()
                if text:
                    return text
        except Exception:
            pass
    return DEFAULT_PERSONALITY

PERSONALITY = load_persona()

greatings = ["Вітаю, Сер! Готовий відповідати/допомагати Вам", "Привіт! Слухаю твої побажання!", "Хай бро, ай вейт йор квешен)"]

jokes = ["Жарт 1", "Жарт 2", "Жарт 3"]

def random_joke():
    return random.choice(jokes)

def random_greating():
    return random.choice(greatings)

def analyze_text(text):
    if not text:
        return "empty"
    elif "жарт" in text or "сміши" in text:
        return "joke"
    elif "мотив" in text or "порада" in text:
        return "motivate"
    elif "гроші" in text or "грошей" in text:
        return "money"
    elif "час" in text:
        return "time"
    elif "бувай" in text or "до зустрічі" in text:
        return "exit"
    return "unknown"


def get_response(text):
    t = text.lower()
    tag = analyze_text(t)
    
    if "empty" in tag:
        return f"{NAME}: Ви нічого не сказали! Спробуйте ще раз)"
    if "joke" in tag:
        return f"{NAME}: {random_joke()}"
    if "money" in tag:
        return f"{NAME}: На вашій карті: {random.randint(0, 100000)}₴ гривень." #return f"{NAME}: На вашій карті: " + str(random.randint(0, 100000)) + " гривень."
    if "motivate" in tag:
        return f"{NAME}: Ось Вам порада - Через 20 років ви будете більше розчаровані тими речами, які ви не робили, ніж тими, які ви зробили."
    if "time" in tag:
        return f"{NAME}: Зараз {datetime.now().strftime("%H:%M")}"
    if "exit" in tag:
        return "exit"
    return f"{NAME}: Не розумію, що Ви хочете. Що це має значити?"


def main():
    print(PERSONALITY)
    print(f"{NAME}: {random_greating()}")
    while True:
        user = input(f"ALEXEY: ").strip()
        response = get_response(user)
        if response == "exit":
            print(f"{NAME}: Бувайте. Чекаю на Вас! :)")
            break
        print(response)


if __name__ == "__main__":
    main()