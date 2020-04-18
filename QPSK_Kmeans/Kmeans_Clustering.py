import numpy as np
import math


def Kmeans(cluster, symbol, qam, hk):
    if qam == 4:
        symbol_num = len(symbol)
        init_center = [complex(1, 1) * hk, complex(-1, 1) * hk, complex(-1, -1) * hk, complex(1, -1) * hk]

        #Clustering
        for start in range(cluster):
            # Dist 부분
            temp_Y = [[0] * symbol_num for i in range(4)]  # 임시 심볼 값을 담을 4xn 배열
            dist = [[0] * symbol_num for i in range(4)]  # 거리를 담을 4xn 배열
            rsc_TakeCenter = [[0] * 4 for i in range(3)]  # 중심점을 잡을 소스 배열

            for i in range(symbol_num):
                # dist 거리 재기
                for j in range(4):
                    part_Real = math.pow(symbol[i].real - init_center[j].real, 2)
                    part_Imag = math.pow(symbol[i].imag - init_center[j].imag, 2)
                    dist[j][i] = math.sqrt(part_Real + part_Imag)

            position = QPSK_position(dist, symbol_num)

            for i in range(symbol_num):
                # center점 수정
                temp_Y[position[i]][i] = symbol[i]  # 임시 temp_Y를 만들어주고
                for q in range(4):
                    if position[i] == q:
                        rsc_TakeCenter[0][q] += symbol[i].real
                        rsc_TakeCenter[1][q] += symbol[i].imag
                        rsc_TakeCenter[2][q] += 1

            # 새로운 초기점 생성
            for v in range(4):
                if rsc_TakeCenter[2][v] != 0:
                    init_center[v] = complex(rsc_TakeCenter[0][v] / rsc_TakeCenter[2][v],
                                             rsc_TakeCenter[1][v] / rsc_TakeCenter[2][v])
        return init_center, temp_Y





def QPSK_position(dist, ylength):
    position = np.zeros(ylength, int)  # 심볼의 사분면 위치를 담을 배열

    # mindist 부분 - 사분면을 구함
    temp = 0
    for i in range(ylength):
        for j in range(4):
            if j == 0:
                temp = dist[j][i]
            elif temp > dist[j][i]:
                temp = dist[j][i]
        for k in range(4):
            if dist[k][i] == temp:
                position[i] = k
    return position