# <-------Import Statements------->
import sys
from database_coffee_machine import MENU, resources


# <-------Coffee Machine Object------->
class CoffeeMachine:
    def __init__(self):
        self.choice = self.take_choice()
        self.money_earned = 0
        self.choice_cost = 0
        self.choice_ingredients = {}
        self.resources_enough = None
        self.valid_choices = ['espresso', 'latte', 'cappuccino']
        self.redirecting_func()

    @staticmethod
    def take_choice():
        """This method takes coffee choice(input) of the user and returns it"""
        choice = input(
            "What would you like? (espresso/latte/cappuccino): \n").lower()
        return choice

    @staticmethod
    def final_termination_check():
        """This method terminates the program if resources available can't make any coffee in MENU"""
        if resources['water'] < 50 or resources['coffee'] < 18:
            print('Temporary shutdown due to lack of ingredients')
            sys.exit()

    def counter(self):
        """This method counts the money we earned"""
        self.money_earned += self.choice_cost
        return self.money_earned

    def update_resources(self):
        """This method updates the resources according to the purchase"""
        for ingredient, amount in self.choice_ingredients.items():
            resources[ingredient] = resources[ingredient] - amount

    def insert_coins(self):
        """This method takes input(coins) from the user and calculates the amount. It refunds the amount if inserted coins are less than actual prize, gives the change and coffee if it is more."""
        print(f"{self.choice} costs ${self.choice_cost}. Insert the coins.")
        quarters = int(input("How many quarters?: "))
        dimes = int(input("How many dimes?: "))
        nickels = int(input("How many nickels?: "))
        pennies = int(input("How many pennies?: "))

        amount_paid = (pennies / 100) + ((nickels * 5) / 100) + \
                      ((dimes * 10) / 100) + ((quarters * 25) / 100)
        balance = amount_paid - self.choice_cost

        if balance == 0:
            print(f"Here is your {self.choice}! Enjoy")
            self.update_resources()
            self.counter()
            self.final_termination_check()
            self.starter_terminator()
        elif balance > 0:
            print(f"Here is your balance amount. ${balance}")
            print(f"Here is your {self.choice}! Enjoy")
            self.update_resources()
            self.counter()
            self.final_termination_check()
            self.starter_terminator()
        elif balance < 0:
            print(f"The cost of {self.choice} is ${self.choice_cost}. You paid ${amount_paid}.")
            print(f"Please collect the refund amount: ${amount_paid}")
            self.starter_terminator()

    def starter_terminator(self):
        """This method restarts the process of CoffeeMachine object if user inputs 'yes' and terminates it with a 'no'"""
        on = input("Any other orders? 'yes' or 'no'? ").lower()
        if on == 'yes':
            self.choice = self.take_choice()
            self.redirecting_func()
        elif on == 'no':
            sys.exit()
        else:
            print('invalid input!, Try again')
            self.starter_terminator()

    def are_items_enough(self):
        """This method checks if the ingredients available are enough for selected coffee option."""
        for item in self.choice_ingredients:
            if resources[item] >= self.choice_ingredients[item]:
                pass
            else:
                print('Sorry, There is no enough ingredients for this.')
                return False
        return True

    def ingredients_and_cost(self):
        """The purpose of this method is to cut down the lines of code and avoid repeating lines in redirecting_func method"""
        self.choice_ingredients = MENU[self.choice]['ingredients']
        self.choice_cost = MENU[self.choice]['cost']

    def report_creator(self):
        """This method prints the report on resources and money earned"""
        for key in resources:
            value = resources[key]
            print(f"{key}: {value}")
        print(f"earned money is {self.money_earned}")

    def redirecting_func(self):
        """
        This method redirects to different other methods depending upon the user choice
        """
        if self.choice in self.valid_choices:
            self.ingredients_and_cost()

            if self.are_items_enough():
                self.insert_coins()
            else:
                self.starter_terminator()

        elif self.choice == 'report':
            self.report_creator()
            self.starter_terminator()

        elif self.choice == 'off':
            sys.exit()

        else:
            print('Invalid Input!')
            self.starter_terminator()


# <-------Instance of CoffeeMachine Object------->
coffee_machine = CoffeeMachine()
