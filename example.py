import matplotlib.pyplot as plt
import numpy as np
import doc

document = doc.Document('output')

"""
# Welcome

Top-level docstrings are formatted as Markdown text cells.
"""

fig, ax = plt.subplots()
ax.plot(np.sin(np.arange(100)))

document.figure(fig)  # This line shows the inline figure instead.

"""
Another plot.
"""

fig, ax = plt.subplots()
ax.plot(np.arange(100))
document.figure(fig)

document.save()
