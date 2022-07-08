from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import aiogram.utils.markdown as fmt
import math
import traceback

from config import TOKEN                                                #импортируем токен бота из другого файла


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])                                 #ответ на start
async def send_welcome(message: types.Message):
    await message.reply("Привет!\nВведите квадратное уравнение!")
 
 
@dp.message_handler(commands=['help'])                                  #ответ на help
async def send_welcome(message: types.Message):
    await message.reply("Введите квадратное уравнение.\nПример правильно введенного уравнения:\na*x^2+x/b=c")


def adekvat(a):                                                         #функция для проверки наличия лишних знаков
    b = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '^', '*', '=', '/', 'x', '+', '-']
    p = 'я не понимаю Вас'
    q = 0
    for i in range(len(a)):
        if a[i] not in b:
            q += 1
    if q != 0:
        return p
    else:
        return ''


 
def scet1(a, b):                                                        #вычисляем первый коэффициент
    i = b
    k = ''
    p = ''
    if a[b] != 'x':                                                     #смотрим есть ли коэффициент перед x
        if a[b] == '-' and a[b + 1] == 'x':                             #если он -1
            k += '-1'
        else:
            while a[i] != '*':                                          #если он любой другой
                if a[i] == 'x':
                    break
                k += a[i]
                i += 1
    if len(a) > b+3:
        if (a[b + 3] == '/'):                                           #смотрим есть ли положительная дробная часть
            i = b + 3
            k += '1'
            while a[i] != '+':                                          #если есть, то заносим в k
                if a[i] == '-':
                    break
                k += a[i]
                i += 1 
            while a[i] != '-':
                if a[i] == '+':
                    break
                k += a[i]
                i += 1 
    if len(a) > b+4:  
        if (a[b + 4] == '/'):                                           #смотрим есть ли отрицательная дробная часть
            i = b + 4
            while a[i] != '+':                                          #если есть, то заносим в k
                if a[i] == '-':
                    break
                k += a[i]
                i += 1 
            while a[i] != '-':
                if a[i] == '+':
                    break
                k += a[i]
                i += 1 
    if len(a) > b + 3: 
        if (a[b + 3] != '/') and (a[b + 1] == '^'):                     #если ничего из вышесказанного нет, то записываем в k единицу
            k = '1'
    return k

def scet2(a, b):                                                        #находим 2 коэффициент
    i = b-1
    k = ''
    p = ''
    if a[b-1] != '+':                                                   #смотрим есть ли коэффициент перед x
        if a[b] == 'x' and a[b+1] != '/':                               #если он -1
            k += '-1'
        elif a[b+1] == '/':                                             #проверяем отрицательную дробь
            i = b + 2
            k += '-1/'
            while a[i] != '=':
                k += a[i]
                i += 1
        else:                                                           #проверяем отрицательное умножение
            while a[i] != '*':                                          
                k += a[i]
                i += 1
    else:                                                               #если коэффициент положительный
        if a[b] == 'x' and a[b+1] != '/':                               #если он 1
            k += '1'
        elif a[b+1] == '/':                                             #если он дробный
            i = b + 2
            k += '1/'
            while a[i] != '=':
                k += a[i]
                i += 1
        else:                                                           #если он положительное умножение
            while a[i] != '*':                                          
                k += a[i]
                i += 1
    return k


def coef1(a):                                                           #находим коэффициент при x^2
    k1 = ''
    k1 = scet1(a, 0)

    return k1


def coef2(a):                                                           #вычисляем сдвиг, взависимости от первого коэффициента
    i = 0
    q = 0
    k1 = coef1(a)
    k2 = ''
    if k1 == '-1':
        k2 = scet2(a, 5)
    elif k1 == '1':
        k2 = scet2(a, 4)
    elif '/' in k1:
        if '-' in k1:
            k2 = scet2(a, len(k1) + 3)
        else:
            k2 = scet2(a, len(k1) + 3)
    else:
        if '-' in k1:
            k2 = scet2(a, len(k1) + 5)
        else:
            k2 = scet2(a, len(k1) + 5)

    return k2

def coef3(a):                                                       #находим свободный член
    i = 0
    p = ''
    k3 = ''
    while a[i] != '=':
        i += 1
    i += 1
    for j in range(i, len(a)):
        k3 += a[j]

    return k3

def fl(k):                                                          #функция для перевода десятичной дроби в число float
    p = ''
    if '/' in k:
        if '-' in p:    
            p += k[3:]
            p = float(p)
            p = 1/p
        else:
            p += k[3:]
            p = float(p)
            p = -1/p
    else:
        p = float(k)
    
    return p

def perev(k):                                                       #функция для смены знака свободному члену
    if k > 0:
        k = 0 - k
    else:
        k = 0 - k

    return k

def resh(a, b, c):                                                  #фукнция для решения квадратного уравнения
    p = ''
    discr = b ** 2 - 4 * a * c
    if discr > 0:
        x1 = (-b + math.sqrt(discr)) / (2 * a)
        x2 = (-b - math.sqrt(discr)) / (2 * a)
        x1 = str(x1)                                                #для вывода необходимо перевести в строку
        x2 = str(x2)
        p += x1
        p += "  "
        p += x2                                        
    elif discr == 0:
        x = -b / (2 * a)
        x = str(x)
        p += x
    else:
        x1 = (-b + discr ** 0.5) / (2 * a)
        x2 = (-b - discr ** 0.5) / (2 * a)
        x1 = str(x1)                                                #для вывода необходимо перевести в строку
        x2 = str(x2)
        p += x1
        p += "\n"
        p += x2  

    return p

def colvX(a):                                                       #счетчик количества х в уравнении
    q = 0
    for i in range(len(a)):
        if a[i] == 'x':
            q += 1
    return q


@dp.message_handler()                                               #функция для выполнения финальных действий и вывода результата
async def quadro(message: str(types.Message)):
    pol1 = str(message.text)
    p = adekvat(pol1)                                               #проверяем что нет посторонних символов
    try:
        if p == '':                                                 #если их нет:
            if colvX(pol1) == 2:                                    #если в уравнении 2 х
                a = fl(coef1(pol1))
                b = fl(coef2(pol1))
                c = perev(fl(coef3(pol1)))
                await message.answer(resh(a, b, c))
            elif colvX(pol1) == 1:                                  #если один
                a = fl(coef1(pol1))
                b = 0
                c = perev(fl(coef3(pol1)))
                await message.answer(resh(a, b, c))
            else:                                                   #если их нет
                await message.answer('Это не квадратное уравнение(((')
        else:                                                       #вывод сообщения что лишние символы
            await message.answer(p)
    except Exception:
        await message.answer('Возникла ошибка!\nОбратитесь к нам, и мы постараемся ее исправить)')  #сообщение об ошибке
    #await message.answer(a)
    #await message.answer(b)
    #await message.answer(c)
 
if __name__ == '__main__':                                          #функция для постоянной проверки новых сообщений от пользователя
    executor.start_polling(dp, skip_updates=True)