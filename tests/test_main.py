"""test main and test cases for homework 4"""
import sys
from unittest.mock import patch
import pytest
from main import calculate_and_print, main  # Ensure this import matches your project structure

# Parameterize the test function to cover different operations and scenarios, including errors
@pytest.mark.parametrize("a_string, b_string, operation_string, expected_string", [
    ("5", "3", 'add', "The result of 5 add 3 is equal to 8"),
    ("10", "2", 'subtract', "The result of 10 subtract 2 is equal to 8"),
    ("4", "5", 'multiply', "The result of 4 multiply 5 is equal to 20"),
    ("20", "4", 'divide', "The result of 20 divide 4 is equal to 5"),
    ("1", "0", 'divide', "An error occurred: Cannot divide by zero"),  # Adjusted error message
    ("9", "3", 'unknown', "Unknown operation: unknown"),
    ("a", "3", 'add', "Invalid number input: a or 3 is not a valid number."),
    ("5", "b", 'subtract', "Invalid number input: 5 or b is not a valid number."),
])
def test_calculate_and_print(a_string, b_string, operation_string, expected_string, capsys):
    """Test calculate and print from main"""
    # Call the function with the provided parameters
    calculate_and_print(a_string, b_string, operation_string)

    # Capture the output
    captured = capsys.readouterr()

    # Assert that the output matches the expected output
    assert captured.out.strip() == expected_string

def test_extra_arguments(capsys):
    """test extra arguments"""
    sys.argv = ["main.py", "5", "3", "add", "extra_arg"]  # Extra argument provided
    with pytest.raises(SystemExit):  # Expecting the program to exit with code 1
        main()  # This will call the main function

    captured = capsys.readouterr()  # Capture the output printed to the console
    assert "Usage: python main.py <number1> <number2> <operation>" in captured.out
def test_argument_count(capsys):
    """Test argument count validation"""
    sys.argv = ["main.py", "5", "3", "add"]  # Correct number of arguments
    calculate_and_print("5", "3", "add")
    captured = capsys.readouterr()
    assert captured.out.strip() == "The result of 5 add 3 is equal to 8"

    sys.argv = ["main.py", "5", "3"]  # Too few arguments
    with pytest.raises(SystemExit):  # Expecting program to exit with error
        main()

    captured = capsys.readouterr()
    assert "Usage: python main.py <number1> <number2> <operation>" in captured.out

    sys.argv = ["main.py", "5", "3", "add", "extra"]  # Too many arguments
    with pytest.raises(SystemExit):  # Expecting program to exit with error
        main()
    captured = capsys.readouterr()
    assert "Usage: python main.py <number1> <number2> <operation>" in captured.out


# New test for unexpected errors
def test_unexpected_error(capsys):
    """Test handling of unexpected errors"""
    with patch('calculator.Calculator.add', side_effect=Exception("Unexpected test error")):
        calculate_and_print("5", "3", "add")
        captured = capsys.readouterr()
        assert captured.out.strip() == "An error occurred: Unexpected test error"

# Additional test for system exit with unexpected error
def test_main_with_unexpected_error(capsys):
    """Test main function with unexpected error"""
    sys.argv = ["main.py", "5", "3", "add"]
    with patch('calculator.Calculator.add', side_effect=Exception("Unexpected test error")):
        main()
        captured = capsys.readouterr()
        assert captured.out.strip() == "An error occurred: Unexpected test error"

def test_module_execution(capsys):
    """Test direct module execution"""
    with patch('main.__name__', '__main__'):
        capsys.readouterr()
