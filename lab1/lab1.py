import subprocess
import sys


def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


if __name__ == '__main__':
    install("numpy")
    import numpy as np
    with open("data.txt", "r") as data:
        series = data.read()
    series = series.replace("\n", " ")
    series = np.fromstring(series, dtype=int, sep=",")
    gamma = float(input("Параметр гамма: "))
    n = int(input("Кількість інтервалів: "))
    T1 = int(input("Час на визначення ймовірності: "))
    T2 = int(input("Час на визначення інтенсивності: "))
    T_avg = series.mean()
    delimiter = series.max() / n
    density = [len(np.where(np.logical_and(series > delimiter * i, series < delimiter * (i+1)))[0])
               / (len(series) * delimiter) for i in range(n)]
    density = np.array(density)
    probs = [1 - density[:i].sum() * delimiter for i in range(n+1)]
    probs = np.array(probs)
    ti = (probs < gamma).argmax()
    ti_1 = ti - 1
    d = (probs[ti_1] - gamma) / (probs[ti_1] - probs[ti])
    T_gamma = ti_1 + delimiter * d


    def p_work(time):
        index = (np.array([delimiter * i for i in range(n + 1)]) > time).argmax() - 1
        return 1 - density[:index].sum() * delimiter - (time - delimiter * index) * density[index], index


    P_work, _ = p_work(T1)
    intensity, idx = p_work(T2)
    intensity = density[idx] / intensity
    print("-" * 50)
    print(f"Середній наробіток до відмови Tср: {T_avg}")
    print(f"γ-відсотковий наробіток на відмову Tγ при γ = {gamma}: {T_gamma}")
    print(f"Ймовірність безвідмовної роботи на час {T1} годин: {P_work}")
    print(f"Інтенсивність відмов на час {T2} годин: {intensity}")