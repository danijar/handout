import matplotlib.pyplot as plt
import numpy as np
import report

"""
Top-level docstrings are formatted as Markdown text cells.
"""

fig, ax = plt.subplots()
ax.plot(np.sin(np.arange(100)))

report.display(fig)  # This line shows the inline figure instead.

report.generate('report.html')
