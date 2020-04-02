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
        pass

    elif qam == 64:
        pass

    elif qam == 256:
        pass

    return data_sum


def Equals(data_s, data_y):
    err = 0
    for i in range(len(data_s)):
        if data_s[i].real != data_y[i].real or data_s[i].imag != data_y[i].imag:
           err += 1

    return err