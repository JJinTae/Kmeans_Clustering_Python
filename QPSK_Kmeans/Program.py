import random as rnd
import numpy as np
import math
import matplotlib.pyplot as plt
import Demode as de
import Symbol as sym
import Kmeans_Clustering as kc
import Ch_Est as est
import timeit

# import tensorflow as tf
# real = tf.constant(2.25)
# imag = tf.constant(3.25)
# tf.dtypes.complex(real, imag)

QAM = 64
Count_Total = 5
Cluster = 10
symbol_num = 3000
SNR = 20
symbol = []
SER = np.zeros(SNR)
MSE = np.zeros(SNR)

# Kmeans에 필요한 데이터
dist = [[0]*symbol_num for i in range(4)] # 거리를 담을 4xn 배열

# Matrix = [[0]*5 for i in range(7)]  열 행
# 인덱스로 접근해서 값 변경

for count in range(Count_Total):
    print(count)

    symbol = sym.Gensymbol(QAM, symbol_num)  # 초기 심볼 생성
    data_s = de.Demode(QAM, symbol)  # 초기 심볼 위치
    ch = sym.Gen_ch() # 채널 생성
    symbol = sym.MultyCh(symbol, ch) # 채널 입력

    for snr in range(SNR):
        if QAM == 4 or QAM == 16:
            tap = snr
        else:
            tab = snr * 2

        symbol_y = sym.Addnoise(tab, symbol)  # 초기 심볼 + 노이즈
        # 초기화 부분

        if QAM == 4:
            center, temp_Y = kc.Kmeans(Cluster, symbol_y, QAM, ch)
            est_ch, mse = est.Est_Ch(center, ch)
        else:
            center, temp_Y = kc.Kmeans_16QAM(Cluster, symbol_y, QAM, ch)
            hk_center = kc.Ch_Est_Center(center, QAM)
            est_ch, mse = est.Est_Ch(hk_center, ch)
        # print(snr)
        # print(ch)
        # print(est_ch)
        # print("------")
        symbol_r = sym.DividCh(symbol_y, est_ch)

        data_r = de.Demode(QAM, symbol_r)
        SER[snr] += de.Equals(data_s, data_r)
        MSE[snr] += mse


for i in range(SNR):
    SER[i] = SER[i] / (symbol_num * Count_Total)
    MSE[i] = MSE[i] / Count_Total
    print(i)
    print(SER[i])


# 심볼점 찍는 기능
# Temp_Y
# for j in range(QAM):
#     for i in range(symbol_num):
#         print(plt.scatter(temp_Y[j][i].real, temp_Y[j][i].imag))
# Symbol
# for i in range(symbol_num):
#     plt.scatter(symbol_r[i].real, symbol_r[i].imag, color = 'r')
#     plt.scatter(symbol_y[i].real, symbol_y[i].imag, color = 'b')
#
# 초기점 찍는 기능
# for test in range(QAM):
#     plt.scatter(center[test].real, center[test].imag, color = '0.25')
#
# plt.xlim(-3.0, 3.0)
# plt.ylim(-3.0, 3.0)

# SER Semilogy
if QAM == 4 or QAM == 16:
    x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
else:
    x = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38]


plt.semilogy(x, SER)
plt.xlim([0, 40])
plt.ylim(pow(10,-2), pow(10,0))

plt.grid()
plt.show()

# 랜덤값
# 0부터 1까지 랜덤값을 반환
# print(rnd.randrange(0,2))

# 정규 분포
# 평균이 0 표준편차가 1인 정규분포 pure.shape만큼 생성
# pure = np.linspace(-1, 1, 100)
# noise = np.random.normal(0,1,pure.shape)
# 정규 분포 평균이 0 표준편차가 1 랜덤 발생
# print(random.gauss(0.0, 1.0))