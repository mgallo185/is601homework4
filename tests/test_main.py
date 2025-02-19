"""test main and test cases for homework 4"""
import sys
from unittest.mock import patch
import runpy
import pytest
from main import calculate_and_print, main

@pytest.mark.parametrize("a_string, b_string, operation_string, expected_string", [
    ("5", "3", 'add', "The result of 5 add 3 is equal to 8"),
    ("10", "2", 'subtract', "The result of 10 subtract 2 is equal to 8"),
    ("4", "5", 'multiply', "The result of 4 multiply 5 is equal to 20"),
    ("20", "4", 'divide', "The result of 20 divide 4 is equal to 5"),
    ("1", "0", 'divide', "An error occurred: Cannot divide by zero"),
    ("9", "3", 'unknown', "Unknown operation: unknown"),
    ("a", "3", 'add', "Invalid number input: a or 3 is not a valid number."),
    ("5", "b", 'subtract', "Invalid number input: 5 or b is not a valid number."),
])
def test_calculate_and_print(a_string, b_string, operation_string, expected_string, capsys):
    """Test calculate and print from main"""
    calculate_and_print(a_string, b_string, operation_string)
    captured = capsys.readouterr()
    assert captured.out.strip() == expected_string

def test_argument_count(capsys):
    """Test argument count validation"""
    # Test correct arguments
    sys.argv = ["main.py", "5", "3", "add"]
    calculate_and_print("5", "3", "add")
    captured = capsys.readouterr()
    assert captured.out.strip() == "The result of 5 add 3 is equal to 8"

    # Test too few arguments
    sys.argv = ["main.py", "5", "3"]
    with pytest.raises(SystemExit):
        main()
    captured = capsys.readouterr()
    assert "Usage: python main.py <number1> <number2> <operation>" in captured.out

    # Test too many arguments
    sys.argv = ["main.py", "5", "3", "add", "extra"]
    with pytest.raises(SystemExit):
        main()
    captured = capsys.readouterr()
    assert "Usage: python main.py <number1> <number2> <operation>" in captured.out

def test_main_success(capsys):
    """Test successful execution of main()"""
    with patch.object(sys, 'argv', ['main.py', '5', '3', 'add']):
        main()
        captured = capsys.readouterr()
        assert captured.out.strip() == "The result of 5 add 3 is equal to 8"

def test_unexpected_error(capsys):
    """Test handling of unexpected errors"""
    with patch('calculator.Calculator.add', side_effect=Exception("Unexpected test error")):
        calculate_and_print("5", "3", "add")
        captured = capsys.readouterr()
        assert captured.out.strip() == "An error occurred: Unexpected test error"

def test_module_execution(capsys):
    """Test direct module execution"""
    with patch.object(sys, 'argv', ['main.py', '5', '3', 'add']):
        runpy.run_module('main', run_name='__main__')
        captured = capsys.readouterr()
        assert captured.out.strip() == "The result of 5 add 3 is equal to 8"
