import argparse
import csv
import re

class CSVDataCleanup:
  def __init__(self, input_file, output_file):
    self.input_file = input_file
    self.output_file = output_file

  def remove_duplicates(self):
    with open(self.input_file, mode="r") as file:
      reader = csv.DictReader(file)
      unique_rows = [dict(t) for t in {tuple(d.items()) for d in reader}]

    with open(self.output_file, mode="w", newline="") as file:
      writer = csv.DictWriter(file, fieldnames=unique_rows[0].keys())
      writer.writeheader()
      writer.writerows(unique_rows)

  def correct_formatting(self):
    with open(self.input_file, mode="r") as file:
      reader = csv.DictReader(file)
      corrected_rows = []

      for row in reader:
        if "phone" in row and row["phone"]:
          row["phone"] = re.sub(r'\D', '', row["phone"])

          if len(row["phone"]) == 10:
            row["phone"] = f'({row["phone"][:3]})-{row["phone"][3:6]}-{row["phone"][6:]}'

        corrected_rows.append(row)

    with open(self.output_file, mode="w", newline="") as file:
      writer = csv.DictWriter(file, fieldnames=corrected_rows[0].keys())
      writer.writeheader()
      writer.writerows(corrected_rows)

def parse_arguments():
  parser = argparse.ArgumentParser(description="Data Cleanup Tool for CSV Files")
  parser.add_argument("input_file", help="Path to the input CSV file")
  parser.add_argument("output_file", help="Path to the output cleaned CSV file")
  parser.add_argument("-r", "--remove-duplicates", action="store_true", help="Remove duplicate rows from the CSV")
  parser.add_argument("-c", "--correct-formatting", action="store_true", help="Correct formatting issues in the CSV (e.g., phone numbers)")
  return parser.parse_args()

if __name__ == "__main__":
  args = parse_arguments()

  if not args.remove_duplicates and not args.correct_formatting:
    print("Error: You must provide at least one cleanup option.")
    exit(1)

  cleanup_tool = CSVDataCleanup(args.input_file, args.output_file)

  if args.remove_duplicates:
    cleanup_tool.remove_duplicates()
    print("Duplicates removed successfully!")

  if args.correct_formatting:
    cleanup_tool.correct_formatting()
    print("Formatting issues corrected successfully!")