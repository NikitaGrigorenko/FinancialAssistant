import os
import sys
import json
from constants import data
from main_page import MainPage
from editor_page import ExpenseTracker
from helper_page import HelperPage
from PyQt5.QtWidgets import QApplication


class Application:
    """
    Represents the main application for the expense tracker.

    This class manages the switching between the main page and the editor page,
    loads data from a JSON file, and runs the application.
    """

    def __init__(self):
        """
        Initializes the Application class.

        It sets up the necessary objects and connects the signals and slots
        for switching between pages.
        """
        self.app = QApplication(sys.argv)
        self.editor_page = ExpenseTracker()
        self.main_page = MainPage()
        self.helper_page = HelperPage()

        self.editor_page.return_main_button.clicked.connect(
            self.switch_to_main_page)
        self.main_page.editor_button.clicked.connect(
            self.switch_to_editor_page)
        self.helper_page.return_main_button.clicked.connect(
            self.switch_to_main_page)
        self.main_page.helper_button.clicked.connect(
            self.switch_to_helper_page)

        self.switch_to_main_page()

    def switch_to_main_page(self):
        """
        Switches to the main page.

        Loads data, updates the main page with the loaded data, closes the
        editor page, and shows the main page.
        """
        self.load_data()
        self.main_page.update_data(self.data)
        self.editor_page.close()
        self.helper_page.close()
        self.main_page.show()

    def switch_to_editor_page(self):
        """
        Switches to the editor page.

        Closes the main page and shows the editor page.
        """
        self.main_page.close()
        self.editor_page.show()

    def switch_to_helper_page(self):
        """
        Switches to the helper page.

        Closes the main page and shows the helper page.
        """
        self.main_page.close()
        self.helper_page.show()

    def load_data(self):
        """
        Loads data from a JSON file.

        The JSON file is expected to be named 'expenses.json' and located in
        the same directory as the script file. The loaded data is stored in
        the instance variable 'data'.
        """
        file_path = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), 'expenses.json')
        with open(file_path) as file:
            self.data = json.load(file)

    def run(self):
        """
        Runs the application.

        Executes the application event loop.
        """
        sys.exit(self.app.exec_())


if __name__ == "__main__":
    file_path = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), 'expenses.json')
    
    if not os.path.exists(file_path):
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
    

    application = Application()
    application.run()
