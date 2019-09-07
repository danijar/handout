import collections
import inspect
import io
import logging
import pathlib
import shutil

from handout import blocks


MATHJAX_SCRIPTS = (
    '<script type="text/x-mathjax-config">'
    'MathJax.Hub.Config({tex2jax: {inlineMath: [["$","$"]]}});'
    '</script>'
    '<script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/'
    'MathJax.js?config=TeX-MML-AM_CHTML" async></script>'
)


class Handout(object):

  def __init__(self, directory, title='Handout'):
    self._directory = pathlib.Path(directory).expanduser()
    self._directory.mkdir(parents=True, exist_ok=True)
    self._title = title
    self._blocks = collections.defaultdict(list)
    self._pending = []
    # The logger is configured in handout/__init__.py to make it available
    # right after importing the handout package. This allows the user to change
    # the logging level, message format, etc.
    self._logger = logging.getLogger('handout')
    for info in inspect.stack():
      if info.filename == __file__:
        continue
      break
    module = inspect.getmodule(info.frame)
    self._source_name = info.filename
    self._source_text = inspect.getsource(module)
    self._num_images = 0
    self._num_videos = 0
    self._num_figures = 0

  def add_text(self, *args, **kwargs):
    show = kwargs.pop('show', False)
    stream = io.StringIO()
    kwargs['file'] = stream
    print(*args, **kwargs)  # Print into custom stream.
    message = stream.getvalue()
    block = blocks.Message([message])
    self._pending.append(block)
    # Remove up to one line break since the logger adds one.
    if message.endswith('\n'):
      message = message[:-1]
    self._logger.info(message)

  def add_image(self, image, format='png', width=None):
    if isinstance(image, str):
      filename = image
    else:
      import imageio
      filename = 'image-{}.{}'.format(self._num_images, format)
      imageio.imsave(self._directory / filename, image)
      self._logger.info('Saved image: {}'.format(filename))
    block = blocks.Image(filename, width)
    self._pending.append(block)
    self._num_images += 1

  def add_video(self, video, format='gif', fps=30, width=None):
    if isinstance(video, str):
      filename = video
    else:
      import imageio
      filename = 'video-{}.{}'.format(self._num_videos, format)
      imageio.mimsave(self._directory / filename, video, fps=fps)
      self._logger.info('Saved video: {}'.format(filename))
    if filename.endswith('.gif'):
      block = blocks.Image(filename, width)
    else:
      block = blocks.Video(filename, width)
    self._pending.append(block)
    self._num_videos += 1

  def add_html(self, string):
    block = blocks.Html([string])
    self._pending.append(block)
    self._logger.info(string)

  def add_figure(self, figure, width=None):
    filename = 'figure-{}.png'.format(self._num_figures)
    block = blocks.Image(filename, width)
    self._pending.append(block)
    filename = self._directory / filename
    figure.savefig(filename)
    self._logger.info('Saved figure: {}'.format(filename))
    self._num_figures += 1

  def show(self):
    self._blocks[self._get_current_line()] += self._pending
    self._pending = []
    output = self._generate(self._source_text)
    filename = self._directory / 'index.html'
    with open(filename, 'w') as f:
      f.write(output)
    datadir = pathlib.Path(__file__).parent / 'data'
    for source in datadir.glob('**/*'):
      target = self._directory / source.relative_to(datadir)
      if source.is_dir() or target.exists():
        continue
      target.parent.mkdir(exist_ok=True)
      shutil.copyfile(source, target)
    self._logger.info("Handout written to: {}".format(filename))

  def _generate(self, source):
    content = []
    content.append(blocks.Html([
        '<!DOCTYPE html>',
        '<html>',
        '<head>',
        '<title>{}</title>'.format(self._title),
        '<link rel="stylesheet" href="style.css">',
        '<link rel="stylesheet" href="highlight.css">',
        '<link rel="shortcut icon" type="image/x-icon" href="favicon.ico">',
        '<script src="marked.js"></script>',
        '<script src="script.js"></script>',
        '<script src="highlight.js"></script>',
        '<script>hljs.initHighlightingOnLoad();</script>',
        MATHJAX_SCRIPTS,
        '</head>',
        '<body>',
        '<article>',
    ]))
    content.append(blocks.Code())
    excluding = False  # Range exclude.
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
      if isinstance(content[-1], blocks.Text):
        content[-1].append(line)
      elif line == '# handout: begin-exclude':
        excluding = True
      elif line == '# handout: end-exclude':
        excluding = False
      elif excluding:
        pass
      elif line.endswith('# handout: exclude'):
        pass
      else:
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
