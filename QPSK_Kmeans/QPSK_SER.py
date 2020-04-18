import random as rnd
import numpy as np
import math
import matplotlib.pyplot as plt
import Demode as de
import Symbol as sym
import timeit

# import tensorflow as tf
# real = tf.constant(2.25)
# imag = tf.constant(3.25)
# tf.dtypes.complex(real, imag)

QAM = 4
Count_Total = 1
symbol_num = 1000
SNR = 15
symbol = []
SER = np.zeros(SNR)

# Kmeans에 필요한 데이터
init_center = [complex(1, 1), complex(-1, 1), complex(-1, -1), complex(1, -1)]
dist = [[0]*symbol_num for i in range(4)] # 거리를 담을 4xn 배열
temp_Y = [[0]*symbol_num for i in range(4)] # 임시 심볼 값을 담을 4xn 배열

# Matrix = [[0]*5 for i in range(7)]  열 행
# 인덱스로 접근해서 값 변경

for count in range(Count_Total):

    symbol = sym.Gensymbol(QAM, symbol_num)  # 초기 심볼
    data_s = de.Demode(QAM, symbol)  # 초기 심볼 위치

    for snr in range(SNR):

        symbol_y = sym.Addnoise(snr, symbol)  # 초기 심볼 + 노이즈
        # 초기화 부분
        position = np.zeros(symbol_num, int)  # 심볼의 사분면 위치를 담을 배열
        rsc_TakeCenter = [[0] * 4 for i in range(3)]

        start = timeit.default_timer()
        # Dist 부분
        for i in range(symbol_num):

            # dist 거리 재기
            for j in range(4):
                part_Real = math.pow(symbol_y[i].real - init_center[j].real, 2)
                part_Imag = math.pow(symbol_y[i].imag - init_center[j].imag, 2)
                dist[j][i] = math.sqrt(part_Real + part_Imag)
        stop = timeit.default_timer()

        for i in range(symbol_num):
            # mindist 부분 - 사분면을 구함
            temp = 0
            for j in range(4):
                if j == 0:
                    temp = dist[j][i]
                elif temp > dist[j][i]:
                    temp = dist[j][i]
            for k in range(4):
                if dist[k][i] == temp:
                    position[i] = k
            # center점 수정
            temp_Y[position[i]][i] = symbol_y[i]  # 임시 temp_Y를 만들어주고

            for q in range(4):
                if position[i] == q:
                    rsc_TakeCenter[0][q] += symbol_y[i].real
                    rsc_TakeCenter[1][q] += symbol_y[i].imag
                    rsc_TakeCenter[2][q] += 1



        # 새로운 초기점 생성
        for v in range(4):
            if rsc_TakeCenter[2][v] != 0:
                init_center[v] = complex(rsc_TakeCenter[0][v] / rsc_TakeCenter[2][v],
                                         rsc_TakeCenter[1][v] / rsc_TakeCenter[2][v])

        data_y = de.Demode(QAM, symbol_y)

        SER[snr] += de.Equals(data_s, data_y)

for i in range(SNR):
    SER[i] = SER[i] / (symbol_num * Count_Total)
    print(i)
    print(SER[i])

# 초기점 찍는 기능
# for test in range(QAM):
#     plt.scatter(init_center[test].real, init_center[test].imag)
# 심볼점 찍는 기능
# for i in range(symbol_num):
#     plt.scatter(symbol[i].real, symbol[i].imag)
plt.xlim(-1.5, 1.5)
plt.ylim(-1.5, 1.5)
print(stop - start)

# SER Semilogy
# x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
# plt.semilogy(x, SER)
# plt.xlim([0, SNR])
# plt.ylim(pow(10,-5), pow(10,0))

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