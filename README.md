# Python Handout

Turn Python scripts into handouts with Markdown comments and inline figures. An
alternative to Jupyter notebooks without hidden state and using your own text
editor.

<img src="https://i.imgur.com/OZmSNfx.png" width="20%" />&nbsp;&nbsp;&nbsp;<img src="https://i.imgur.com/O1n6R9c.png" width="20%" />

## Instructions

- Install via `pip3 install --user handout`.
- Run your script via `python3 example.py`. You can start with the `example.py`
  from above.
- View the handout by opening `output/index.html` in your browser.

To iterate, edit your script, run it, and refresh your browser.

## How it works

You write a normal Python program.

- At the beginning, you create the handout class via `doc = Handout(directory)`.
- Define inline figures via `doc.display(fig)` and print variables via
  `doc.write(foo)`.
- At the end, call `doc.save()` to generate a HTML report.

## Dependencies

There are no dependencies. You scripts will typically use `matplotlib`.
