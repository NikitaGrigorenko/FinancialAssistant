class FinancialLogic:
    def __init__(self):
        self.expenses = []

    def add_expense(self, amount, category, description):
        """Adds an expense to the list of expenses

        Args:
            amount (float): The amount of the expense
            category (str): The category of the expense
            description (str): The description of the expense
        """
        expense = {
            'amount': amount,
            'category': category,
            'description': description
        }
        self.expenses.append(expense)
        print("The expense has been added successfully.")

    def calculate_total_expenses(self):
        """Calculates the total expenses

        Returns:
            float: the total amount of expenses
        """
        total_expenses = sum(expense['amount'] for expense in self.expenses)
        return total_expenses

    def get_expenses_by_category(self, category):
        """Get expenses based on category

        Args:
            category (str): The category of expense to retrieve

        Returns:
            float: the amount of the expense of a certain category
        """
        expenses_by_category = [
            expense for expense in self.expenses if expense['category'] == category]
        return expenses_by_category

    def print_expenses(self):
        """Prints information about all expenses

        If there are no expenses, print the message "There are no costs to display."
        """
        if not self.expenses:
            print("There are no costs to display.")
        else:
            for expense in self.expenses:
                print(
                    f"Amount: {expense['amount']}, Category: {expense['category']}, Description: {expense['description']}")
