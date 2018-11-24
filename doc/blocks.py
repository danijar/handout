from doc import tools


class Html(object):

  def __init__(self, lines=None):
    self.lines = lines or []

  def append(self, line):
    self.lines.append(line)

  def render(self):
    return '\n'.join(tools.strip_empty_lines(self.lines))


class Code(object):

  def __init__(self, lines=None):
    self.lines = lines or []

  def append(self, line):
    self.lines.append(line)

  def render(self):
    lines = '\n'.join(tools.strip_empty_lines(self.lines))
    if not lines:
      return ''
    return '<pre><code class="python">' + lines + '</code></pre>'


class Text(object):

  def __init__(self, lines=None):
    self.lines = lines or []

  def append(self, line):
    self.lines.append(line)

  def render(self):
    lines = tools.strip_empty_lines(self.lines)
    if not lines:
      return []
    return '<div class="markdown">' + '\n'.join(lines) + '</div>'


class Image(object):

  def __init__(self, filename):
    self.filename = filename

  def append(self, line):
    raise NotImplementedError()

  def render(self):
    return '<img src="{}" />'.format(self.filename)
