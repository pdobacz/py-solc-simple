import os
from solc_simple import Builder


def test_compilation_does_not_crash():
    OWN_DIR = os.path.dirname(os.path.realpath(__file__))

    def path(relative_path):
        joined = os.path.join(OWN_DIR, relative_path)
        return os.path.abspath(os.path.realpath(joined))

    builder = Builder(path('../priv'), path('../priv/build'))
    builder.compile_all()
