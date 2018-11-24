import inspect
import os
import shutil


class Document(object):

  def __init__(self, directory):
    self._directory = os.path.expanduser(directory)
    os.makedirs(self._directory, exist_ok=True)

  def figure(self, figure):
    info = self._get_user_frame_info()
    filename = self._get_image_name(info.filename, info.lineno)
    filename = os.path.join(self._directory, filename)
    figure.savefig(filename)

  def save(self, name='index.html', style=None):
    info = self._get_user_frame_info()
    module = inspect.getmodule(info.frame)
    source = inspect.getsource(module)
    output = self._generate(info, source)
    filename = os.path.join(self._directory, name)
    with open(filename, 'w') as f:
      f.write(output)
    shutil.copyfile(
        style or os.path.join(os.path.dirname(__file__), 'style.css'),
        os.path.join(self._directory, 'style.css'))
    shutil.copyfile(
        os.path.join(os.path.dirname(__file__), 'github.css'),
        os.path.join(self._directory, 'highlight.css'))
    shutil.copyfile(
        os.path.join(os.path.dirname(__file__), 'highlight.js'),
        os.path.join(self._directory, 'highlight.js'))

  def _generate(self, info, source):
    blocks = []
    blocks.append(Html([
        '<link rel="stylesheet" href="style.css">',
        '<link rel="stylesheet" href="highlight.css">',
        '<script src="highlight.pack.js"></script>',
        '<script>hljs.initHighlightingOnLoad();</script>',
    ]))
    blocks.append(Code())
    for lineno, line in enumerate(source.split('\n')):
      lineno += 1  # Line numbers are 1-based indices.
      line = line.rstrip()
      if isinstance(blocks[-1], Code) and line.startswith('"""'):
        blocks.append(Text())
        continue
      if isinstance(blocks[-1], Text) and line.endswith('"""'):
        blocks.append(Code())
        continue
      filename = self._get_image_name(info.filename, lineno)
      exists = os.path.exists(os.path.join(self._directory, filename))
      if isinstance(blocks[-1], Code) and exists:
        blocks.append(Image(filename))
        blocks.append(Code())
        continue
      if lineno == info.lineno:
        # Skip `doc.save()` line.
        assert isinstance(blocks[-1], Code)
        continue
      assert isinstance(blocks[-1], (Code, Text))
      blocks[-1].append(line)
    return '\n'.join(block.render() for block in blocks)

  def _get_image_name(self, filename, lineno):
    filename = '{}-L{}.png'.format(filename, lineno)
    return filename

  def _get_user_frame_info(self):
    for info in inspect.stack():
      if info.filename == __file__:
        continue
      break
    return info


class Html(object):

  def __init__(self, lines=None):
    self.lines = lines or []

  def append(self, line):
    self.lines.append(line)

  def render(self):
    return '\n'.join(strip_empty_lines(self.lines))


class Code(object):

  def __init__(self, lines=None):
    self.lines = lines or []

  def append(self, line):
    self.lines.append(line)

  def render(self):
    lines = '\n'.join(strip_empty_lines(self.lines))
    if not lines:
      return ''
    return '<pre><code class="python">' + lines + '</code></pre>'


class Text(object):

  def __init__(self, lines=None):
    self.lines = lines or []

  def append(self, line):
    self.lines.append(line)

  def render(self):
    lines = strip_empty_lines(self.lines)
    if not lines:
      return []
    return '<p>' + ' '.join(lines) + '</p>'


class Image(object):

  def __init__(self, filename):
    self.filename = filename

  def append(self, line):
    raise NotImplementedError()

  def render(self):
    return '<img src="{}" />'.format(self.filename)


def strip_empty_lines(lines):
  output = []
  for line in lines:
    if not line and not output:
      continue
    output.append(line)
  lines = reversed(output)
  output = []
  for line in lines:
    if not line and not output:
      continue
    output.append(line)
  lines = reversed(output)
  return list(lines)
