import collections
import glob
import inspect
import io
import logging
import os
import shutil
import sys

from handout import blocks


class Handout(object):

  def __init__(self, directory):
    self._directory = os.path.expanduser(directory)
    os.makedirs(self._directory, exist_ok=True)
    self._blocks = collections.defaultdict(list)
    self._logger = logging.getLogger('handout')
    for info in inspect.stack():
      if info.filename == __file__:
        continue
      break
    module = inspect.getmodule(info.frame)
    self._source_name = info.filename
    self._source_text = inspect.getsource(module)
    self._num_figures = 0

  def write(self, *args, **kwargs):
    stream = io.StringIO()
    if kwargs.get('file', sys.stdout) == sys.stdout:
      kwargs['file'] = stream
    print(*args, **kwargs)  # Print into custom stream.
    message = stream.getvalue()
    block = blocks.Message([message])
    self._blocks[self._get_current_line()].append(block)
    self._logger.info(message.rstrip('\n'))

  def html(self, string):
    block = blocks.Html([string])
    self._blocks[self._get_current_line()].append(block)
    self._logger.info(string)

  def display(self, figure, width=None):
    filename = 'figure-{}.png'.format(self._num_figures)
    block = blocks.Image(filename, width)
    self._blocks[self._get_current_line()].append(block)
    filename = os.path.join(self._directory, filename)
    figure.savefig(filename)
    self._logger.info('Saved figure: {}'.format(filename))
    self._num_figures += 1

  def save(self, name='index.html', style=None):
    output = self._generate(self._source_text)
    filename = os.path.join(self._directory, name)
    with open(filename, 'w') as f:
      f.write(output)
    datadir = os.path.join(os.path.dirname(__file__), 'data')
    shutil.copyfile(
        style or os.path.join(datadir, 'style.css'),
        os.path.join(self._directory, 'style.css'))
    names = 'highlight.css highlight.js marked.js script.js favicon.ico'
    for name in names.split():
      shutil.copyfile(
          os.path.join(datadir, name),
          os.path.join(self._directory, name))
    self._logger.info("Handout written to: {}".format(filename))

  def _generate(self, source):
    content = []
    content.append(blocks.Html([
        '<html>',
        '<head>',
        '<title>Handout</title>',
        '<link rel="stylesheet" href="style.css">',
        '<link rel="stylesheet" href="highlight.css">',
        '<link rel="shortcut icon" type="image/x-icon" href="favicon.ico">',
        '<script src="marked.js"></script>',
        '<script src="script.js"></script>',
        '<script src="highlight.js"></script>',
        '<script>hljs.initHighlightingOnLoad();</script>',
        '</head>',
        '<body>',
        '<article>',
    ]))
    content.append(blocks.Code())
    for lineno, line in enumerate(source.split('\n')):
      lineno += 1  # Line numbers are 1-based indices.
      line = line.rstrip()
      if isinstance(content[-1], blocks.Code) and line.startswith('"""'):
        line = line[3:]
        content.append(blocks.Text())
      if isinstance(content[-1], blocks.Text) and line.endswith('"""'):
        line = line[:-3]
        content[-1].append(line)
        content.append(blocks.Code())
        continue
      if not line.endswith('# handout=exclude'):
        content[-1].append(line)
      blocks_ = self._blocks[lineno]
      if blocks_:
        for block in blocks_:
          content.append(block)
        content.append(blocks.Code())
    content.append(blocks.Html([
        '</article>',
        '</body>',
        '</html>',
    ]))
    return ''.join(block.render() for block in content)

  def _get_current_line(self):
    for info in inspect.stack():
      if info.filename == self._source_name:
        return info.lineno
    message = (
        "Handout object was created in '{}' and accessed in '{}'. The file in "
        "which you create the handout will be rendered. Thus, it only makes "
        "sense to add to the handout from this file or functions called from "
        "this file. You should not pass the handout object to a parent file.")
    raise RuntimeError(message.format(self._source_name, info.filename))
