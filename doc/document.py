import collections
import glob
import inspect
import io
import os
import shutil
import sys

from doc import blocks


class Document(object):

  def __init__(self, directory):
    self._outdir = os.path.expanduser(directory)
    os.makedirs(self._outdir, exist_ok=True)
    self._figdir = os.path.join(self._outdir, 'figures')
    if os.path.exists(self._figdir):
      shutil.rmtree(self._figdir)
    os.makedirs(self._figdir)
    self._messages = collections.defaultdict(list)

  def display(self, figure):
    info = self._get_user_frame_info()
    filename = self._next_image_name(info.filename, info.lineno)
    figure.savefig(filename)

  def write(self, *args, **kwargs):
    stream = io.StringIO()
    if kwargs.get('file', sys.stdout) == sys.stdout:
      kwargs['file'] = stream
    print(*args, **kwargs)  # Print into custom stream.
    message = stream.getvalue()
    info = self._get_user_frame_info()
    self._messages[(info.filename, info.lineno)].append(message)

  def save(self, name='index.html', style=None):
    info = self._get_user_frame_info()
    module = inspect.getmodule(info.frame)
    source = inspect.getsource(module)
    output = self._generate(info, source)
    filename = os.path.join(self._outdir, name)
    with open(filename, 'w') as f:
      f.write(output)
    datadir = os.path.join(os.path.dirname(__file__), 'data')
    shutil.copyfile(
        style or os.path.join(datadir, 'style.css'),
        os.path.join(self._outdir, 'style.css'))
    shutil.copyfile(
        os.path.join(datadir, 'highlight.css'),
        os.path.join(self._outdir, 'highlight.css'))
    shutil.copyfile(
        os.path.join(datadir, 'highlight.js'),
        os.path.join(self._outdir, 'highlight.js'))
    shutil.copyfile(
        os.path.join(datadir, 'marked.js'),
        os.path.join(self._outdir, 'marked.js'))
    shutil.copyfile(
        os.path.join(datadir, 'script.js'),
        os.path.join(self._outdir, 'script.js'))

  def _generate(self, info, source):
    content = []
    content.append(blocks.Html([
        '<link rel="stylesheet" href="style.css">',
        '<link rel="stylesheet" href="highlight.css">',
        '<script src="marked.js"></script>',
        '<script src="script.js"></script>',
        '<script src="highlight.js"></script>',
        '<script>hljs.initHighlightingOnLoad();</script>',
    ]))
    content.append(blocks.Code())
    for lineno, line in enumerate(source.split('\n')):
      lineno += 1  # Line numbers are 1-based indices.
      line = line.rstrip()
      if line.endswith('# report=exclude'):
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
      messages = self._messages[(info.filename, lineno)]
      if isinstance(content[-1], blocks.Code) and messages:
        content.append(blocks.Message())
        for message in messages:
          content[-1].append(message)
        content.append(blocks.Code())
        continue
      filenames = self._find_image_names(info.filename, lineno)
      if isinstance(content[-1], blocks.Code) and filenames:
        for filename in filenames:
          filename = os.path.relpath(filename, self._outdir)
          content.append(blocks.Image(filename))
        content.append(blocks.Code())
        continue
    return '\n'.join(block.render() for block in content)

  def _next_image_name(self, filename, lineno):
    count = len(self._find_image_names(filename, lineno))
    filename = '{}-L{}-{}.png'.format(filename, lineno, count)
    filename = os.path.join(self._figdir, filename)
    return filename

  def _find_image_names(self, filename, lineno):
    pattern = '{}-L{}-*.png'.format(filename, lineno)
    pattern = os.path.join(self._figdir, pattern)
    return sorted(glob.glob(pattern))

  def _get_user_frame_info(self):
    for info in inspect.stack():
      if info.filename == __file__:
        continue
      break
    return info
