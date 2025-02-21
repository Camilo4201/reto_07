import json
from collections import deque, namedtuple

# Define a named tuple for MenuItem
MenuItemTuple = namedtuple('MenuItemTuple', ['name', 'price'])

class MenuItem:
    def __init__(self, name, price):
        self._name = name
        self._price = price

    @property
    def name(self):
        return self._name

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        self._price = value

    def calculate_total_price(self):
        return self.price


class Appetizer(MenuItem):
    def __init__(self, name, price):
        super().__init__(name, price)


class MainCourse(MenuItem):
    def __init__(self, name, price):
        super().__init__(name, price)


class Beverage(MenuItem):
    def __init__(self, name, price):
        super().__init__(name, price)

    def calculate_total_price(self, has_main_course):
        if has_main_course:
            return self.price * 0.9  # 10% discount
        return self.price


class Order:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def update_item(self, index, new_item):
        if 0 <= index < len(self.items):
            self.items[index] = new_item

    def delete_item(self, index):
        if 0 <= index < len(self.items):
            del self.items[index]

    def calculate_total_price(self):
        total = 0
        has_main_course = any(isinstance(item, MainCourse) for item in self.items)

        for item in self.items:
            if isinstance(item, Beverage):
                total += item.calculate_total_price(has_main_course)
            else:
                total += item.calculate_total_price()

        return total

    def save_menu(self, filename):
        menu_dict = {item.name: item.price for item in self.items}
        with open(filename, 'w') as f:
            json.dump(menu_dict, f)

    @classmethod
    def load_menu(cls, filename):
        with open(filename, 'r') as f:
            menu_dict = json.load(f)
            order = cls()
            for name, price in menu_dict.items():
                order.add_item(MenuItem(name, price))
            return order


class Payment:
    def __init__(self, order):
        self.order = order

    def process_payment(self):
        total_price = self.order.calculate_total_price()
        print(f"Processing payment for total amount: ${total_price:.2f}")


class Restaurant:
    def __init__(self):
        self.orders = deque()  # FIFO queue for managing orders

    def add_order(self, order):
        self.orders.append(order)

    def process_next_order(self):
        if self.orders:
            order = self.orders.popleft()  # Process the next order
            payment = Payment(order)
            payment.process_payment()
        else:
            print("No orders to process.")

# Example usage
if __name__ == "__main__":
    # Create a restaurant instance
    restaurant = Restaurant()

    # Create a new order
    order1 = Order()
    order1.add_item(Appetizer("Spring Rolls", 5.00))
    order1.add_item(MainCourse("Grilled Chicken", 15.00))
    order1.add_item(Beverage("Soda", 2.00))
    order1.add_item(Beverage("Wine", 10.00))

    # Save the menu to a JSON file
    order1.save_menu("menu.json")

    # Load the menu from a JSON file
    loaded_order = Order.load_menu("menu.json")

    # Add the order to the restaurant
    restaurant.add_order(loaded_order)

    # Process the next order
    restaurant.process_next_order()