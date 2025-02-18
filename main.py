import sys
from decimal import Decimal, InvalidOperation
from calculator import Calculator

def calculate_and_print(num1, num2, operation_name):
    '''Calculate and print'''
    operation_mappings = {
        'add': Calculator.add,
        'subtract': Calculator.subtract,
        'multiply': Calculator.multiply,
        'divide': Calculator.divide
    }

    try:
        # Convert input to decimals
        a_decimal, b_decimal = map(Decimal, [num1, num2])

        # Perform operation if valid, otherwise print error
        operation = operation_mappings.get(operation_name)
        if operation:
            result = operation(a_decimal, b_decimal)
            print(f"The result of {num1} {operation_name} {num2} is equal to {result}")
        else:
            print(f"Unknown operation: {operation_name}")

    except InvalidOperation:
        print(f"Invalid number input: {num1} or {num2} is not a valid number.")
    except ValueError as e:
        print(f"An error occurred: {e}")
    except Exception as e:  # Keep this to catch unexpected cases
        print(f"An error occurred: {e}")

def main():
    '''Main function'''
    if len(sys.argv) != 4:
        print("Usage: python main.py <number1> <number2> <operation>")
        sys.exit(1)

    _, a, b, operation = sys.argv
    calculate_and_print(a, b, operation)

if __name__ == '__main__':
    main()
