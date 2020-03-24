import random as rnd
import numpy as np
import math
import matplotlib.pyplot as plt

temp = [1,-1]
symbol_num = 1000
SNR = 5
symbol = []

Mean = math.sqrt(2)
db = math.pow(10, -SNR / 20)


for count in range(symbol_num) :
    Re = temp[rnd.randrange(0,2)] / Mean
    Im = temp[rnd.randrange(0,2)] / Mean

    noise_Re = np.random.normal(0,1) / Mean * db
    noise_Im = np.random.normal(0,1) / Mean * db

    Re = Re + noise_Re
    Im = Im + noise_Im

    plt.scatter(Re,Im)

    # 완성된 심볼을 복소수 배열에 담는다.
    symbol.append(complex(Re, Im))

    # print(symbol[count])
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