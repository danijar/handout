import matplotlib.pyplot as plt
import numpy as np
import doc

document = doc.Document('output')

"""
# Welcome

Top-level docstrings are formatted as Markdown text cells.
"""

for index in range(3):
  document.write('Iteration', index)

fig, ax = plt.subplots()
ax.plot(np.arange(100))

document.display(fig)  # This line shows the inline figure instead.

"""You can hide lines with `# report=exclude`."""

# Invisible below:
bar = 13  # report=exclude

"""
A series of multiple plots.
"""

for iteration in range(3):
  fig, ax = plt.subplots()
  x = np.arange(100) / (iteration + 1)
  y = np.sin(x)
  ax.plot(x, y)
  document.display(fig)

document.save()
