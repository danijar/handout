import handout


def test_handout_on_title_arg_inserts_title(tmp_path):
    doc = handout.Handout(directory=tmp_path, title='This string')
    output = doc._generate(source='')
    assert '<title>This string</title>' in output
