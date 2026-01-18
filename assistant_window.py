import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk
import threading
from google import genai

client = genai.Client(api_key="AIzaSyAFvpqtSBbqYkq39-sFnAQA1VkrC5UgdjM")

FONT_MAIN = ("Segoe UI", 12)
FONT_BOLD = ("Segoe UI", 12, "bold")
COLOR_USER_TEXT = "#005c99"   
COLOR_AI_TEXT = "#2d2d2d"     
COLOR_BG_CHAT = "#ffffff"  
COLOR_ACCENT = "#4a90e2"  

def load_image(path):
    try:
        image = Image.open(path)
        image = image.resize((250, 180), Image.Resampling.LANCZOS)
        image = ImageTk.PhotoImage(image)
        return image
    except Exception as e:
        print(f"Error loading image {path}: {e}")
        return None

def display_text(sender, text):
    chat_display.configure(state='normal')
    
    chat_display.insert(tk.END, "\n")
    
    if sender == "You":
        chat_display.insert(tk.END, f"{text}\n", "user_msg")
    else:
        chat_display.insert(tk.END, f"{text}\n", "ai_msg")
        
    chat_display.insert(tk.END, "\n", "separator")
    chat_display.configure(state='disabled')
    chat_display.see(tk.END)

def detect_emotion(text):
    t = text.lower()
    if any(word in t for word in ["привіт", "добре", "гарно", "круто", "супер", "дякую"]):
        return "happy"
    if any(word in t for word in ["помилка", "погано", "жах", "не працює", "сумно", "біль"]):
        return "sad"
    return "neutral"
    
def set_state(emotion):
    if emotion not in emotions:
        return
        
    image, bg_color = emotions.get(emotion)
    
    root.configure(bg=bg_color)
    input_container.configure(bg=bg_color)
    avatar_label.configure(bg=bg_color)
    
    if image:
        avatar_label.configure(image=image)
        avatar_label.image = image

def start_chat_threading(event=None):
    user_text = user_input.get().strip()
    if not user_text: return
    
    send_button.configure(state="disabled", text="⏳", bg="#cccccc")
    user_input.delete(0, tk.END)
    
    display_text("You", user_text)
    
    threading.Thread(target=process_message, args=(user_text,)).start()

def process_message(user_text):
    init_emotion = detect_emotion(user_text)
    
    root.after(0, set_state, init_emotion)

    reply = ""
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_text,
        )
        reply = response.text
    except Exception as e:
        print(f"Error: {e}")
        reply = f"Вибачте, виникла технічна шоколадка: {e}"
        root.after(0, set_state, "sad")
        
    root.after(0, lambda: display_text("ShI", reply))
    root.after(0, lambda: send_button.configure(state="active", text="➤", bg=COLOR_ACCENT))

root = tk.Tk()
root.title("AI Companion")
root.geometry("500x850") 
root.resizable(True, True)

images = {
    "neutral": load_image("neutral.png"),
    "sad": load_image("sad.png"),
    "happy": load_image("happy.png"),
}

emotions = {
    "neutral": (images["neutral"], "#dbede6"),
    "sad": (images["sad"], "#8faabf"), 
    "happy": (images["happy"], "#a8e6cf"), 
}

avatar_label = tk.Label(root, bd=0)
avatar_label.pack(side=tk.TOP, pady=(30, 10))

chat_frame = tk.Frame(root, bg=COLOR_BG_CHAT)
chat_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=20, pady=10)

chat_display = tk.Text(
    chat_frame, 
    height=15, 
    width=50, 
    state="disabled", 
    wrap="word", 
    font=FONT_MAIN,
    bg=COLOR_BG_CHAT,
    bd=0,     
    padx=15,   
    pady=15,
    highlightthickness=0 
)
chat_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(chat_frame, command=chat_display.yview, bg=COLOR_BG_CHAT)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
chat_display.configure(yscrollcommand=scrollbar.set)

chat_display.tag_config("user_msg", foreground=COLOR_USER_TEXT, justify="right", rmargin=10)
chat_display.tag_config("ai_msg", foreground=COLOR_AI_TEXT, justify="left", lmargin1=0, lmargin2=0)
chat_display.tag_config("separator", font=("Arial", 4)) 

input_container = tk.Frame(root)
input_container.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=20)

input_inner_frame = tk.Frame(input_container, bg="white", padx=5, pady=5)
input_inner_frame.pack(fill=tk.X)

user_input = tk.Entry(
    input_inner_frame, 
    font=FONT_MAIN, 
    bd=0, 
    bg="white",
    highlightthickness=0
)
user_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=5)
user_input.bind("<Return>", start_chat_threading)

send_button = tk.Button(
    input_inner_frame, 
    text="➤", 
    command=start_chat_threading, 
    font=("Arial", 14), 
    bg=COLOR_ACCENT, 
    fg="white",
    activebackground="#357abd",
    activeforeground="white",
    bd=0,
    cursor="hand2",
    width=4
)
send_button.pack(side=tk.RIGHT, padx=5)

set_state("neutral")
display_text("ShI", "Кхендекох! Як твої справи сьогодні?")

root.mainloop()