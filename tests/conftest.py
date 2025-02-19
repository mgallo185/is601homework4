"""# conftest.py"""
# conftest.py

from decimal import Decimal
from faker import Faker
from calculator.operations import add, subtract, multiply, divide

# Initialize Faker for generating random test data
fake = Faker()
fake.seed_instance(12345)

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
    for i in range(num_records):
        # Ensure we get both normal numbers and potential zero divisors
        if i % 4 == 0:
            a = Decimal('10')
            b = Decimal('0')
            operation_name = 'divide'
        else:
            a = Decimal(str(fake.random_number(digits=2)))
            b = Decimal(str(fake.random_number(digits=2)))
            operation_name = fake.random_element(elements=list(operation_mappings.keys()))

        operation_func = operation_mappings[operation_name]

        # Calculate expected result
        if operation_name == 'divide' and b == 0:
            # Skip division by zero cases as they're handled by test_divide_by_zero
            continue

        expected = operation_func(a, b)

        yield a, b, operation_name, operation_func, expected

def pytest_addoption(parser):
    """Add command-line option for number of test records"""
    parser.addoption(
        "--num_records",
        action="store",
        default=10,
        type=int,
        help="Number of test records to generate"
    )

def pytest_generate_tests(metafunc):
    """Generate test parameters"""
    if any(x in metafunc.fixturenames for x in ["a", "b", "expected"]):
        num_records = metafunc.config.getoption("num_records")
        parameters = list(generate_test_data(num_records))

        modified_parameters = [
            (a, b, operation_name, expected) if "operation_name" in metafunc.fixturenames
            else (a, b, operation_func, expected)
            for a, b, operation_name, operation_func, expected in parameters
        ]

        if modified_parameters:
            metafunc.parametrize("a,b,operation,expected", modified_parameters)
