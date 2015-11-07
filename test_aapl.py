#!/usr/bin/env python
"""Unit tests for test project.yahoo_options_data."""
from unittest import TestCase
from mock import patch

import json
import project.yahoo_options_data

computedJson = project.yahoo_options_data.contractAsJson("aapl.dat")
expectedJson = open("aapl.json").read()
expectedJson_change = open("aapl_change.json").read()

'''
class StandAloneTests(TestCase):
    """Test the stand-alone module functions."""
    @patch('__builtin__.open')
    def test_aapl(self, mock_open):
        """Test the yahoo_option_data function."""
        mock_open.return_value.read.return_value = \
            "aapl.dat\n"
        self.assertTrue(
		json.loads(computedJson) == json.loads(expectedJson) or json.loads(computedJson) == json.loads(expectedJson_change)
		)
'''
if json.loads(computedJson) != json.loads(expectedJson) and json.loads(computedJson) != json.loads(expectedJson_change):
  print "Test failed!"
  print "Expected output:", expectedJson
  print "Your output:", computedJson
  assert False
else:
  print "Test passed"
