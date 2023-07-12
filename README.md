# Financial Assistant
   **The project for the Innopolis University Python Programming Course**

A PC application that will help the user keep track of their finances. Set the upper limit of spending per month. Add new expenses, and edit old ones. Withdraw the amount for a certain period. As a bonus, there will be an auxiliary thing that will tell you in which category you need to make fewer expenses to fulfill the budget. The design of the app will be implemented by using PyQT.

# Team members

- Nikita Grigorenko (Team Lead and developer)
- Insaf Yusupov (developer)

## Build instructions

Prerequisites:
- Python 3.8
- PyQT5

> Note : Currently we working on .exe format to run the app

```bash
# Navigate to the cloned Git repository folder with the source code of our tool
cd financial_assistant
```

## Sample Usage

The syntax for a sample invocation of this app is as follows:

```bash
python3 main.py
```

After launching our app for the first time, you will be asked to set a budget for the current month. It will look like this.
After you do this, the main page will remain in front of you, which will show your spending by category this month.
![alt text](https://github.com/NikitaGrigorenko/FinancialAssistant/blob/main/assets/1.png)

By switching to the edit page, you can add new expenses, edit existing ones, and delete expenses.
![alt text](https://github.com/NikitaGrigorenko/FinancialAssistant/blob/main/assets/2.png)

The assistant page shows you the categories in which it is worth reducing expenses in order not to exceed the budget.
![alt text](https://github.com/NikitaGrigorenko/FinancialAssistant/blob/main/assets/3.png)
