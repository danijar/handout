import inspect
import os
import shutil


TMP_DIR = 'report'


def display(fig):
  info = _get_user_frame_info()
  os.makedirs(TMP_DIR, exist_ok=True)
  filename = _get_image_name(info.filename, info.lineno)
  filename = os.path.join(TMP_DIR, filename)
  fig.savefig(filename)


def generate(filepath):
  assert filepath.endswith('.html')
  info = _get_user_frame_info()
  module = inspect.getmodule(info.frame)
  source = inspect.getsource(module)
  output = ['<link rel="stylesheet" href="style.css">']
  output.append('<pre>')
  mode = _Mode.CODE
  for lineno, line in enumerate(source.split('\n')):
    lineno += 1  # Line numbers are 1-based indices.
    line = line.rstrip()
    if mode == _Mode.CODE and line.startswith('"""'):
      mode = _Mode.TEXT
      output.append('</pre>')
      output.append('<p>')
      continue
    if mode == _Mode.TEXT and line.endswith('"""'):
      mode = _Mode.CODE
      output.append('</p>')
      output.append('<pre>')
      continue
    plot = _get_image_name(info.filename, lineno)
    if mode == _Mode.CODE and os.path.exists(os.path.join(TMP_DIR, plot)):
      output.append('</pre>')
      output.append('<img src="{}" />'.format(plot))
      output.append('<pre>')
      continue
    if lineno == info.lineno:
      assert mode == _Mode.CODE
      continue
    output.append(line)
  print(output[-1])
  if output[-1] == '<pre>':
    output = output[:-1]
  else:
    output.append('</pre>')
  os.makedirs(TMP_DIR, exist_ok=True)
  shutil.copyfile('style.css', os.path.join(TMP_DIR, 'style.css'))
  with open(os.path.join(TMP_DIR, filepath), 'w') as f:
    f.write('\n'.join(output))


class _Mode(object):

  CODE = 1
  TEXT = 2
  PLOT = 3


def _get_user_frame_info():
  for info in inspect.stack():
    if info.filename == __file__:
      continue
    break
  return info


def _get_image_name(filename, lineno):
  return '{}-F{}.png'.format(filename, lineno)
