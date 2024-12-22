import json
import time
from database import SQLiteDataSink
from django_database import get_expression
from interpreter import *
from parserc import *


def process_message(message, equation):
    """
    Processes a single message using the given equation.
    """
    message_obj = json.loads(message)
    attr_value = message_obj.get("value", "")  # Get returns default value if not found
    kpi_id = message_obj.get("kpi_id", "N/A")  # Get KPI ID if available

    # Check if attr_value is numeric
    try:
        numeric_value = float(attr_value)
    except ValueError:
        numeric_value = None

    lexer = Lexer(equation)
    parser = Parser(lexer)

    try:
        if "Regex" in equation:  # Handles regex equations
            interpreter = Interpreter(parser, attr_value)
        else:  # Handles arithmetic equations
            if numeric_value is None:
                raise ValueError(f"Non-numeric value '{attr_value}' cannot be used in arithmetic equations")
            parser.attr_value = numeric_value  # Pass numeric value to parser
            interpreter = Interpreter(parser, str(numeric_value))

        tree = parser.parse()
        if tree is None:  # Ensuring tree is valid
            raise Exception("Failed to parse equation: Invalid AST")

        result = interpreter.visit(tree)

        output_message = {
            "kpi_id": kpi_id,
            "equation": equation,
            "value": attr_value,
            "result": result
        }
        return output_message

    except Exception as e:
        raise Exception(f"Error processing message: {e}")


def read_equation(config_file):
    """
    Reads the equation from the config file.
    """
    with open(config_file, "r") as file:
        return file.read().strip()


# class FileReader:
#     """
#     Reads new records from a file incrementally.
#     """
#     def __init__(self, file_path):
#         self.file_path = file_path
#         self.last_position = 0

#     def read_new_records(self):
#         """Read new records from the file starting from the last position."""
#         with open(self.file_path, "r") as file:
#             file.seek(self.last_position)
#             records = file.readlines()
#             self.last_position = file.tell()
#         return [record.strip() for record in records if record.strip()]


class DataProcessor:
    """
    Processes records and applies the equation to them.
    """
    def __init__(self, input_file, equation, output_file):
        self.input_file = input_file
        self.equation = equation
        self.output_file = output_file

    def process_records(self):
        """
        Processes records from the input file and saves output to a JSON file.
        """
        output_results = []  # Collect results to write to the output file

        with open(self.input_file, "r") as file:
            records = json.load(file)

        for record in records:
            try:
                asset_id = record.get("kpi_id")
                output_message = process_message(json.dumps(record), self.equation)
                print(output_message)
                output_results.append(output_message)
            except Exception as e:
                print(f"Error processing record: {record}, Error: {e}")

        # Write all results to the output JSON file
        with open(self.output_file, "w") as out_file:
            json.dump(output_results, out_file, indent=4)
        print(f"Results saved to {self.output_file}")


def main():
    input_file = "djangoTask/kpi_values.json"
    config_file = "config.txt"
    output_file = "output_results.json"

    try:
        equation = read_equation(config_file)
        processor = DataProcessor(input_file, equation, output_file)
        print(f"Processor initialized with input_file = {input_file}, equation = {equation}, output_file = {output_file}")

        processor.process_records()
    except Exception as e:
        print(f"Failed to initialize processor: {e}")


if __name__ == "__main__":
    main()
