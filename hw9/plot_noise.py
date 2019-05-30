import matplotlib.pyplot as plt
import pandas as pd
noise = pd.read_csv("noisy_data.out.txt", header=None, sep='\t')
plt.scatter(noise[0], noise[1])
plt.show()
