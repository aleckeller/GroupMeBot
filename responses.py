import bot

def say_hi_to_sender():
    sender = bot.get_sender_name()
    message = ""
    if sender:
        message = "hi " + sender
    else:
        message = "hi"
    return message