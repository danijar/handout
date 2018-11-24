import inspect
import os
import shutil

from doc import blocks


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
    datadir = os.path.join(os.path.dirname(__file__), 'data')
    shutil.copyfile(
        style or os.path.join(datadir, 'style.css'),
        os.path.join(self._directory, 'style.css'))
    shutil.copyfile(
        os.path.join(datadir, 'github.css'),
        os.path.join(self._directory, 'highlight.css'))
    shutil.copyfile(
        os.path.join(datadir, 'highlight.js'),
        os.path.join(self._directory, 'highlight.js'))

  def _generate(self, info, source):
    content = []
    content.append(blocks.Html([
        '<link rel="stylesheet" href="style.css">',
        '<link rel="stylesheet" href="highlight.css">',
        '<script src="highlight.js"></script>',
        '<script>hljs.initHighlightingOnLoad();</script>',
    ]))
    content.append(blocks.Code())
    for lineno, line in enumerate(source.split('\n')):
      lineno += 1  # Line numbers are 1-based indices.
      line = line.rstrip()
      if isinstance(content[-1], blocks.Code) and line.startswith('"""'):
        content.append(blocks.Text())
        continue
      if isinstance(content[-1], blocks.Text) and line.endswith('"""'):
        content.append(blocks.Code())
        continue
      filename = self._get_image_name(info.filename, lineno)
      exists = os.path.exists(os.path.join(self._directory, filename))
      if isinstance(content[-1], blocks.Code) and exists:
        content.append(blocks.Image(filename))
        content.append(blocks.Code())
        continue
      if lineno == info.lineno:
        # Skip `doc.save()` line.
        assert isinstance(content[-1], blocks.Code)
        continue
      assert isinstance(content[-1], (blocks.Code, blocks.Text))
      content[-1].append(line)
    return '\n'.join(block.render() for block in content)

  def _get_image_name(self, filename, lineno):
    filename = '{}-L{}.png'.format(filename, lineno)
    return filename

  def _get_user_frame_info(self):
    for info in inspect.stack():
      if info.filename == __file__:
        continue
      break
    return info
