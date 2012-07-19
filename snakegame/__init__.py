import argparse

from snakegame.engines import BUILTIN_ENGINES
from snakegame.bots import BUILTIN_BOTS

def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--engine')
    args = parser.parse_args(argv)
    print args
