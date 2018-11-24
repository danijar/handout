"""
# Python Handout v0.2.0

Combine source code, Markdown text, and figures.
"""

import handout
import matplotlib.pyplot as plt
import numpy as np

"""Start your handout by passing an output directory."""

doc = handout.Handout('output')

"""
## Markdown text

Comments with triple quotes are converted to text blocks.

Text blocks support [Markdown formatting][1], for example:

- Headlines
- Hyperlinks
- Inline `code()` snippets
- **Bold** and *italic*

[1]: https://commonmark.org
"""

"""
## Print output

Write variables to our handout, same syntax as Python's `print()`:
"""
for index in range(3):
  doc.write('Iteration', index)

"""
## Inline figures

Display matplotlib figures on the handout using `display()`:
"""
fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(np.arange(100))
fig.tight_layout()
doc.display(fig)  # Display the figure below this line.

"""Multiple plots are inserted right after another."""

for iteration in range(3):
  fig, ax = plt.subplots(figsize=(3, 2))
  x = np.arange(100) / (iteration + 1)
  y = np.sin(x)
  ax.plot(x, y)
  doc.display(fig, width=0.33)

"""
## Exclude lines

Hide code from the handout with the `# handout=exclude` comment:
"""

# Invisible below:
value = 13  # handout=exclude

"""
## View the handout

When you're done, save the handout and open output/index.html in your browser.
You can also pass your own CSS style file to this function.
"""

doc.save()
