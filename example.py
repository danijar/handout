import matplotlib.pyplot as plt
import numpy as np
import doc

document = doc.Document('output')

"""
# Welcome

Top-level docstrings are formatted as Markdown text cells.
"""

fig, ax = plt.subplots()
ax.plot(np.arange(100))

document.display(fig)  # This line shows the inline figure instead.

"""
Another plot.
"""

for iteration in range(3):
  fig, ax = plt.subplots()
  x = np.arange(100) / (iteration + 1)
  y = np.sin(x)
  ax.plot(x, y)
  document.display(fig)

document.save()
