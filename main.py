from datetime import datetime
import os
class ExpenseHandler:

    def __init__(self, filename= "expense.csv"):
        self.filename = filename
        if not os.path.isfile(filename):
            self.create_file(self.filename)
    def read_file(self, filename= "expense.csv"):
        try:
            with open(filename, "r") as file:
                return [line.strip().split(",") for line in file]
        except FileNotFoundError:
            print("File not found")
            return []
    


    def create_file(self, filename):
        try:
            with open(filename, "w") as file:
                file.write("id,date,category,amount,description,payment_method\n")
        except IOError:
            print(f"Error creating file '{filename}'.")
    def _date(self):
        date = datetime.today()
        return f"{date.day}-{date.month}-{date.year}"
    def add_expense(self, category,amount, description= None, payment_method=None):
        date = self._date()
        id = self.expense_id()
        # expense = f"{id},{date},{category},{amount}"
        expense = f"{id},{date},{category},{amount},{description},{payment_method}"

        # if description:
        #     expense += f",{description}"
        # if payment_method:
        #     expense += f",{payment_method}"

        try:
            with open("expense.csv", "a") as file:
                file.write(f"{expense}\n")
        except IOError:
            print("Error adding expense.")

    def expense_id(self):
        expenses = self.read_file()
        if len(expenses) == 1:
            return 1
        return int(expenses[-1][0]) + 1
    
    def print_expense(self, expenses):
        for expense in expenses:
            # Formatting for better readability
            id = expense[0]
            date = expense[1]
            category = expense[2]
            amount = expense[3]
            description = expense[4]
            payment_method = expense[5]

            s = f"{id.ljust(3, " ")}|{date.center(10, " ")}|{amount.center(10, " ")}|{category.center(20, " ")}|{description.center(40, " ")}|{payment_method.rjust(16, " ")}"
            print(s)

    def list_expenses(self):
        ...



def main():
    expense_handler = ExpenseHandler()
    data = expense_handler.read_file()
    # expense_handler.add_expense("Groceries", "10.99", "Buying fresh produce")
    expenses = expense_handler.read_file()
    expense_handler.print_expense(expenses)


if __name__ == '__main__':
    main()