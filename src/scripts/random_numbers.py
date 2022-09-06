import numpy as np
import paths

# Generate some data
random_numbers = np.random.randn(100,10)
np.savetxt(paths.data / "random_numbers.dat", random_numbers)