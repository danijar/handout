import tempfile

from handout import Handout

def test_handout_on_title_arg_inserts_title():
    h = Handout(directory=tempfile.mkdtemp(), title="This string")._generate(source="")   
    assert "<title>This string</title>" in h