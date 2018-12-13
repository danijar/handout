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
    self._logs = collections.defaultdict(list)
    self._images = collections.defaultdict(list)
    self._logger = logging.getLogger('handout')
    for info in inspect.stack():
      if info.filename == __file__:
        continue
      self._used_from = info.filename
      break

  def display(self, figure, width=None):
    info = self._get_user_frame_info()
    index = len(self._images[(info.filename, info.lineno)])
    filename = '{}-L{}-{}.png'.format(info.filename, info.lineno, index)
    filename = os.path.join(self._directory, filename)
    self._images[(info.filename, info.lineno)].append((filename, width))
    figure.savefig(filename)
    self._logger.info('Saved figure: {}'.format(filename))

  def write(self, *args, **kwargs):
    stream = io.StringIO()
    if kwargs.get('file', sys.stdout) == sys.stdout:
      kwargs['file'] = stream
    print(*args, **kwargs)  # Print into custom stream.
    log = stream.getvalue()
    info = self._get_user_frame_info()
    self._logs[(info.filename, info.lineno)].append(log)
    self._logger.info(log.rstrip('\n'))

  def save(self, name='index.html', style=None):
    info = self._get_user_frame_info()
    module = inspect.getmodule(info.frame)
    source = inspect.getsource(module)
    output = self._generate(info, source)
    filename = os.path.join(self._directory, name)
    with open(filename, 'w') as f:
      f.write(output)
    datadir = os.path.join(os.path.dirname(__file__), 'data')
    shutil.copyfile(
        style or os.path.join(datadir, 'style.css'),
        os.path.join(self._directory, 'style.css'))
    shutil.copyfile(
        os.path.join(datadir, 'highlight.css'),
        os.path.join(self._directory, 'highlight.css'))
    shutil.copyfile(
        os.path.join(datadir, 'highlight.js'),
        os.path.join(self._directory, 'highlight.js'))
    shutil.copyfile(
        os.path.join(datadir, 'marked.js'),
        os.path.join(self._directory, 'marked.js'))
    shutil.copyfile(
        os.path.join(datadir, 'script.js'),
        os.path.join(self._directory, 'script.js'))
    self._logger.info("Handout written to: {}".format(filename))

  def _generate(self, info, source):
    content = []
    content.append(blocks.Html([
        '<html>',
        '<head>',
        '<link rel="stylesheet" href="style.css">',
        '<link rel="stylesheet" href="highlight.css">',
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
      if line.endswith('# handout=exclude'):
        continue
      if isinstance(content[-1], blocks.Code) and line.startswith('"""'):
        line = line[3:]
        content.append(blocks.Text())
      if isinstance(content[-1], blocks.Text) and line.endswith('"""'):
        line = line[:-3]
        content[-1].append(line)
        content.append(blocks.Code())
        continue
      content[-1].append(line)
      logs = self._logs[(info.filename, lineno)]
      if isinstance(content[-1], blocks.Code) and logs:
        content.append(blocks.Log())
        for log in logs:
          content[-1].append(log)
        content.append(blocks.Code())
        continue
      images = self._images[(info.filename, lineno)]
      if isinstance(content[-1], blocks.Code) and images:
        for filename, width in images:
          filename = os.path.relpath(filename, self._directory)
          content.append(blocks.Image(filename, width))
        content.append(blocks.Code())
        continue
    content.append(blocks.Html([
        '</article>',
        '</body>',
        '</html>',
    ]))
    return ''.join(block.render() for block in content)

  def _get_user_frame_info(self):
    for info in inspect.stack():
      if info.filename == self._used_from:
        return info
    message = (
        "Handout object was created in '{}' and accessed in '{}'. The file in "
        "which you create the handout will be rendered. Thus, it only makes "
        "sense to add to the handout from this file or functions called from "
        "this file. You should not pass the handout object to a parent file.")
    raise RuntimeError(message.format(self._used_from, info.filename))
