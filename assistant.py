import random
from datetime import datetime
import os
import json

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

def load_user():
    if os.path.exists("user.json"):
        try:
            with open("user.json", "r", encoding="utf-8") as f:
                text = f.read().strip()
                if not text:
                    return None
                data = json.loads(text)
                return data
        except Exception:
            return None
    else:
        return None

def save_user(user_data):
    with open("user.json", "w", encoding="utf-8") as f:
        json.dump(user_data, f, ensure_ascii=False, indent=2)

def get_user():
    user_data = load_user()
    if user_data and "name" in user_data:
        return user_data
    
    print(f"{NAME}: Як Вас звати?")
    while True:
        ask_user = input("ALEXEY: ").strip()
        if not ask_user:
            print(f"{NAME}: Настрочи нормально!")
        else:
            user_data = {"name": ask_user}
            save_user(user_data)
            return user_data

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

def add_note():
    print(f"{NAME}: Напишіть що треба зберегти і я збережу")
    text = input(f"ALEXEY: ")
    with open("notes.txt", "a", encoding="utf-8") as f:
        f.write(text + "\n")
    return f"{NAME}: Нотатку '{text[:30]}...' записано!"

def read_note():
    if not os.path.exists("notes.txt"):
        return f"{NAME}: У вас ще немає нотаток. Створіть першу!"
    
    try:
        with open("notes.txt", "r", encoding="utf-8") as f:
            notes = [line.strip() for line in f.readlines() if line.strip()]
        
        if not notes:
            return f"{NAME}: У вас немає нотаток."
        
        response = f"{NAME}: Ваші нотатки:\n"
        for i, note in enumerate(notes, 1):
            response += f"{i}) {note}\n"
        return response.strip()
    except Exception as e:
        return f"{NAME}: Помилка при читанні нотаток: {e}"

def delete_notes():
    try:
        with open("notes.txt", "w", encoding="utf-8") as f:
            f.write("")
        return f"{NAME}: Всі нотатки видалено!"
    except Exception as e:
        return f"{NAME}: Помилка при видаленні нотаток: {e}"

def show_profile(user_data):
    if not user_data:
        return f"{NAME}: Профіль не знайдено. Створіть новий профіль."
    
    response = f"{NAME}: Ваш профіль:\n"
    response += "=" * 30 + "\n"
    
    for key, value in user_data.items():
        if key == "facts" and isinstance(value, list):
            if value:
                response += f"Факти про вас ({len(value)}):\n"
                for i, fact in enumerate(value, 1):
                    response += f"  {i}. {fact}\n"
            else:
                response += "Факти про вас: ще не додано\n"
        else:
            response += f"{key.capitalize()}: {value}\n"
    
    response += "=" * 30
    return response

def add_fact_about_me(user_data):
    print(f"{NAME}: Напишіть факт про себе")
    fact = input(f"ALEXEY: ").strip()
    
    if not fact:
        return f"{NAME}: Факт не може бути порожнім, давайте напишіть хоча б пару букв!"
    
    if "facts" not in user_data:
        user_data["facts"] = []
    
    user_data["facts"].append(fact)
    save_user(user_data)
    
    return f"{NAME}: Факт '{fact[:50]}...' додано до вашого профілю!"

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
    
    t = text.lower()
    
    if "жарт" in t or "сміши" in t or "жартуй" in t:
        return "joke"
    elif "мотив" in t or "порада" in t or "мотивуй" in t:
        return "motivate"
    elif "гроші" in t or "грошей" in t or "баланс" in t:
        return "money"
    elif "збережи" in t or "запиши" in t or "запам'ятай" in t or "нотатк" in t:
        return "add_note"
    elif "прочитай нотатку" in t or "покажи нотатку" in t or "згадати нотатку" in t or "нотатку" == t:
        return "read_note"
    elif "видали нотатки" in t or "очисти нотатки" in t or "стер нотатки" in t:
        return "delete_notes"
    elif "профіль" in t or "інформація про мене" in t:
        return "profile"
    elif "додай факт про мене" in t or "запам'ятай факт" in t or "запиши факт" in t:
        return "add_fact"
    elif "час" in t or "котра година" in t:
        return "time"
    elif "бувай" in t or "до зустрічі" in t or "вихід" in t or "exit" in t:
        return "exit"
    else:
        return None

def get_response(text, user_data):
    t = text.lower()
    tag = analyze_text(t)
    
    if tag is None:
        return f"{NAME}: {random_unknown()}", user_data
    elif "empty" in tag:
        return f"{NAME}: {random_empty()}", user_data
    elif "joke" in tag:
        return f"{NAME}: Ось Вам жарт - {random_joke()}", user_data
    elif "money" in tag:
        return f"{NAME}: На вашій карті: {random.randint(0, 100000)}₴ гривень.", user_data
    elif "motivate" in tag:
        return f"{NAME}: Ось Вам порада - {random_motive()}", user_data
    elif "time" in tag:
        return f"{NAME}: Зараз - {datetime.now().strftime('%H:%M')}", user_data
    elif "add_note" in tag:
        return add_note(), user_data
    elif "read_note" in tag:
        return read_note(), user_data
    elif "delete_notes" in tag:
        return delete_notes(), user_data
    elif "profile" in tag:
        return show_profile(user_data), user_data
    elif "add_fact" in tag:
        response = add_fact_about_me(user_data)
        return response, user_data
    elif "exit" in tag:
        return "exit", user_data
    
    return f"{NAME}: {random_unknown()}", user_data

def main():
    print(PERSONALITY)
    user_data = get_user()
    print(f"{NAME}: {user_data['name']}, {random_greating()}")
    
    while True:
        user_input = input(f"ALEXEY: ").strip()
        response, updated_user_data = get_response(user_input, user_data)
        user_data = updated_user_data
        
        if response == "exit":
            print(f"{NAME}: Бувайте. Чекаю на Вас! :)")
            break
        print(response)

if __name__ == "__main__":
    main()
