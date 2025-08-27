
class Restaurant:
    def __init__(self):
        self.menu_items = {} # Dict
        self.book_table = []
        self.customer_orders = []
        self.waitlist = []
        self.total_revenue = None
    
    # Menu
    def add_item_to_menu(self,item,price):
        self.menu_items[item] = price

    def update_item(self,item,new_price):
        if item in self.menu_items:
            self.menu_items[item] = new_price
            print(f"Updated {item} price.")
        else:
            print("Item not found.")

    def remove_item(self,item):
        if item in self.customer_orders:
            print("This item is in use and can't be removed.")
        else:
            self.menu_items.pop(item)
            print("Item removed from menu.")

    def display_menu(self):
        c = input("Do you want it sorted by price? (yes/no):").lower()
        if c == "no":
            print("\n Our menu: ")
            for item, price in self.menu_items.items():
                print(f"{item}: {price}DA")
        elif c == "yes":
            print("\n Our menu: ")
            sorted_menu = dict(sorted(self.menu_items.items(), key=lambda item: item[1]))
            for item,price in sorted_menu.items():
                print(f"{item}: {price}DA")

    # Booking tables
    def book_tables(self,table_nbr,customer_name):
        if not any(t[0] == table_nbr for t in self.book_table):
            self.book_table.append((table_nbr,customer_name))
            print(f"Table {table_nbr} booked successfully.")
        else:
            self.waitlist.append((table_nbr,customer_name))
            print(f"Table {table_nbr} already booked. You are now on the waitlist")

    def cancel_table(self, table_nbr,customer_name):
        if table_nbr in self.book_table:
            self.book_table.remove((table_nbr,customer_name))
            print("Reservation cancelled.")
            if any(t[0] == table_nbr for t in self.waitlist):
                self.book_tables(self.waitlist[0][0],self.waitlist[0][1])
                self.waitlist.remove((table_nbr,customer_name))
        else:
            print("This table isn't booked.")

    def print_table_reservations(self):
        print("Booked tables:")
        if self.book_table:
            for table_nbr in self.book_table:
                print(f"Table {table_nbr}.")
        else:
            print("No reservations yet.")

    # Orders
    def customer_order(self,order,table_nbr):
        if order not in self.menu_items:
            print("This item is not available.")
        elif table_nbr not in self.book_table:
            print("This table is not booked.")
        else:
            order_details ={"table_number": table_nbr, "order": order}
            self.customer_orders.append(order_details)
            print(f"Order taken for table {table_nbr}: {order}")

    def print_orders(self):
        print("Customer orders:")
        if self.customer_orders:
            for order_details in self.customer_orders:
                print(f"Table {order_details['table_nbr']}: {order_details['order']}")
            else:
                print("No orders yet.")

def show_options(menu_options,choice):
    if choice =="0":
        print("See you again soon!")
        return False
    elif choice in menu_options:
        try: 
            menu_options[choice]()
        except ValueError:
            print("Invalid choice")
    else:
        print("Invalid choice")


my_restaurant = Restaurant()
customer_options = {
    "A" : my_restaurant.display_menu,
    "B" : lambda: my_restaurant.book_tables(
        int(input("Enter table number: ")),
        input("Enter your name:")
    ),
    "C" : lambda: my_restaurant.cancel_table(
        int(input("Enter table number: ")),
        input("Enter your name:")
    ),
    "D" : lambda: my_restaurant.customer_order(
        input("Enter order: "),
        int(input("Enter table number: "))
    )
}

employee_options = {
    "A": lambda: my_restaurant.add_item_to_menu(
        input("Enter item: "),
        int(input("Enter price: "))
    ),
    "B": lambda: my_restaurant.update_item(
        input("Enter item: "),
        int(input("Enter new price: "))
    ),
    "C": lambda: my_restaurant.remove_item(
        input("Enter item: ")
    ),
    "D": my_restaurant.print_table_reservations,
    "E": my_restaurant.print_orders,

}

while True:
    person = input("Are you an employee or a customer? (answer customer/employee or 0 to exit): ")
    if person == "0":
        break
    elif person == "customer":
        while True:
            print("--------Welcome to our restaurant!--------")
            print("What can we do for you?")
            print("A- Show Menu") 
            print("B- Book a table")
            print("C- Cancel a table")
            print("D- Order")
            print("0- Exit")
            
            choice = input("Enter you choice: ")
            if show_options(customer_options,choice) == False:
                break

    elif person == "employee":
        while True:
            print("A- Add item to the menu")
            print("B- Update item")
            print("C- Remove item")
            print("D- Show table reservations")
            print("E- Show orders")
            print("0- Exit")

            choice = input("Enter you choice: ")
            if show_options(employee_options,choice) == False:
                break

    else:
        print("Invalid choice")
        