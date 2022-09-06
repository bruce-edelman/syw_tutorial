import numpy as np
import matplotlib.pyplot as plt
import paths

# Load the data
data = np.loadtxt(paths.data / "random_numbers.dat")

# Plot the results
fig = plt.figure(figsize=(7,6))
plt.plot(data)
plt.savefig(paths.figures / "random_numbers.pdf")