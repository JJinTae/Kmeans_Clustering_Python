import math

def Demode(qam ,Symbol):
    data_sum = []
    if qam == 4:
        for i in range(len(Symbol)):
            if Symbol[i].real <= 0:
                data_real = -1
            else:
                data_real = 1

            if Symbol[i].imag <= 0:
                data_imag = -1
            else:
                data_imag = 1

            data_sum.append(complex(data_real, data_imag))

    elif qam == 16:
        Mean = math.sqrt(10)
        for i in range(len(Symbol)):
            if Symbol[i].real < -2 / Mean:
                data_real = -3
            elif Symbol[i].real > 2 / Mean:
                data_real = 3
            elif Symbol[i].real > -2 / Mean and Symbol[i].real <= 0:
                data_real = -1
            elif Symbol[i].real > 0 and Symbol[i].real <= 2 / Mean:
                data_real = 1

            if Symbol[i].imag < -2 / Mean:
                data_imag = -3
            elif Symbol[i].imag > 2 / Mean:
                data_imag = 3
            elif Symbol[i].imag > -2 / Mean and Symbol[i].imag <= 0:
                data_imag = -1
            elif Symbol[i].imag > 0 and Symbol[i].imag <= 2 / Mean:
                data_imag = 1

            data_sum.append(complex(data_real, data_imag))

    elif qam == 64:
        Mean = math.sqrt(42)
        for i in range(len(Symbol)):
            if Symbol[i].real > 0 and Symbol[i].real <= 2 / Mean:
                data_real = 1
            elif Symbol[i].real > 2 / Mean and Symbol[i].real <= 4 / Mean:
                data_real = 3
            elif Symbol[i].real > 4 / Mean and Symbol[i].real <= 6 / Mean:
                data_real = 5
            elif Symbol[i].real > 6:
                data_real = 7

            if Symbol[i].real <= -6 / Mean:
                data_real = -7
            elif Symbol[i].real <= -4 / Mean and Symbol[i].real > -6 / Mean:
                data_real = -5
            elif Symbol[i].real <= -2 / Mean and Symbol[i].real > -4 / Mean:
                data_real = -3
            elif Symbol[i].real <= 0 and Symbol[i].real > -2 / Mean:
                data_real = -1

            if Symbol[i].imag > 0 and Symbol[i].imag <= 2 / Mean:
                data_imag = 1
            elif Symbol[i].imag > 2 / Mean and Symbol[i].imag <= 4 / Mean:
                data_imag = 3
            elif Symbol[i].imag > 4 / Mean and Symbol[i].imag <= 6 / Mean:
                data_imag = 5
            elif Symbol[i].imag > 6:
                data_imag = 7

            if Symbol[i].imag <= -6 / Mean:
                data_imag = -7
            elif Symbol[i].imag <= -4 / Mean and Symbol[i].imag > -6 / Mean:
                data_imag = -5
            elif Symbol[i].imag <= -2 / Mean and Symbol[i].imag > -4 / Mean:
                data_imag = -3
            elif Symbol[i].imag <= 0 and Symbol[i].imag > -2 / Mean:
                data_imag = -1

            data_sum.append(complex(data_real, data_imag))


    elif qam == 256:
        Mean = math.sqrt(340)
        pass

    return data_sum


def Equals(data_s, data_y):
    err = 0
    for i in range(len(data_s)):
        if data_s[i].real != data_y[i].real or data_s[i].imag != data_y[i].imag:
           err += 1

    return err