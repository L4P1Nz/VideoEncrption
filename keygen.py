import numpy as np
import struct

def get_bytes_from_float(number):
    data = struct.pack('d', number)
    return data

# Model 1:
def henon_chaotic_map_1(a, b, Xo, Yo, iterations):
    X = np.zeros(iterations+1)
    Y = np.zeros(iterations+1)

    X[0] = Xo
    Y[0] = Yo

    for i in range(iterations):
        X[i+1] = 1 + b*Y[i] - a * X[i]**2
        Y[i+1] = X[i]

    return (X, Y)

# Model 2:
def henon_chaotic_map_2(a, b, Xo, Yo, iterations):
    X = np.zeros(iterations+1)
    Y = np.zeros(iterations+1)

    X[0] = Xo
    Y[0] = Yo

    key = [None] * iterations
    key1 = [None] * iterations
    key2 = [None] * iterations
    for i in range(iterations):
        X[i+1] = 1 + Y[i] - a * X[i]**2
        Y[i+1] = b * X[i]

        key[i] = select1(X[i], Y[i], X[i+1], Y[i+1])
        key1[i] = select2(key[i])
        key2[i] = integrate(key[i], key1[i])

    return key2

def select1(Xi, Yi, Xi1, Yi1):
    return get_bytes_from_float(Xi) + get_bytes_from_float(Yi) + get_bytes_from_float(Xi1) + get_bytes_from_float(Yi1)

def select2(key):
    return key[:16]

def integrate(key, key1):
    return key + key1


# keys = henon_chaotic_map_2(a2, b2, Xo2, Yo2, M)
# print(keys)