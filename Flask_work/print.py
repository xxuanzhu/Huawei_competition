from math import e
import math
import matplotlib.pyplot as plt
import numpy as np

"""简单log函数的实现"""
if __name__ == '__main__':
    x = np.arange(1, 37, 1)
    print(x)
    y = np.log(x)



plt.plot(x, y, color="#9F35FF", linewidth=2)


plt.legend(loc="lower right")
plt.xlabel("deadline")
plt.ylabel("cost sensitivity")
plt.grid(True)
plt.show()
