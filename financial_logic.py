import os
import json


class FinancialLogic:
    """
    Represents the financial logic for managing expenses.

    This class provides methods for adding, editing, deleting, and retrieving
    expenses. It also calculates the total expenses and saves the expenses to
    a JSON file.
    """

    def __init__(self):
        """
        Initializes the FinancialLogic class.

        Sets up the initial state with an empty dictionary to store expenses.
        """
        self.expenses = {}

    def add_expense(self, amount, category, description):
        """Adds an expense to the list of expenses

        Args:
            amount (float): The amount of the expense
            category (str): The category of the expense
            description (str): The description of the expense
        """
        expense = {
            'amount': amount,
            'description': description
        }
        if category not in self.expenses:
            self.expenses[category] = {
                'items': [expense], 'sumOfAmounts': amount}
        else:
            self.expenses[category]['items'].append(expense)
            self.expenses[category]['sumOfAmounts'] += amount
        self.save_expenses_to_json()

    def edit_expense(self, category, index, amount, description):
        """Edits an existing expense

        Args:
            category (str): The category of the expense
            index (int): The index of the expense to edit
            amount (float): The updated amount of the expense
            description (str): The updated description of the expense
        """
        if category in self.expenses and index < len(self.expenses[category]['items']):
            old_amount = self.expenses[category]['items'][index]['amount']
            self.expenses[category]['sumOfAmounts'] += amount - old_amount
            self.expenses[category]['items'][index]['amount'] = amount
            self.expenses[category]['items'][index]['description'] = description
            self.save_expenses_to_json()

    def delete_expense(self, category, index):
        """Deletes an existing expense

        Args:
            category (str): The category of the expense
            index (int): The index of the expense to delete
        """
        if category in self.expenses and index < len(self.expenses[category]['items']):
            deleted_expense = self.expenses[category]['items'].pop(index)
            self.expenses[category]['sumOfAmounts'] -= deleted_expense['amount']
            self.save_expenses_to_json()

    def calculate_total_expenses(self):
        """Calculates the total expenses

        Returns:
            float: the total amount of expenses
        """
        total_expenses = sum(category['sumOfAmounts']
                             for category in self.expenses.values())
        return total_expenses

    def get_expenses_by_category(self, category):
        """Get expenses based on category

        Args:
            category (str): The category of expense to retrieve

        Returns:
            list: the expenses of a certain category
        """
        if category in self.expenses:
            return self.expenses[category]['items']
        else:
            return []

    def save_expenses_to_json(self):
        """Saves expenses to a JSON file

        Args:
            filename (str): The name of the JSON file
        """
        json_data = {'money': self.expenses,
                     'totalSum': self.calculate_total_expenses()}
        file_path = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), 'expenses.json')
        with open(file_path, 'w') as file:
            json.dump(json_data, file, indent=4)
