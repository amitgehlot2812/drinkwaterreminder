from notifypy import Notify
import time
import schedule
import pyttsx3
import random

def initialize_tts_engine():
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate - 80)
    return engine

engine = initialize_tts_engine()

notification = Notify(
    default_notification_application_name="Drink Water Reminder",
    default_notification_title="Have a Glass of Water",
    default_notification_icon="clock.gif"
)

def greetings(context="general"):
    timestamp = time.strftime('%H:%M:%S')
    print(f"Current time is: {timestamp}")
    
    if context == "general" and '06:00:00' <= timestamp < '10:09:00':
        print("Good Morning Sir!")
        engine.say("Good Morning Sir!")
    elif context == "break":
        print("Enjoy your break time")
        engine.say("Enjoy your break time")
    elif context == "lunch":
        print("It's your lunch time, go have healthy food.")
        engine.say("Its your lunch time, go have healthy food.")
    elif context == "tea":
        print("Take tea break, eat healthy and stay hydrated.")
        engine.say("Take tea break, eat healthy and stay hydrated.")
    
    engine.runAndWait()

# Trigger greetings at startup if within morning window
current_time = time.strftime('%H:%M:%S')
if '06:00:00' <= current_time < '10:09:00':
    greetings("general")

# Water tracking and quotes
duplicate = set()
water_store = []

def drink_water():
    now = time.strftime('%H:%M:%S')
    if '13:10:00' <= now < '15:00:00':
        print("Skipping reminder during digestion time.")
        return

    try:
        with open("inspirationalv2.txt", "r", encoding="utf-8") as file:
            content = file.readlines()
    except FileNotFoundError:
        print("Error: The file 'inspirationalv2.txt' was not found.")
        return
    
    # Reset if all quotes used
    if len(duplicate) == len(content):
        print("All quotes used. Resetting duplicate list.")
        duplicate.clear()

    random.shuffle(content)

    for quote in content:
        quote = quote.strip()
        if quote not in duplicate:
            duplicate.add(quote)
            notification.message = quote
            notification.send(block=False)
            engine.say(quote)
            engine.runAndWait()

            try:
                water_amount = int(input("How much water did you drink (ml)? "))
                water_store.append(water_amount)
            except ValueError:
                print("Invalid input. Water not recorded.")
            break
    else:
        print("All quotes used. Resetting.")
        duplicate.clear()

def day_summary():
    total_water = sum(water_store)
    print(f"Today's total water intake: {total_water} ml")
    engine.say(f"Today's total water intake is {total_water} milliliters.")
    engine.runAndWait()
    
    with open("water_log.txt", "a") as f:
        f.write(f"{time.strftime('%Y-%m-%d')} - Total: {total_water} ml\n")

# Scheduling
schedule.every().day.at("10:10").do(greetings, context="break")
schedule.every().day.at("13:10").do(greetings, context="lunch")
schedule.every().day.at("15:25").do(greetings, context="tea")

schedule.every(45).minutes.do(drink_water)  # Change from 10s to realistic reminder interval
schedule.every().day.at("18:00").do(day_summary)

while True:
    schedule.run_pending()
    time.sleep(1)