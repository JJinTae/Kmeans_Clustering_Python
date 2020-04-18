import random as rnd
import numpy as np
import math


def Gensymbol(qam, symbol_num):
    point = [1, -1, 3, -3, 5, -5, 7, -7, 9, -9, 11, -11, 13, -13, 15, -15]
    ComArray = [] # 생성된 심볼을 담을 리스트

    if qam == 4:
        Mean = math.sqrt(2)
        for i in range(symbol_num):
            ComArray.append(complex(point[rnd.randrange(0,2)]/Mean, point[rnd.randrange(0,2)]/Mean))
    elif qam == 16:
        Mean = math.sqrt(10)
        for i in range(symbol_num):
            ComArray.append(complex(point[rnd.randrange(0,4)]/Mean, point[rnd.randrange(0,4)]/Mean))


    elif qam == 64:
        Mean = math.sqrt(42)
        for i in range(symbol_num):
            ComArray.append(complex(point[rnd.randrange(0, 8)] / Mean, point[rnd.randrange(0, 4)] / Mean))

    elif qam == 256:
        Mean = math.sqrt(340)
        for i in range(symbol_num):
            ComArray.append(complex(point[rnd.randrange(0, 16)] / Mean, point[rnd.randrange(0, 4)] / Mean))

    return ComArray


def Addnoise(snr, symbol):
    Mean = math.sqrt(2)
    db = math.pow(10, -snr / 20)
    ComArray = []

    for i in range(len(symbol)):
        re_noise = np.random.normal(0, 1) / Mean * db
        im_noise = np.random.normal(0, 1) / Mean * db
        ComArray.append(complex(symbol[i].real + re_noise, symbol[i].imag + im_noise))

    return ComArray

def Gen_ch():
    Mean = math.sqrt(2)
    CH_RE = np.random.normal(0, 1) / Mean
    CH_IM = np.random.normal(0, 1) / Mean

    return complex(CH_RE, CH_IM)

def MultyCh(symbol, ch):
    for i in range(len(symbol)):
        symbol[i] = symbol[i] * ch

    return symbol

def DividCh(symbol, ch):
    for i in range(len(symbol)):
        symbol[i] = symbol[i] / ch

    return symbol