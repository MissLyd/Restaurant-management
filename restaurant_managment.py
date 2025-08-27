
class Restaurant:
    def __init__(self):
        self.menu_items = {} # Dict
        self.book_table = {}
        self.customer_orders = []
        self.waitlist = []
        self.total_revenue = None
    

    # ------------------------Menu------------------------

    # 1- Adding a menu item with its positive price and valid season
    def add_item_to_menu(self,item,price = None,season = None,valid_seasons=None):

        # Checking if price is positive
        while price is None or price <= 0: 
            try:
                price = float(input("Enter a positive price: "))
                if price <= 0:
                    print("Price must be greater than 0.")
            except ValueError:
                print("Please enter a number.")
                price = None

        # Checking if season is valid
        while season not in valid_seasons:
            season = input(f"Enter season {valid_seasons}: ").capitalize()
            if season not in valid_seasons:
                print("Invalid season, try again.")

        # Adding item to nested dictionary
        self.menu_items[item] = {
            "price": price,
            "season": season
        }
    
    # 2- Updating an existing menu item
    def update_item(self,item):
        if item not in self.menu_items:
            print("Item not found.")
            return
        
        # Choosing what to update(season,price or both)
        choice = input("What do you want to update?(price/season/both): ").strip()

        if choice in ("price","both"):
            # Checking if new price is positive
            while True: 
                try:
                    new_price = float(input("Enter the new price: "))
                    if new_price <= 0:
                        print("Price must be greater than 0.")
                    else:
                        break
                except ValueError:
                    print("Please enter a number.")
            
            # updating the item's price
            self.menu_items[item]["price"] = new_price
            print(f"Updated {item} price.")

        if choice in ("season","both"):
            # Checking if new season is valid
            while True:
                new_season = input(f"Enter new season {valid_seasons}: ").capitalize().strip()
                if new_season in valid_seasons:
                    break
                else:
                    print("Invalid season, try again.")
            
            # updating the item's season
            self.menu_items[item]["season"] = new_season
            print(f"Updated {item} season.")
        
    # 3- Removing an item from the menu
    def remove_item(self,item):
        if item in self.customer_orders:
            print("This item is in use and can't be removed.") # Because it's in use
        else:
            self.menu_items.pop(item)
            print("Item removed from menu.")
    
    # 4- Displaying the menu
    def display_menu(self):

        choice = input("How do you want our menu sorted? (price/season/none): ").lower()

        if choice == "none":
            print("\n Our menu: ")
            for item, details in self.menu_items.items():
                print(f"{item}: {details["price"]}da, Season: {details["season"]}")

        elif choice == "price":
            print("\n Our menu: ")
            sorted_menu = dict(sorted(self.menu_items.items(), key=lambda item: item[1]["price"])) # Sorts the prices frommin to max
            for item, details in sorted_menu.items():
                print(f"{item}: {details["price"]}da, Season: {details["season"]}")

        elif choice=="season":
            print("\n Our menu: ")
            sorted_menu = dict(sorted(self.menu_items.items(), key=lambda item: item[1]["season"])) # Sorts season in alphabetic order
            for item, details in sorted_menu.items():
                print(f"{item}: {details["price"]}da, Season: {details["season"]}")

        else:
            print("Invalid choice. Showing unsorted menu by default:")
            for item, details in self.menu_items.items():
                print(f"{item}: {details["price"]}da, Season: {details["season"]}")
            

    # -----------------------Booking tables----------------------------

    def book_tables(self,table_nbr,customer_name):
        if table_nbr not in self.book_table:
            self.book_table[table_nbr] = customer_name
            print(f"Table {table_nbr} booked successfully.")
        else:
            self.waitlist.append((table_nbr,customer_name))
            print(f"Table {table_nbr} already booked. You are now on the waitlist")

    def cancel_table(self, table_nbr,customer_name):
        if table_nbr in self.book_table:
            self.book_table.pop(table_nbr)
            print("Reservation cancelled.")
            if any(t[0] == table_nbr for t in self.waitlist):
                self.book_tables[self.waitlist[0][0]] = self.waitlist[0][1]
                self.waitlist.remove((table_nbr,customer_name))
        else:
            print("This table isn't booked.")

    def print_table_reservations(self):
        print("Booked tables:")
        if self.book_table:
            for table_nbr in self.book_table:
                print(f"Table {table_nbr} booked by {self.book_table[table_nbr]}.")
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
valid_seasons = {"Spring","Summer","Winter","Autumn","All"}
customer_options = {
    "A" : my_restaurant.display_menu,
    "B" : lambda: my_restaurant.book_tables(
        int(input("Enter table number: ")),
        input("Enter your name: ").strip()
    ),
    "C" : lambda: my_restaurant.cancel_table(
        int(input("Enter table number: ")),
        input("Enter your name: ").strip()
    ),
    "D" : lambda: my_restaurant.customer_order(
        input("Enter order: ").strip(),
        int(input("Enter table number: "))
    )
}

employee_options = {
    "A": lambda: my_restaurant.add_item_to_menu(
        input("Enter item: ").strip(),
        int(input("Enter price: ")),
        input("Enter season: ").capitalize().strip(),
        valid_seasons
    ),
    "B": lambda: my_restaurant.update_item(
        input("Enter item: ").strip()
    ),
    "C": lambda: my_restaurant.remove_item(
        input("Enter item: ").strip()
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
        