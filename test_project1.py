import unittest, contextlib, io
from unittest import mock
from project1 import main

def _get_expected_output(sample_output: str) -> str:
    with open(sample_output) as output:
        return output.read()

def _get_program_output(sample_input : str) -> str:
    with mock.patch('builtins.input', return_value = sample_input):
        with contextlib.redirect_stdout(io.StringIO()) as project:
            main()

    return project.getvalue()

class TestSimulation(unittest.TestCase):

    def test_file_not_found(self):
        output_file = 'tests/asdasd.txt'

        self.assertEqual('FILE NOT FOUND\n', _get_program_output(output_file))

    def test_sample_input_ordered(self):
        output_file = 'tests/sample_output/sample_output.txt'
        expected = _get_expected_output(output_file)

        input_file = 'tests/sample_input/sample_input.txt'
        program_res = _get_program_output(input_file)

        self.assertEqual(expected, program_res)

    def test_sample_input_unordered(self):
        output_file = 'tests/sample_output/sample_output.txt'
        expected = _get_expected_output(output_file)

        input_file = 'tests/sample_input/sample_input_with_different_order.txt'
        program_res = _get_program_output(input_file)

        self.assertEqual(expected, program_res)

    def test_sample_input_two_alert_at_same_time(self):
        output_file = 'tests/sample_output/sample_output_two_alert_at_same_time.txt'
        expected = _get_expected_output(output_file)

        input_file = 'tests/sample_input/sample_input_two_alert_at_the_same_time.txt'
        program_res = _get_program_output(input_file)

        self.assertEqual(expected, program_res)

    def test_sample_input_two_cancel_at_same_time(self):
        output_file = 'tests/sample_output/sample_output_two_cancel_at_same_time.txt'
        expected = _get_expected_output(output_file)

        input_file = 'tests/sample_input/sample_input_two_cancel_at_same_time.txt'
        program_res = _get_program_output(input_file)

        self.assertEqual(expected, program_res)

    def test_sample_input_cancel_before_alert(self):
        output_file = 'tests/sample_output/sample_output_cancel_before_alert.txt'
        expected = _get_expected_output(output_file)

        input_file = 'tests/sample_input/sample_input_cancel_before_alert.txt'
        program_res = _get_program_output(input_file)

        self.assertEqual(expected, program_res)

    def test_sample_input_cancel_and_alert_at_same_time(self):
        output_file = 'tests/sample_output/sample_output_alert_and_cancel_at_same_time.txt'
        expected = _get_expected_output(output_file)

        input_file = 'tests/sample_input/sample_input_alert_and_cancel_at_same_time.txt'
        program_res = _get_program_output(input_file)

        self.assertEqual(expected, program_res)

    def test_sample_input_no_cancel(self):
        output_file = 'tests/sample_output/sample_output_no_canel.txt'
        expected = _get_expected_output(output_file)

        input_file = 'tests/sample_input/sample_input_no_cancel.txt'
        program_res = _get_program_output(input_file)

        self.assertEqual(expected, program_res)

    def test_sample_input_no_alert(self):
        output_file = 'tests/sample_output/sample_output_no_alert.txt'
        expected = _get_expected_output(output_file)

        input_file = 'tests/sample_input/sample_input_no_alert.txt'
        program_res = _get_program_output(input_file)

        self.assertEqual(expected, program_res)

    def test_sample_starting_alert_and_cancel_device_are_diff(self):
        output_file = 'tests/sample_output/sample_output_starting_alert_and_cancel_have_different_device.txt.txt'
        expected = _get_expected_output(output_file)

        input_file = 'tests/sample_input/sample_input_starting_alert_and_cancel_have_different_device.txt'
        program_res = _get_program_output(input_file)

        self.assertEqual(expected, program_res)

if __name__ == "__main__":
    unittest.main()

