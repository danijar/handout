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
    if not style:
      style = os.path.join(os.path.dirname(__file__), 'style.css')
    shutil.copyfile(style, os.path.join(self._directory, 'style.css'))

  def _generate(self, info, source):
    CODE, TEXT = 1, 2
    output = ['<link rel="stylesheet" href="style.css">']
    output.append('<pre>')
    mode = CODE
    for lineno, line in enumerate(source.split('\n')):
      lineno += 1  # Line numbers are 1-based indices.
      line = line.rstrip()
      if mode == CODE and line.startswith('"""'):
        mode = TEXT
        output.append('</pre>')
        output.append('<p>')
        continue
      if mode == TEXT and line.endswith('"""'):
        mode = CODE
        output.append('</p>')
        output.append('<pre>')
        continue
      filename = self._get_image_name(info.filename, lineno)
      exists = os.path.exists(os.path.join(self._directory, filename))
      if mode == CODE and exists:
        output.append('</pre>')
        output.append('<img src="{}" />'.format(filename))
        output.append('<pre>')
        continue
      if lineno == info.lineno:
        assert mode == CODE
        continue
      output.append(line)
    if output[-1] == '<pre>':
      output = output[:-1]
    else:
      output.append('</pre>')
    return '\n'.join(output)

  def _get_image_name(self, filename, lineno):
    filename = '{}-L{}.png'.format(filename, lineno)
    return filename

  def _get_user_frame_info(self):
    for info in inspect.stack():
      if info.filename == __file__:
        continue
      break
    return info


class Code(object):

  def __init__(self, lines):
    self.lines = lines


class Text(object):

  def __init__(self, lines):
    self.lines = lines
