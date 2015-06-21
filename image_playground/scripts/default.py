import numpy as np

minval, maxval = np.min(image), np.max(image)
inverted = maxval - image + minval
