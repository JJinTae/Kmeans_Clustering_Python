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

QAM = 4
Count_Total = 100
Cluster = 10
symbol_num = 1000
SNR = 15
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
    sym.MultyCh(symbol, ch) # 채널 입력

    for snr in range(SNR):

        symbol_y = sym.Addnoise(snr, symbol)  # 초기 심볼 + 노이즈
        # 초기화 부분

        if QAM == 4:
            center, temp_Y = kc.Kmeans(Cluster, symbol, QAM, ch)
            est_ch, mse = est.Est_Ch(center, ch)

        symbol_r = sym.DividCh(symbol_y, est_ch)

        data_r = de.Demode(QAM, symbol_r)
        SER[snr] += de.Equals(data_s, data_r)
        MSE[snr] += mse


for i in range(SNR):
    SER[i] = SER[i] / (symbol_num * Count_Total)
    MSE[i] = MSE[i] / Count_Total
    print(i)
    print(SER[i])

# 초기점 찍는 기능
# for test in range(QAM):
#     plt.scatter(init_center[test].real, init_center[test].imag)
# 심볼점 찍는 기능
# for i in range(symbol_num):
#      plt.scatter(testsymbol[i].real, testsymbol[i].imag)
# plt.xlim(-1.5, 1.5)
# plt.ylim(-1.5, 1.5)

# SER Semilogy
x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
plt.semilogy(x, SER)
plt.xlim([0, SNR])
plt.ylim(pow(10,-5), pow(10,0))

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