import unittest

def load_tests(loader, tests, pattern):
    return loader.discover('backgammon/tests', pattern='test_*.py', top_level_dir='.')
