import math

def Est_Ch(center, Hk):
    Com_center = []
    theta = []
    dist = []
    MSE = []

    tmp_com = [complex(1, 0), complex(-1, 0), complex(0, 1), complex(0, -1)]
    sqrt2 = complex(math.sqrt(2), 0)

    for i in range(4):
        Com_center.append(complex(center[i].real, center[i].imag))
        theta.append(math.atan2(Com_center[i].real, Com_center[i].imag))

    for i in range(4):
        for j in range(4):
            if theta[i] < theta[j]:
                theta_temp = theta[i]
                theta[i] = theta[j]
                theta[j] = theta_temp

                center_Temp = Com_center[i]
                Com_center[i] = Com_center[j]
                Com_center[j] = center_Temp

    C = (Com_center[1] + Com_center[2]) / sqrt2

    for i in range(4):
        MSE.append(C * tmp_com[i])
        dist.append(abs(pow(MSE[i] - Hk, 2)))

    Est_ch = MSE[dist.index(min(dist))]
    MSE_result = min(dist)

    return Est_ch, MSE_result


