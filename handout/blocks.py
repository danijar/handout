from handout import tools


class Html(object):

  def __init__(self, lines=None):
    self._lines = lines or []

  def append(self, line):
    self._lines.append(line)

  def render(self):
    return '\n'.join(tools.strip_empty_lines(self._lines))


class Code(object):

  def __init__(self, lines=None):
    self._lines = lines or []

  def append(self, line):
    self._lines.append(line)

  def render(self):
    lines = '\n'.join(tools.strip_empty_lines(self._lines))
    if not lines:
      return ''
    lines = lines.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return '<pre><code class="python">' + lines + '</code></pre>\n'


class Text(object):

  def __init__(self, lines=None):
    self._lines = lines or []

  def append(self, line):
    self._lines.append(line)

  def render(self):
    lines = '\n'.join(tools.strip_empty_lines(self._lines))
    if not lines:
      return ''
    lines = lines.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return '<div class="markdown">' + lines + '</div>\n'


class Image(object):

  def __init__(self, filename, width=None):
    self._filename = filename
    self._width = width

  def append(self, line):
    raise NotImplementedError()

  def render(self):
    output = '<img '
    output += 'src="{}"'.format(self._filename)
    if self._width:
      output += 'width="{}%"'.format(round(100 * self._width, 2))
    output += ' />'
    return output


class Message(object):

  def __init__(self, lines=None):
    self._lines = lines or []

  def append(self, line):
    self._lines.append(line)

  def render(self):
    lines = []
    for line in self._lines:
      while len(line.rstrip('\n')) > 79:
        lines.append(line[:79] + '\n')
        line = line[79:]
      lines.append(line)
    return '<pre class="message">' + ''.join(lines) + '</pre>\n'
