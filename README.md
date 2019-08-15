# Python Handout

[![PyPI](https://img.shields.io/pypi/v/handout.svg)](https://pypi.python.org/pypi/handout/#history)

Turn Python scripts into handouts with Markdown comments and inline figures. An
alternative to Jupyter notebooks without hidden state that supports any text
editor.

| Code | Handout |
| ---- | ------- |
| ![Code](https://i.imgur.com/YEvUB9U.png) | ![Handout](https://i.imgur.com/dEGxaAz.png) |

## Getting started

You use Python Handout as a library inside a normal Python program:

1. Install via `pip3 install -U handout`.
2. Run your script via `python3 script.py`. (You can start with the `example.py`
   from the repository.)
3. Open `output/index.html` in your browser to view the result.
4. Iterate and refresh your browser.

## Features

Create the handout via `doc = handout.Handout(outdir)` to access these features:

| Feature | Example |
| ------- | ------- |
| Add [Markdown text][markdown] as triple-quote comments. | `"""Markdown text"""` |
| Add text via `print()` syntax. | `doc.add_text('text:', variable)` |
| Add image from array or url. | `doc.add_image(image, 'png', width=1)` |
| Add video from array or url. | `doc.add_video(video, 'gif', fps=30, width=1)` |
| Add matplotlib figure. | `doc.add_figure(fig, width=1)` |
| Add custom HTML. | `doc.add_html(string)` |
| Insert added items and save to `<outdir>/index.html`. | `doc.show()` |

[markdown]: https://commonmark.org/help/

## Questions

Feel free to create an issue on Github.
