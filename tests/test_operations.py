"""Test operations"""
from decimal import Decimal
import pytest
from faker import Faker
from calculator.calculation import Calculation
from calculator.operations import add, subtract, multiply, divide

# Initialize Faker
fake = Faker()

def test_operation_add():
    '''Testing the addition operation with random values'''
    a = fake.pydecimal(left_digits=2, right_digits=2, positive=True)
    b = fake.pydecimal(left_digits=2, right_digits=2, positive=True)
    calculation = Calculation(a, b, add)
    assert calculation.perform() == a + b, "Add operation failed"

def test_operation_subtract():
    '''Testing the subtract operation with random values'''
    a = fake.pydecimal(left_digits=2, right_digits=2, positive=True)
    b = fake.pydecimal(left_digits=2, right_digits=2, positive=True)
    calculation = Calculation(a, b, subtract)
    assert calculation.perform() == a - b, "Subtract operation failed"

def test_operation_multiply():
    '''Testing the multiply operation with random values'''
    a = fake.pydecimal(left_digits=2, right_digits=2, positive=True)
    b = fake.pydecimal(left_digits=2, right_digits=2, positive=True)
    calculation = Calculation(a, b, multiply)
    assert calculation.perform() == a * b, "Multiply operation failed"

def test_operation_divide():
    '''Testing the divide operation with random values'''
    a = fake.pydecimal(left_digits=2, right_digits=2, positive=True)
    b = fake.pydecimal(left_digits=2, right_digits=2, positive=True)
    # Ensure b is not zero
    if b == Decimal('0'):
        b = Decimal('1')

    calculation = Calculation(a, b, divide)
    assert calculation.perform() == a / b, "Divide operation failed"

def test_divide_by_zero():
    '''Testing the divide by zero exception'''
    a = fake.pydecimal(left_digits=2, right_digits=2, positive=True)
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        calculation = Calculation(a, Decimal('0'), divide)
        calculation.perform()
