from math import log, factorial
from lab2.lab2 import calculate_reliability


N = input("Input number of elements: ")
while not N.isnumeric():
    N = input("Incorrect value, try again:")
N = int(N)

while True:
    ps = input("Input probabilities: ").strip()
    try:
        ps = list(map(lambda x: float(x), ps.split(" ")))
        if len(ps) == N:
            break
        else:
            print("Incorrect number of probabilities!")
    except ValueError:
        print("Incorrect input")

T_in = input("Input time: ")
while not T_in.isnumeric():
    T_in = input("Incorrect value, try again:")
T_in = int(T_in)

K = input("Input K: ")
while not K.isnumeric():
    K = input("Incorrect value, try again:")
K = int(K)

P_sys = calculate_reliability(N, "data.txt", ps)

Q_sys = 1 - P_sys
T_sys = - T_in / log(P_sys)
print(f"Q_sys = {Q_sys}")
print(f"T_sys = {T_sys}")

# General reservation
Q_reserved1 = 1 / factorial(K + 1) * Q_sys
P_reserved1 = 1 - Q_reserved1
T_reserved1 = -T_in / log(P_reserved1)
print(f"P_res = {P_reserved1}")
print(f"Q_res = {Q_reserved1}")
print(f"T_res = {T_reserved1}")
G_p1 = P_reserved1 / P_sys
G_q1 = Q_reserved1 / Q_sys
G_t1 = T_reserved1 / T_sys
print(f"G_p1 = {G_p1}")
print(f"G_q1 = {G_q1}")
print(f"G_t1 = {G_t1}")

# Separate reservation
print("-" * 100)
new_ps = [1 - pow(1 - p, K + 1) for p in ps]
P_reserved2 = calculate_reliability(N, "data.txt", new_ps)
Q_reserved2 = 1 - P_reserved2
T_reserved2 = -T_in / log(P_reserved2)
print(f"P_res = {P_reserved2}")
print(f"Q_res = {Q_reserved2}")
print(f"T_res = {T_reserved2}")
G_p2 = P_reserved2 / P_sys
G_q2 = Q_reserved2 / Q_sys
G_t2 = T_reserved2 / T_sys
print(f"G_p2 = {G_p2}")
print(f"G_q2 = {G_q2}")
print(f"G_t2 = {G_t2}")
