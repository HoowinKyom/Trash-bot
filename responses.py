import random

def get_response(message: str) -> str:
    p_message = message.lower()

    if p_message == 'Bot':
        return 'Hey there! You called? 🤖 I\'m AssistifyBot, your virtual companion on this Discord adventure. Need assistance, have a question, or just looking for some fun commands? Type !help to discover all the cool things I can do! 🌟'

    if p_message == 'hello':
        return 'Hey there!'

    if 'bot' in p_message:
        return 'Hey there! You called? 🤖 I\'m AssistifyBot, your virtual companion on this Discord adventure. Need assistance, have a question, or just looking for some fun commands? Type !help to discover all the cool things I can do! 🌟'

    if p_message == '!help':
        return 'Sure thing! Please make sure to check out the #rules channel for important guidelines. Happy chatting! 📜'
    
    if p_message == 'nigga':
        return 'wash your mouth 🫣'
    
    if p_message == 'bitch':
        return "I'm here to assist and keep things friendly. Let's keep the conversation respectful, please."
    
    if p_message == '!vip':
        return 'https://www.roblox.com/games/12355337193?privateServerLinkCode=55769532370951510012163242173675'
    
    if p_message == 'Nigger' or p_message == 'nigger':
        return "I'm here to assist and keep things friendly. Let's keep the conversation respectful, please."

