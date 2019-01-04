# Python Handout

[![PyPI](https://img.shields.io/pypi/v/handout.svg)](https://pypi.python.org/pypi/handout/#history)

Turn Python scripts into handouts with Markdown comments and inline figures. An
alternative to Jupyter notebooks without hidden state and using your own text
editor.

| Code | Handout |
| ---- | ------- |
| ![Code](https://i.imgur.com/OZmSNfx.png) | ![Handout](https://i.imgur.com/O1n6R9c.png) |

## Getting started

You use Python Handout as a library inside a normal Python program:

1. Install via `pip3 install -U handout`.
2. Run your script via `python3 script.py`. (You can start with the `example.py`
   from the repository.)
3. Open `output/index.html` in your browser to view the handout.
4. Iterate and refresh your browser.

## Features

Create the handout via `doc = handout.Handout(outdir)` to access these features:

| Feature | Example |
| ------- | ------- |
| Add [Markdown text][markdown] as multi-line comments. | `"""Markdown text"""` |
| Add matplotlib figures. | `doc.display(fig, width=1.0)` |
| Add print messages. | `doc.write('text:', value)` |
| Add custom HTML. | `doc.html(string)` |
| Generate the report to `<outdir>/index.html`. | `doc.save()` |

Pro tip: You can save multiple times for fast feedback.

[markdown]: https://commonmark.org/help

## Questions

Feel free to create an issue on Github.
