import random as rnd
import numpy as np
import math
import matplotlib.pyplot as plt
import os

temp = [1,-1]
QAM = 4
count_Cluster = 10
symbol_num = 1000
SNR = 5
symbol = []


Mean = math.sqrt(2)
db = math.pow(10, -SNR / 20)

# Kmeans에 필요한 데이터
init_center = [complex(1, 1), complex(-1, 1), complex(-1, -1), complex(1, -1)]
dist = [[0]*symbol_num for i in range(4)] # 거리를 담을 4xn 배열
temp_Y = [[0]*symbol_num for i in range(4)] # 임시 심볼 값을 담을 4xn 배열



# Matrix = [[0]*5 for i in range(7)]  열 행
# 인덱스로 접근해서 값 변경


for count in range(symbol_num) :
    Re = temp[rnd.randrange(0,2)] / Mean
    Im = temp[rnd.randrange(0,2)] / Mean

    noise_Re = np.random.normal(0,1) / Mean * db
    noise_Im = np.random.normal(0,1) / Mean * db

    Re = Re + noise_Re
    Im = Im + noise_Im

    # plt에 심볼값을 넣어준다.
    # plt.scatter(Re,Im)

    # 완성된 심볼을 복소수 배열에 담는다.
    symbol.append(complex(Re, Im))

    # print(symbol[count])


for count in range(count_Cluster):
    # 초기화 부분
    position = np.zeros(symbol_num, int)  # 심볼의 사분면 위치를 담을 배열
    count = [[0] * 4 for i in range(3)]

    # Dist 부분
    for i in range(symbol_num):
        temp = 0

        # dist 거리 재기
        for j in range(4):
            part_Real = math.pow(symbol[i].real - init_center[j].real, 2)
            part_Imag = math.pow(symbol[i].imag - init_center[j].imag, 2)
            dist[j][i] = math.sqrt(part_Real + part_Imag)

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
        temp_Y[position[i]][i] = symbol[k]  # 임시 temp_Y를 만들어주고

        for q in range(4):
            if position[i] == q:
                count[0][q] += symbol[i].real
                count[1][q] += symbol[i].imag
                count[2][q] += count[2][q] + 1


    # 새로운 초기점 생성
    for i in range(symbol_num):
        for v in range(4):
            if count[2][v] != 0:
                init_center[v] = complex(count[0][v] / count[2][v], count[1][v] / count[2][v])

for test in range(4):
    plt.scatter(init_center[test].real, init_center[test].imag)
















plt.grid()
plt.xlim(-1.5, 1.5)
plt.ylim(-1.5, 1.5)
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