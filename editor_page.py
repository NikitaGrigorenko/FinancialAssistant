import os
import json
from datetime import datetime
from constants import category_type
from PyQt5.QtGui import QColor, QPalette
from financial_logic import FinancialLogic
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QWidget, QComboBox, QTextEdit, QInputDialog, QMessageBox


class EditExpenseWindow(QDialog):
    """
    Represents a dialog window for editing an expense.

    This class provides a dialog window with an input field for entering the
    updated expense amount. It emits the accepted signal when the edit is
    submitted.
    """

    def __init__(self, parent=None):
        """
        Initializes the EditExpenseWindow dialog.

        Args:
            parent (QWidget): The parent widget (default: None).
        """
        super().__init__(parent)
        self.setWindowTitle("Edit Expense")
        self.amount_label = QLabel("Enter the updated expense amount:")
        self.amount_input = QLineEdit()
        self.submit_button = QPushButton("Submit")
        self.cancel_button = QPushButton("Cancel")

        layout = QVBoxLayout()
        layout.addWidget(self.amount_label)
        layout.addWidget(self.amount_input)
        layout.addWidget(self.submit_button)
        layout.addWidget(self.cancel_button)
        self.setLayout(layout)

        self.submit_button.setStyleSheet(
            "background-color: #5DA56C; color: white; font-weight: bold; font-size: 14px;")
        self.cancel_button.setStyleSheet(
            "background-color: #5DA56C; color: white; font-weight: bold; font-size: 14px;")

        self.submit_button.clicked.connect(self.submit_edit)
        self.cancel_button.clicked.connect(self.close)

    def submit_edit(self):
        """
        Submits the edited expense.

        Retrieves the entered amount from the input field and emits the
        accepted signal.
        """
        amount = self.amount_input.text()
        self.accept()


class ExpenseTracker(QWidget):
    """
    Represents an expense tracking application.

    This class provides a graphical user interface for managing expenses. It
    allows adding, editing, and deleting expenses, as well as showing total
    expenses and expenses by category.
    """

    def __init__(self):
        """
        Initializes the ExpenseTracker widget.
        """
        super().__init__()
        self.logic = FinancialLogic()
        self.expense_amount_input = None
        self.expense_category_input = None
        self.expense_description_input = None

        self.current_month = datetime.now().strftime("%B")

        self.init_ui()

    def init_ui(self):
        """
        Initializes the user interface of the ExpenseTracker widget.
        """
        layout = QVBoxLayout()

        label = QLabel("Expense Tracker")
        label.setStyleSheet(
            "color: #20553F; font-weight: bold; font-size: 24px;")
        layout.addWidget(label)
        self.resize(800, 600)

        self.expense_amount_input = QLineEdit()
        self.expense_amount_input.setPlaceholderText(
            "Enter the expense amount")
        layout.addWidget(self.expense_amount_input)

        self.expense_category_input = QComboBox()
        for category in category_type.values():
            self.expense_category_input.addItem(category)
        layout.addWidget(self.expense_category_input)

        self.expense_description_input = QTextEdit()
        self.expense_description_input.setPlaceholderText(
            "Enter a description of the expense")
        layout.addWidget(self.expense_description_input)

        add_expense_button = QPushButton("Add Expense")
        add_expense_button.setStyleSheet(
            "background-color: #5DA56C; color: white; font-weight: bold; font-size: 14px;")
        add_expense_button.clicked.connect(self.add_expense)
        layout.addWidget(add_expense_button)

        edit_expense_button = QPushButton("Edit Expense")
        edit_expense_button.setStyleSheet(
            "background-color: #5DA56C; color: white; font-weight: bold; font-size: 14px;")
        edit_expense_button.clicked.connect(self.edit_expense)
        layout.addWidget(edit_expense_button)

        delete_expense_button = QPushButton("Delete Expense")
        delete_expense_button.setStyleSheet(
            "background-color: #5DA56C; color: white; font-weight: bold; font-size: 14px;")
        delete_expense_button.clicked.connect(self.delete_expense)
        layout.addWidget(delete_expense_button)

        show_total_expenses_button = QPushButton("Show Total Expenses")
        show_total_expenses_button.setStyleSheet(
            "background-color: #5DA56C; color: white; font-weight: bold; font-size: 14px;")
        show_total_expenses_button.clicked.connect(self.show_total_expenses)
        layout.addWidget(show_total_expenses_button)

        show_expenses_by_category_button = QPushButton(
            "Show Expenses by Category")
        show_expenses_by_category_button.setStyleSheet(
            "background-color: #5DA56C; color: white; font-weight: bold; font-size: 14px;")
        show_expenses_by_category_button.clicked.connect(
            self.show_expenses_by_category)
        layout.addWidget(show_expenses_by_category_button)

        self.return_main_button = QPushButton("Back to Main Page")
        self.return_main_button.setStyleSheet(
            "background-color: #5DA56C; color: white; font-weight: bold; font-size: 14px;")
        layout.addWidget(self.return_main_button)

        self.setLayout(layout)
        self.setWindowTitle("Expense Tracker")
        palette = self.palette()
        palette.setColor(QPalette.Background, QColor(220, 240, 230))
        self.setPalette(palette)
        self.show()

        file_path = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), "expenses.json")
        if os.path.exists(file_path):
            try:
                with open(file_path, "r") as file:
                    json_data = json.load(file)
                    self.logic.expenses = json_data.get("money", {})
            except FileNotFoundError:
                pass

        palette = self.palette()
        palette.setColor(QPalette.Background, QColor(220, 240, 230))
        self.setPalette(palette)

    def add_expense(self):
        """
        Adds an expense.

        Retrieves the amount, category, and description from the input fields and
        calls the add_expense method of the FinancialLogic class to add the
        expense.
        """
        amount = float(self.expense_amount_input.text())
        category = self.expense_category_input.currentIndex() + 1
        description = self.expense_description_input.toPlainText()
        self.logic.add_expense(amount, category_type[category], description)
        self.show_success_message("Expense added successfully.")

    def edit_expense(self):
        """
        Edits an expense.

        Retrieves the selected expense description and index from the user,
        opens an EditExpenseWindow dialog for entering the updated amount, and
        calls the edit_expense method of the FinancialLogic class to edit the
        expense.
        """
        category = self.expense_category_input.currentIndex() + 1
        expenses_available = self.logic.get_expenses_by_category(
            category_type[category])
        if not expenses_available:
            self.show_info_message(
                "No expenses available for editing in this category.")
            return

        descriptions = [expense['description']
                        for expense in expenses_available]

        item, ok = QInputDialog.getItem(
            self, "Select Expense to Edit", "Expense Description:", descriptions, editable=False)
        if ok and item:
            index = next((index for index, expense in enumerate(
                expenses_available) if expense['description'] == item), None)
            if index is not None:
                edit_window = EditExpenseWindow(self)
                if edit_window.exec_() == QDialog.Accepted:
                    amount = edit_window.amount_input.text()
                    if amount:
                        amount = float(amount)
                        description = self.expense_description_input.toPlainText()
                        self.logic.edit_expense(
                            category_type[category], index, amount, description)
                        self.show_success_message(
                            "Expense edited successfully.")
                    else:
                        self.show_info_message(
                            "Please enter the updated expense amount.")

    def delete_expense(self):
        """
        Deletes an expense.

        Retrieves the selected expense description and index from the user and
        calls the delete_expense method of the FinancialLogic class to delete
        the expense.
        """
        category = self.expense_category_input.currentIndex() + 1
        expenses_available = self.logic.get_expenses_by_category(
            category_type[category])
        if not expenses_available:
            self.show_info_message(
                "No expenses available for deleting in this category.")
            return
        palette = self.palette()
        palette.setColor(QPalette.Background, QColor(220, 240, 230))
        self.setPalette(palette)

        descriptions = [expense['description']
                        for expense in expenses_available]

        item, ok = QInputDialog.getItem(
            self, "Select Expense to Delete", "Expense Description:", descriptions, editable=False)
        if ok and item:
            index = next((index for index, expense in enumerate(
                expenses_available) if expense['description'] == item), None)
            if index is not None:
                self.logic.delete_expense(category_type[category], index)
                self.show_success_message("Expense deleted successfully.")

    def show_total_expenses(self):
        """
        Shows the total expenses.

        Calls the calculate_total_expenses method of the FinancialLogic class to
        calculate the total expenses and displays them in an information
        message box.
        """
        total_expenses = self.logic.calculate_total_expenses()
        self.show_info_message(f"Total expenses: {total_expenses}")

    def show_expenses_by_category(self):
        """
        Shows expenses by category.

        Retrieves the selected category and calls the get_expenses_by_category
        method of the FinancialLogic class to retrieve the expenses in that
        category. Displays the expenses in an information message box.
        """
        category_num = self.expense_category_input.currentIndex() + 1
        expenses_by_category = self.logic.get_expenses_by_category(
            category_type[category_num])
        if not expenses_by_category:
            self.show_info_message(
                f"No expenses in the category {category_type[category_num]}.")
        else:
            message = f"Expenses in the category {category_type[category_num]}:\n"
            for index, expense in enumerate(expenses_by_category):
                message += f"Index: {index}, Amount: {expense['amount']}, Description: {expense['description']}\n"
            self.show_info_message(message)

    def show_success_message(self, message):
        """
        Displays a success message box.

        Args:
            message (str): The message to display.
        """
        msg_box = QMessageBox()
        msg_box.setText(message)
        msg_box.setWindowTitle("Success")
        msg_box.exec_()

    def show_info_message(self, message):
        """
        Displays an information message box.

        Args:
            message (str): The message to display.
        """
        msg_box = QMessageBox()
        msg_box.setText(message)
        msg_box.setWindowTitle("Information")
        msg_box.exec_()
