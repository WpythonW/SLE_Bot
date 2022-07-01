import telebot
from operator import methodcaller
import numpy as np
import requests

bot = telebot.TeleBot('5422152712:AAH1TYNiyhwqTsZcQzndwGgw8RiFVjFDevc')
matrix = 0
vector = 0


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Введите матрицу в формате\n1 2 3\n4 5 6\n7 8 9\nили вектор свободных '
                                      'членов в формате\n1 2 3\nВводить можно только '
                                      'числа\n/restart - перезагрузка')
    bot.send_message(message.chat.id, 'Если хотите уточнить, что именно забиваете - пишите:\nmatrix\n1 2\n3 4 - для '
                                      'матрицы\nvector 1 2 - для векторов')


@bot.message_handler(commands=['restart'])
def restart(message):
    global matrix, vector
    matrix = 0
    vector = 0
    bot.send_message(message.chat.id, 'перезапустился')
    start(message)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global matrix, vector
    text = message.text
    if ("\n" not in message.text and "matrix" not in message.text) or "vector" in message.text:
        text = text.replace("vector ", "")
        try:
            vector = np.array(list(map(int, text.split())), float)
        except ValueError:
            bot.send_message(message.chat.id, 'Можно вводить только числа')
            return 0
        if type(matrix) == int:
            bot.send_message(message.chat.id, 'Теперь введите матрицу коэффициентов')
    else:
        text = text.replace("matrix\n", "")
        try:
            matrix = np.array(list(map(methodcaller("split", " "), text.split('\n'))), float)
        except ValueError:
            bot.send_message(message.chat.id, 'Можно вводить только числа')
            return 0
        if type(vector) == int:
            bot.send_message(message.chat.id, 'Теперь введите вектор свободных членов')
    if type(vector) != int and type(matrix) != int:
        print(matrix)
        print(vector)
        if len(matrix) != len(vector):
            bot.send_message(message.chat.id, 'Не совпадают размерности')
            matrix = 0
            vector = 0
            return 0
        answer = G(matrix, vector)
        if type(answer) == bool:
            bot.send_message(message.chat.id, 'Ведущие элементы не должны быть нулями')
            matrix = 0
            vector = 0
        else:
            response = ""
            for i, x in enumerate(answer):
                response += f"x{i} = {x}\n"
            bot.send_message(message.chat.id, response)
            bot.send_message(message.chat.id, "Далее можно без перезапуска забивать следующую матрицу")
            matrix = 0
            vector = 0


def G(M, V):
    n = len(V)
    X = np.zeros(n, float)

    for i in range(n):
        if M[i, i] == 0:
            return False
        if M[i, i] != 1:
            V[i] = V[i] / M[i, i]
            M[i, :] = M[i, :] / M[i, i]
        for j in range(i + 1, n):
            if M[j, i] != 0:
                V[j] = V[j] / M[j, i]
                M[j, :] = M[j, :] / M[j, i]
                V[j] = V[j] - V[i]
                M[j, :] = M[j, :] - M[i, :]

    print(M)
    print(V)
    #k = 0
    #X[-1] = V[-1]
    #X[-2] = V[-2] - M[-2, -1] * X[-1]
    #X[-3] = V[-3] - M[-3, -2] * X[-2] - M[-3, -1] * X[-1]
    X[n - 1] = V[n - 1] / M[n - 1, n - 1]
    for i in range(n - 2, -1, -1):
        sum_ax = 0

        for j in range(i + 1, n):
            sum_ax += M[i, j] * X[j]

        X[i] = (V[i] - sum_ax) / M[i, i]
    print(X)
    return X


try:
    bot.infinity_polling(none_stop=True, interval=0)
except requests.exceptions.ConnectionError as ex:
    print(ex)
    print("===========================")
    pass
