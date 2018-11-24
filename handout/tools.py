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
