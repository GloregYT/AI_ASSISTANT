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

empty = [
    "Тапниі по клаві, хоч одну клавішу",
    "Ви нічого не сказали! Спробуйте ще раз)",
    "Дайте якесь завдання, а не пустий рядок!"
]

unknown = [
    "Я нічерта не зрозумєв, Гріша, давай по новой)",
    "Жодного тегу не розпізнано, напишіть правильний тег!",
    "Не розумію, що Ви хочете. Що це має значити?",
    "Це виходить за межі моїх можливостей наразі",
    "Не можу обробити цей запит. Спробуйте інше формулювання"
]

motivs = [
    "Через 20 років ви будете більше розчаровані тими речами, які ви не робили, ніж тими, які ви зробили.",
    "Щоб дійти до мети, людині потрібно тільки одне — йти.",
    "Якщо ти можеш про це мріяти, то ти можеш це зробити."
]

def random_joke():
    return random.choice(jokes)

def random_greating():
    return random.choice(greatings)

def random_empty():
    return random.choice(empty)

def random_unknown():
    return random.choice(unknown)

def random_motive():
    return random.choice(motivs)

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
    else:
        return None

def get_response(text):
    t = text.lower()
    tag = analyze_text(t)
    
    if tag is None:
        return f"{NAME}: {random_unknown()}"
    elif "empty" in tag:
        return f"{NAME}: {random_empty()}"
    elif "joke" in tag:
        return f"{NAME}: Ось Вам жарт - {random_joke()}"
    elif "money" in tag:
        return f"{NAME}: На вашій карті: {random.randint(0, 100000)}₴ гривень."
    elif "motivate" in tag:
        return f"{NAME}: Ось Вам порада - {random_motive()}"
    elif "time" in tag:
        return f"{NAME}: Зараз - {datetime.now().strftime('%H:%M')}"
    elif "exit" in tag:
        return "exit"
    return f"{NAME}: {random_unknown()}"

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
