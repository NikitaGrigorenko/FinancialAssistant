from financial_logic import FinancialLogic

# Dictionary of an available category types
category_type = {1: "Food",
                 2: "Transport",
                 3: "Sport",
                 4: "Home",
                 5: "Transfers",
                 6: "Clothing",
                 7: "Services",
                 8: "Education",
                 9: "Other",
                 10: "Medicine",
                 11: "Entertaiment"}

if __name__ == '__main__':
    logic = FinancialLogic()

    while True:
        print("1. Add Expense", "\n2. Show total expenses",
              "\n3. Show expenses by category", "\n4. Show all expenses", "\n5. Exit")

        choice = input("Choose an option (1-5): ")

        match choice:
            case '1':
                amount = float(input("Enter the expense amount: "))

                for key, value in category_type.items():
                    print(key, ':', ' '.join(str(x) for x in value))
                category_num = int(
                    input("Enter the number of expense category from the list above: "))
                description = input("Enter a description of the expense: ")
                logic.add_expense(
                    amount, category_type[category_num], description)

            case '2':
                total_expenses = logic.calculate_total_expenses()
                print(f"Total expenses: {total_expenses}")

            case '3':
                for key, value in category_type.items():
                    print(key, ':', ' '.join(str(x) for x in value))
                category_num = int(
                    input("Enter the number of expense category from the list above: "))
                expenses_by_category = logic.get_expenses_by_category(
                    category_type[category_num])

                if not expenses_by_category:
                    print(
                        f"No expenses in the category {category_type[category_num]}.")
                else:
                    print(
                        f"Expenses in the category {category_type[category_num]}:")
                    for expense in expenses_by_category:
                        print(
                            f"Amount: {expense['amount']}, Description: {expense['description']}")

            case '4':
                logic.print_expenses()

            case '5':
                break

            case _:
                print("Incorrect choice. Please choose from 1 to 5.")

        print('\n')
