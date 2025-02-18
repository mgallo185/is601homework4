"""# conftest.py"""
# conftest.py

from decimal import Decimal
from faker import Faker
from calculator.operations import add, subtract, multiply, divide

# Initialize Faker for generating random test data
fake = Faker()

def generate_test_data(num_records):
    """ generate test data"""
    # Define operation mappings for both Calculator and Calculation tests
    operation_mappings = {
        'add': add,
        'subtract': subtract,
        'multiply': multiply,
        'divide': divide
    }

    # Generate test data
    for _ in range(num_records):
        a = Decimal(fake.random_number(digits=2))
        b = Decimal(fake.random_number(digits=2)) if _ % 4 != 3 else Decimal(fake.random_number(digits=1))
        operation_name = fake.random_element(elements=list(operation_mappings.keys()))
        operation_func = operation_mappings[operation_name]

        # Ensure b is not zero for divide operation to prevent division by zero in expected calculation
        if operation_name == 'divide':
            b = Decimal('1') if b == Decimal('0') else b

        try:
            # Calculate the expected result
            expected = operation_func(a, b)
        except ZeroDivisionError:
            expected = "ZeroDivisionError"

        yield a, b, operation_name, operation_func, expected

def pytest_addoption(parser):
    """generate pytest"""
    # Add command-line option for specifying the number of test records to generate
    parser.addoption("--num_records", action="store", default=5, type=int, help="Number of test records to generate")

def pytest_generate_tests(metafunc):
    """check generate tests"""
    # Check if the test is expecting any of the dynamically generated fixtures
    if {"a", "b", "expected"}.intersection(set(metafunc.fixturenames)):
        num_records = metafunc.config.getoption("num_records")

        # Generate test data
        parameters = list(generate_test_data(num_records))

        # Modify parameters to fit test functions' expectations
        modified_parameters = []
        for a, b, operation_name, operation_func, expected in parameters:
            if 'operation_name' in metafunc.fixturenames:
                # For Calculator tests, use operation_name
                modified_parameters.append((a, b, operation_name, expected))
            elif 'operation' in metafunc.fixturenames:
                # For Calculation tests, use operation_func
                modified_parameters.append((a, b, operation_func, expected))

        # Parametrize the test function
        metafunc.parametrize("a,b,operation,expected", modified_parameters)