import handout
import numpy as np

doc = handout.Handout('output/full_width')

# Add some images.
for _ in range(16):
  image = np.ones((64, 64, 3)) * np.random.uniform(0, 1, 3)
  doc.add_image((255 * image).astype(np.uint8), width=0.24)

# Unset document width.
doc.add_html('<style>article { max-width: none; }</style>')
doc.show()
