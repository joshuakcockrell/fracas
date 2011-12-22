from distutils.core import setup
import py2exe
import operator
import sys


if operator.lt(len(sys.argv), 2):
    sys.argv.append('py2exe')

setup(windows = [{'script': "main.py"}],
      options = {"py2exe" : {'optimize': 2}},
      zipfile = "shared.lib")
