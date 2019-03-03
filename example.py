"""
# Python Handout

Turn Python scripts into handouts with Markdown comments and inline figures. An
alternative to Jupyter notebooks without hidden state that supports any text
editor.
"""

import handout
import matplotlib.pyplot as plt
import numpy as np

"""Start your handout with an output directory."""

doc = handout.Handout('output')

"""
## Markdown comments

Comments with triple quotes are converted to text blocks.

Text blocks support [Markdown formatting][1], for example:

- Headlines
- Hyperlinks
- Inline `code()` snippets
- **Bold** and *italic*

[1]: https://commonmark.org/help/
"""

"""
## Add text and variables

Write to our handout using the same syntax as Python's `print()`:
"""
for index in range(3):
  doc.add_text('Iteration', index)
doc.show()

"""
## Add Matplotlib figures

Display matplotlib figures on the handout:
"""
fig, ax = plt.subplots(figsize=(4, 3))
ax.plot(np.arange(100))
fig.tight_layout()
doc.add_figure(fig)
doc.show()  # Display figure below this line.

"""
Set the width to display multiple figures side by side:
"""

for iteration in range(3):
  fig, ax = plt.subplots(figsize=(3, 2))
  ax.plot(np.sin(np.linspace(0, 20 / (iteration + 1), 100)))
  doc.add_figure(fig, width=0.33)
doc.show()

"""
## Exclude lines

Hide code from the handout with the `# handout: exclude` comment:
"""

# Invisible below:
value = 13  # handout: exclude

"""
## View the handout

The handout is automatically saved when you call `doc.show()`. Just open
`output/index.html` in your browser.
"""
