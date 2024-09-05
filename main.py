import os
from datetime import datetime
import argparse

from numpy import argwhere
from requests import head


class ExpenseHandler:
    def __init__(self, filename="expense.csv"):
        self.filename = filename
        if not os.path.isfile(filename):
            self.create_file(self.filename)

    def read_file(self):
        try:
            with open(self.filename, "r") as file:
                return [line.strip().split(",") for line in file]
        except FileNotFoundError:
            print("File not found")
            return []

    def create_file(self, filename):
        try:
            with open(filename, "w") as file:
                file.write("id,date,amount,description\n")
        except IOError:
            print(f"Error creating file '{filename}'.")

    def _date(self):
        date = datetime.today()
        return f"{date.day}-{date.month}-{date.year}"

    def add_expense(self, amount, description=None):
        date = self._date()
        expense_id = self.expense_id()
        expense = f"{expense_id},{date},{amount},{description}"

        try:
            with open("expense.csv", "a") as file:
                file.write(f"{expense}\n")

            print("Expense added successfully (ID: {})".format(expense_id))
        except IOError:
            print("Error adding expense.")

        

    def delete_expense(self, id, expenses):
        updated_expense = list(filter(lambda x: x[0] != id, expenses))

        with open(self.filename, "w") as file:
            for expense in updated_expense:
                file.write(f"{','.join(expense)}\n")

    def expense_id(self):
        expenses = self.read_file()
        if len(expenses) == 1:
            return 1
        return int(expenses[-1][0]) + 1

    def filter_expenses(self, expenses, filter_by, filter_value):
        if filter_by == "description":
            return list(filter(lambda x: x[3] == filter_value, expenses))
        elif filter_by == "id":
            return list(filter(lambda x: x[0] == filter_value, expenses))
        elif filter_by == "month":
            return self._filter_by_month(expenses, filter_value)
        elif filter_by == "year":
            return self._filter_by_year(expenses, filter_value)
        elif filter_by == "day":
            return self._filter_by_day(expenses, filter_value)
        else:
            print("Invalid filter option.")
            return []

    def _filter_by_month(self, expenses, month):
        filtered_list = []

        for expense in expenses[1:]:
            if expense[1].split("-")[1] == month:
                filtered_list.append(expense)
        return filtered_list

    def _filter_by_year(self, expenses, year):
        filtered_list = []

        for expense in expenses[1:]:
            if expense[1].split("-")[2] == year:
                filtered_list.append(expense)
        return filtered_list

    def _filter_by_day(self, expenses, day):
        filtered_list = []

        for expense in expenses[1:]:
            if expense[1].split("-")[0] == day:
                filtered_list.append(expense)
        return filtered_list

    def list_expenses(self, expenses):
        heading = ["id", "date", "amount", "description"]
        if not expenses:
            expenses.append(heading)
        if expenses[0] != heading:
            expenses.insert(0, heading)
        for expense in expenses:
            # Formatting for better readability
            id = expense[0]
            date = expense[1]
            amount: str = expense[2]
            description = expense[3]
            
            amount = "$"+amount if not amount.isalpha() else amount

            s = f"{id.ljust(3, " ")}|{date.center(10, " ")}|{amount.center(10, " ")}|{description.rjust(12, " ")}"
            print(s)

    def summary(self, expenses, month=None, day=None, year=None):
        filtered_expenses = expenses
        if day:
            filtered_expenses = self.filter_expenses(expenses, "day", day)
        elif month:
            filtered_expenses = self.filter_expenses(expenses, "month", month)
        elif year:
            filtered_expenses = self.filter_expenses(expenses, "year", year)
        total_amount = sum([float(i[2]) for i in filtered_expenses])
        return total_amount


def main():
    parser = argparse.ArgumentParser(description="Process some files.")
    parser.add_argument("input", type=str, help="Command")
    parser.add_argument("--description", type=str, help="Description of the expense")
    parser.add_argument("--amount", type=str, help="Amount spent on expense")
    parser.add_argument("--id", type=str, help="Expense Id")
    parser.add_argument("--day", type=str, help="Expense day")
    parser.add_argument("--month", type=str, help="Expense Month")
    parser.add_argument("--year", type=str, help="Expense Year")

    args = parser.parse_args()._get_kwargs()
    command = args[0][1]
    description = args[1][1]
    amount = args[2][1]
    expense_id = args[3][1]
    day = args[4][1]
    month = args[5][1]
    year = args[6][1]

    expense_handler = ExpenseHandler()
    expenses = expense_handler.read_file()
    match command:
        case "add":
            expense_handler.add_expense(amount, description)
        case "delete":
            expense_handler.delete_expense(expense_id, expenses)
            print("Expense deleted successfully.")
        case "list":
            expense_handler.list_expenses(expenses)
        case "summary":
            total_amount = expense_handler.summary(
                expenses, day=day, month=month, year=year
            )
            print(f"Total amount spent: ${total_amount:.2f}")


if __name__ == "__main__":
    main()
