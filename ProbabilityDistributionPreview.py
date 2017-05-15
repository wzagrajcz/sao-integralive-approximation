from ProbablityDistribution import *
import matplotlib.pyplot as plt
import os

map = {}
for i in range(32):
    map[i] = i + 1

samples = [0, 1, 4, 20, 100, 1000]

if not os.path.exists("plots/probability-distribution/"):
    os.makedirs("plots/probability-distribution/")

for i in samples:
    a = ProbabilityDistribution(map, i).probability
    plt.cla()
    plt.clf()
    plt.close()

    x = []
    y = []

    for (q, t) in a:
        x.append(q)
        y.append(t)
    plt.plot(x, y, 'ro')
    plt.ylim([0, 1.1*y[-1]])
    plt.title("Probability distribution for alpha=" + str(i))
    plt.ylabel("Probability")
    plt.xlabel("Element from map")
    plt.savefig("plots/probability-distribution/smpl_" + str(i) + ".jpg")

