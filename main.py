
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler, ConversationHandler
from config import TOKEN
import controller

bot = Bot(token=TOKEN)
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher


def start(update, context):
    context.bot.send_message(update.effective_chat.id, "Запущен калькулятор. Если хотите завершить его работу, введите /finish")
    global step
    step = 0 
    return input_first_number(update, context)

def input_first_number(update, context):
    context.bot.send_message(update.effective_chat.id, "Какие числа хотите использовать? Если рациональные, введите 1. Если комплексные, введите 2.")



def take_user_input(update,context):
    global step, number_1, number_2, operation, number_type
    if step == 0:
        try:
            number_type = int(update.message.text)
            if number_type == 1:
                context.bot.send_message(update.effective_chat.id, "Введите первое число")
                step +=1
            elif number_type == 2:
                context.bot.send_message(update.effective_chat.id, "Введите первое число, формат ввода a+bj")
                step +=1
            else:        
                context.bot.send_message(update.effective_chat.id, "Вы ввели неправильное число, попробуйте еще раз")
                step = 0
        except:
            context.bot.send_message(update.effective_chat.id, "Вы ввели не число. Попробуйте еще раз")
            step = 0
    elif step == 1:
        try:
            if number_type == 1:
                number_1 = float(update.message.text)
                context.bot.send_message(update.effective_chat.id, "Введите второе число")
            elif number_type == 2:
                number_1 = complex(update.message.text)
                context.bot.send_message(update.effective_chat.id, "Введите второе число, формат ввода a+bj")
            step +=1
        except:
            context.bot.send_message(update.effective_chat.id, "Вы ввели не число. Попробуйте еще раз.")
            step = 1
    elif step == 2:
        try:
            if number_type == 1:
                number_2 = float(update.message.text)
            elif number_type == 2:
                number_2 = complex(update.message.text)
            step +=1
            context.bot.send_message(update.effective_chat.id, "Введите знак операции: +, -, *, /")
        except:
            context.bot.send_message(update.effective_chat.id, "Вы ввели не число. Попробуйте еще раз.")
            step = 2
    elif step == 3:
            operation = update.message.text
            if operation == '+' or operation == '-' or operation == '*' or operation == '/':
                result = controller.run(operation, number_1, number_2)
                context.bot.send_message(update.effective_chat.id, f'{number_1} {operation} {number_2} = {result}')
                step = 0
            else:
                context.bot.send_message(update.effective_chat.id, "Вы ввели неверный знак. Попробуйте еще раз.")
                step = 3


def finish(update, context):
    context.bot.send_message(update.effective_chat.id, "Вы завершили работу калькулятора")
    step = 0
    

def unknown(update, context):
    context.bot.send_message(update.effective_chat.id, f'Шо сказал, не пойму')
    


start_handler = CommandHandler('start', start)
finish_handler = CommandHandler('finish', finish)
message_handler = MessageHandler(Filters.text, take_user_input)



dispatcher.add_handler(start_handler)
dispatcher.add_handler(finish_handler)
dispatcher.add_handler(message_handler)


print('server started')
updater.start_polling()
updater.idle()




