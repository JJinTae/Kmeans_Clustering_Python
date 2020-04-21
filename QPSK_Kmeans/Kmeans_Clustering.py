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

            position = Min_dist(dist, symbol_num, qam)

            for i in range(symbol_num):
                # center점 수정
                temp_Y[position[i]][i] = symbol[i]  # 임시 temp_Y를 만들어주고
                for q in range(qam):
                    if position[i] == q:
                        rsc_TakeCenter[0][q] += symbol[i].real
                        rsc_TakeCenter[1][q] += symbol[i].imag
                        rsc_TakeCenter[2][q] += 1

            # 새로운 초기점 생성
            for v in range(qam):
                if rsc_TakeCenter[2][v] != 0:
                    init_center[v] = complex(rsc_TakeCenter[0][v] / rsc_TakeCenter[2][v],
                                             rsc_TakeCenter[1][v] / rsc_TakeCenter[2][v])

        return init_center, temp_Y


def Kmeans_16QAM(cluster, symbol, qam, hk):
    # symbol_num = len(symbol)
    # pre_center, temp_y = Kmeans(cluster, symbol, 4, hk)
    if qam == 16:
        pre_center, temp_y = Kmeans(cluster, symbol, 4, hk)
        center, temp_Y = Kmeans_QAM(cluster, symbol, qam, temp_y, pre_center)
        return center, temp_Y
    elif qam == 64:
        pre_center, temp_y = Kmeans_16QAM(cluster, symbol, 16, hk)
        center, temp_Y = Kmeans_QAM(cluster, symbol, qam, temp_y, pre_center)
        return center, temp_Y

        # init_center = Make_init_center(pre_center, qam)
        # for start in range(cluster):
        #     # Dist 부분
        #
        #     dist = [[0] * symbol_num for i in range(qam)]  # 거리를 담을 배열
        #     rsc_TakeCenter = [[0] * qam for i in range(3)]  # 중심점을 잡을 소스 배열
        #
        #     for startpos in range(qam // 4):
        #         pos = startpos * 4 # 0 4 8 12
        #         for i in range(4):
        #             pos_temp = pos + i # 0 1 2 3 / 4 5 6 7 / 8 9 10 11 / 12 13 14 15
        #             for j in range(symbol_num):
        #                 if temp_y[startpos][j].real != 0 and temp_y[startpos][j].imag != 0:
        #                     part_Real = math.pow(temp_y[startpos][j].real - init_center[pos_temp].real, 2)
        #                     part_Imag = math.pow(temp_y[startpos][j].imag - init_center[pos_temp].imag, 2)
        #                     dist[pos_temp][j] = math.sqrt(part_Real + part_Imag)
        #
        #     position = Min_dist(dist, symbol_num, qam)
        #
        #     temp_Y = [[0] * symbol_num for i in range(qam)]  # 임시 심볼 값을 담을 배열
        #     for i in range(symbol_num):
        #         # center점 수정
        #         temp_Y[position[i]][i] = symbol[i]  # 임시 temp_Y를 만들어주고
        #         for q in range(qam):
        #             if position[i] == q:
        #                 rsc_TakeCenter[0][q] += symbol[i].real
        #                 rsc_TakeCenter[1][q] += symbol[i].imag
        #                 rsc_TakeCenter[2][q] += 1
        #
        #     # 새로운 초기점 생성
        #     for v in range(qam):
        #         if rsc_TakeCenter[2][v] != 0:
        #             init_center[v] = complex(rsc_TakeCenter[0][v] / rsc_TakeCenter[2][v],
        #                                      rsc_TakeCenter[1][v] / rsc_TakeCenter[2][v])
        # return init_center, temp_Y

def Kmeans_QAM(cluster, symbol, qam, temp_y, pre_center):
    symbol_num = len(symbol)
    init_center = Make_init_center(pre_center, qam)
    for start in range(cluster):
        # Dist 부분

        dist = [[0] * symbol_num for i in range(qam)]  # 거리를 담을 배열
        rsc_TakeCenter = [[0] * qam for i in range(3)]  # 중심점을 잡을 소스 배열

        for startpos in range(qam // 4):
            pos = startpos * 4  # 0 4 8 12
            for i in range(4):
                pos_temp = pos + i  # 0 1 2 3 / 4 5 6 7 / 8 9 10 11 / 12 13 14 15
                for j in range(symbol_num):
                    if temp_y[startpos][j].real != 0 and temp_y[startpos][j].imag != 0:
                        part_Real = math.pow(temp_y[startpos][j].real - init_center[pos_temp].real, 2)
                        part_Imag = math.pow(temp_y[startpos][j].imag - init_center[pos_temp].imag, 2)
                        dist[pos_temp][j] = math.sqrt(part_Real + part_Imag)

        position = Min_dist(dist, symbol_num, qam)

        temp_Y = [[0] * symbol_num for i in range(qam)]  # 임시 심볼 값을 담을 배열
        for i in range(symbol_num):
            # center점 수정
            temp_Y[position[i]][i] = symbol[i]  # 임시 temp_Y를 만들어주고
            for q in range(qam):
                if position[i] == q:
                    rsc_TakeCenter[0][q] += symbol[i].real
                    rsc_TakeCenter[1][q] += symbol[i].imag
                    rsc_TakeCenter[2][q] += 1

        # 새로운 초기점 생성
        for v in range(qam):
            if rsc_TakeCenter[2][v] != 0:
                init_center[v] = complex(rsc_TakeCenter[0][v] / rsc_TakeCenter[2][v],
                                         rsc_TakeCenter[1][v] / rsc_TakeCenter[2][v])
    return init_center, temp_Y






def Ch_Est_Center(center, qam):
    hk_center = []
    for i in range(4): # 0 1 2 3
        startpos = i * (qam // 4) # 0 4 8 12
        sum_real = 0
        sum_imag = 0
        for j in range(qam // 4): # 0 1 2 3 = 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15
            sum_real += center[startpos+j].real
            sum_imag += center[startpos+j].imag
        sum_real /= (qam // 4)
        sum_imag /= (qam // 4)
        hk_center.append(complex(sum_real, sum_imag))
    return hk_center


def Make_init_center(center, qam):
    pi = [math.pi / 4, 3 * math.pi / 4, 5 * math.pi / 4, 7 * math.pi / 4]
    temp_i = qam // 4

    init_center = []

    for i in range(temp_i):
        startpos = i * 4
        for j in range(4):
            init_center.append(complex(math.cos(pi[j]) + center[i].real, math.sin(pi[j]) + center[i].imag))
    return init_center

def Min_dist(dist, ylength, qam):
    position = np.zeros(ylength, int)  # 심볼의 사분면 위치를 담을 배열

    if qam == 4:
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

    else:
        temp = 0
        temp_i = qam // 4
        for startpos in range(temp_i):
            for i in range(ylength):
                for j in range(4):
                    pos = startpos * 4 + j
                    if dist[pos][i] != 0:
                        if pos % 4 == 0:
                            temp = dist[pos][i]
                            position[i] = pos
                        elif temp > dist[pos][i]:
                            temp = dist[pos][i]
                            position[i] = pos
        return position

