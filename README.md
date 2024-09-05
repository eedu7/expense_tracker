# Expense Tracker
Sample solution for the [expense-tracker](https://roadmap.sh/projects/expense-tracker) challenge from [roadmap.sh](https://roadmap.sh/).

## How to run

Clone the repository and run the following command:

```bash
git clone https://github.com/eedu7/expense_tracker.git
cd expense-tracker
python main.py add --description "Lunch" --amount 20
```

Run the following command to build and run the project:

```bash
$ expense-tracker add --description "Lunch" --amount 20
# Expense added successfully (ID: 1)

$ expense-tracker add --description "Dinner" --amount 10
# Expense added successfully (ID: 2)

$ expense-tracker list
# ID  Date       Description  Amount
# 1   2024-08-06  Lunch        $20
# 2   2024-08-06  Dinner       $10

$ expense-tracker summary
# Total expenses: $30

$ expense-tracker delete --id 1
# Expense deleted successfully

$ expense-tracker summary
# Total expenses: $20

$ expense-tracker summary --month 8
# Total expenses for August: $20
```
