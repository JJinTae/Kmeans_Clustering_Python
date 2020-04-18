import random as rnd
import numpy as np
import math
import matplotlib.pyplot as plt
import Demode as de
import Symbol as sym
import tensorflow as tf
import timeit

tf.debugging.set_log_device_placement(True)


QAM = 4
Count_Total = 1
symbol_num = 100000
SNR = 15
symbol = []
SER = np.zeros(SNR)

# Kmeans에 필요한 데이터
init_center_real = tf.dtypes.cast(tf.constant([[1], [-1], [-1], [1]]), tf.double)
init_center_imag = tf.dtypes.cast(tf.constant([[1], [1], [-1], [-1]]), tf.double)



temp_Y = [[0]*symbol_num for i in range(4)] # 임시 심볼 값을 담을 4xn 배열

# Matrix = [[0]*5 for i in range(7)]  열 행
# 인덱스로 접근해서 값 변경

for count in range(Count_Total):

    print(count)
    symbol = sym.Gensymbol(QAM, symbol_num)  # 초기 심볼
    data_s = de.Demode(QAM, symbol)  # 초기 심볼 위치 rsc err count

    for snr in range(SNR):

        symbol_y = sym.Addnoise(snr, symbol)  # 초기 심볼 + 노이즈
        # 초기화 부분
        position = np.zeros(symbol_num, int)  # 심볼의 사분면 위치를 담을 배열
        rsc_TakeCenter = [[0] * 4 for i in range(3)]


        # 계산을 위해 담음
        symbol_y = np.array(symbol_y) # real imag 배열을 나누기 위해 array로 담음
        # symbol_real = tf.constant(symbol_y.real)
        # symbol_imag = tf.constant(symbol_y.imag)
        start = timeit.default_timer()
        with tf.device('/GPU:0'):
            temp_real = tf.pow(tf.subtract(symbol_y.real, init_center_real), 2)
            temp_imag = tf.pow(tf.subtract(symbol_y.imag, init_center_imag), 2)
            dist_temp = tf.sqrt(tf.add(temp_real, temp_imag))

        dist = dist_temp.numpy()

        stop = timeit.default_timer()



        # 보기쉽게 Dist를 구하는 부분과 Dist중 최솟값을 구하는 부분을 나눔
        for i in range(symbol_num):
            temp = 0
            # mindist 부분 - 사분면을 구함
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
        temp_center_real = np.zeros(shape=(QAM, 1))
        temp_center_imag = np.zeros(shape=(QAM, 1))
        for v in range(4):
            if rsc_TakeCenter[2][v] != 0:
                temp_center_real[v][0] = rsc_TakeCenter[0][v] / rsc_TakeCenter[2][v]
                temp_center_imag[v][0] = rsc_TakeCenter[1][v] / rsc_TakeCenter[2][v]
        init_center_real = tf.dtypes.cast(tf.constant(temp_center_real), tf.double)
        init_center_imag = tf.dtypes.cast(tf.constant(temp_center_imag), tf.double)

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