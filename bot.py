import telebot
from config import TOKEN
from database import init_db, add_task, get_tasks, delete_task

bot = telebot.TeleBot(TOKEN)
init_db()

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Hi! Use /add, /list or /delete to manage your tasks.")

@bot.message_handler(commands=['add'])
def add(message):
    task_text = message.text[5:].strip()
    if task_text:
        add_task(message.chat.id, task_text)
        bot.send_message(message.chat.id, f"Task added: {task_text}")
    else:
        bot.send_message(message.chat.id, "Please provide a task after /add.")

@bot.message_handler(commands=['list'])
def list_tasks(message):
    tasks = get_tasks(message.chat.id)
    if tasks:
        msg = "\n".join([f"{i + 1}. {text}" for i, (tid, text) in enumerate(reversed(tasks))])
    else:
        msg = "No tasks yet."
    bot.send_message(message.chat.id, msg)

@bot.message_handler(commands=['delete'])
def delete(message):
    try:
        tasks = get_tasks(message.chat.id)
        tasks = list(reversed(tasks))
        index = int(message.text.split()[1]) - 1
        if 0 <= index < len(tasks):
            task_id = tasks[index][0]
            delete_task(message.chat.id, task_id)
            bot.send_message(message.chat.id, f"Task {index + 1} deleted.")
        else:
            bot.send_message(message.chat.id, "Invalid task number.")
    except (IndexError, ValueError):
        bot.send_message(message.chat.id, "Usage: /delete task_number")

bot.polling(none_stop=True)