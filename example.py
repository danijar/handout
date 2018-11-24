import matplotlib.pyplot as plt
import numpy as np
import doc

document = doc.Document('output')

"""
Top-level docstrings are formatted as Markdown text cells.
"""

fig, ax = plt.subplots()
ax.plot(np.sin(np.arange(100)))

document.figure(fig)  # This line shows the inline figure instead.

document.save()
