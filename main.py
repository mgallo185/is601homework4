"""main.py"""
import sys
from decimal import Decimal, InvalidOperation
from calculator import Calculator

def calculate_and_print(num1, num2, operation_name):
    '''calculate and print'''
    operation_mappings = {
        'add': Calculator.add,
        'subtract': Calculator.subtract,
        'multiply': Calculator.multiply,
        'divide': Calculator.divide
    }

    # Unified error handling for decimal conversion
    try:
        # Convert inputs to decimals
        a_decimal, b_decimal = map(Decimal, [num1, num2])

        # Check if the operation exists and perform the calculation
        operation = operation_mappings.get(operation_name)
        if operation:
            result = operation(a_decimal, b_decimal)
            print(f"The result of {num1} {operation_name} {num2} is equal to {result}")
        else:
            print(f"Unknown operation: {operation_name}")

    except InvalidOperation:
        # Catch invalid number input
        print(f"Invalid number input: {num1} or {num2} is not a valid number.")
    except ZeroDivisionError:
        # Catch division by zero errors
        print("Error: Division by zero.")
    except Exception as e:
        # Catch any other unexpected errors
        print(f"An error occurred: {e}")

def main():
    '''main function'''
    if len(sys.argv) != 4:
        print("Usage: python main.py <number1> <number2> <operation>")
        sys.exit(1)

    _, a, b, operation = sys.argv
    calculate_and_print(a, b, operation)

if __name__ == '__main__':
    main()
