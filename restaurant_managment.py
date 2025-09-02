
class Restaurant:
    def __init__(self):
        self.menu_items = {} # menu_items = { item: {"price": price,"Season":season} }
        self.book_table = {} # book_table = {"table nbr": customer name}
        self.customer_orders = [] # customer_orders= [{ 
                                                        #"table": table_nbr,
                                                        #"customer": customer name, 
                                                        # "items": [(item_name, qty)],
                                                        #  "total": float,
                                                        # "rating": float,
                                                        # }]
        self.waitlist = [] # waitlist= [(customer name, table nbr)]
        self.total_revenue = None
    

    # ------------------------------------------------Menu------------------------------------------------

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
            

    # -----------------------------------------------Tables----------------------------------------------------

    #1- Booking tables or pushing to waitlist if the table is already booked
    def book_tables(self,table_nbr):

        if table_nbr not in self.book_table: # If the table is available
            while True:
                customer_name = input("Enter your name: ").strip()
                if customer_name != "": # Checking that the name is not empty
                    self.book_table[table_nbr] = customer_name
                    print(f"Table {table_nbr} booked successfully under the name {customer_name}.")
                    break

                else:
                    print("Enter a valid name.")

        else: # If the table is booked, push to waitlist
            self.waitlist.append((table_nbr,customer_name))
            print(f"Table {table_nbr} already booked. You are now on the waitlist")

    #2- Cancelling a booked table
    def cancel_table(self,customer_name,table_nbr):

        # Checking for the name first, cancelling if available
        if customer_name in self.book_table.values():
            self.book_table.pop(table_nbr)
            print("Reservation cancelled.")

            # If any demands for that table match in the waitlist, push to booked tables
            if any(t[0] == table_nbr for t in self.waitlist): 
                self.book_tables[self.waitlist[0][0]] = self.waitlist[0][1]
                self.waitlist.remove((table_nbr,customer_name))
        else:
            print("Sorry, you haven't made a reservation.") 


    #3- Printing all reservations
    def print_table_reservations(self):
        print("Booked tables:")
        if self.book_table:
            for table_nbr in self.book_table:
                print(f"Table {table_nbr} booked by {self.book_table[table_nbr]}.")
        else:
            print("No reservations yet.") # If empty

    # ------------------------------------------------Orders------------------------------------------------

    #1- Taking an order
    def customer_order(self,table_nbr):

        # Checking if the table is availabke
        if table_nbr not in self.book_table:
            print("This table is not booked.")
            return
        
        # Input customer name
        customer_name=input("Enter your name: ").strip()
        order=[]
        total=0

        while True:
            # Asking for items of order one by one 
            suborder= input("Enter one item of your order or 0 to finish: ").strip

            # Exiting the loop
            if suborder == "0":
                break
            # Checking if the item chosen is in the menu
            elif suborder not in self.menu_items:
                print("This item is not available.")
            # If it is
            else:
                while True:
                    try:
                        # Asking for the quantity of one item
                        qty= int(input("How many?: "))
                        # Checking if it's positive
                        if qty<=0:
                            print("Enter a positive number: ")
                        else:
                            break
                    except ValueError:
                        print("Please enter a valid number.")

                # Adding the item and its quantity to the order
                order.append((suborder,qty))
                # Counting the total cost
                total += qty* self.menu_items[suborder]["price"]
                
        print(f"Order taken for {customer_name} at table {table_nbr}.Your total is: {total} DA")

        # Optional rating
        while True:
            choice = input("Do you want to rate us?(yes/no): ").strip().capitalize()
            if choice =="no":
                rating=0
                break
            elif choice=="yes":
                while True:
                    rating = float(input("Rate us out of 10: "))
                    if rating<0 or rating >10:
                        print("The rating should be from 0 to 10.")
                    else:
                        break
            else:
                print("Invalid choice. Please answer yes or no.")
            
        
        # Adding all the information to the customer's order
        self.customer_orders.append({
            "table":table_nbr,
            "customer": customer_name,
            "items":order,
            "total":total,
            "rating": rating
        })
                    
        # Incrementing total revenue
        self.total_revenue+= total
    
    # 2- Printing all orders
    def print_orders(self):
        
        # If the list of orders is empty
        if not self.customer_orders:
            print("No orders yet.")
            return
        
        print("Customer orders:")
        for order in self.customer_orders:
            print(f"\nTable: {order['table']}")
            print(f"Customer: {order['customer']}")
            print("Items:")
        for item, qty in order["items"]:
            price = self.menu_items[item]["price"]
            print(f"  - {item} x {qty} = {price * qty} DA")
            print(f"Total: {order['total']} DA")
            print(f"Rating: {order['rating']}/10")
    
    # 3- Sales report
    def sales_report(self):

        # If the list of orders is empty
        if not self.customer_orders:
            print("No orders yet.")
            return
        
        # New sales report dictionary 
        sales_report={}
        # Initializing grand total to 0
        grand_total=0

        # Looping through customer orders 
        for order in self.customer_orders:
            # Looping through items in orders
            for (item, qty) in order["items"]:
                price=self.menu_items[item]["price"]
                # Adding to the revenue
                revenue=qty*price

                # If the item isn't yet in the sales report
                if item not in sales_report:
                    # Adding it and initializing its values to 0
                    sales_report[item]={"qty":0,"revenue":0}

                # Updating quantity and revenue
                sales_report[item]["qty"]+= qty
                sales_report[item]["revenue"]+=revenue
                # Updating grand total
                grand_total+=revenue
                    
        # Printing sales report
        print("Sales report")
        for item,data in sales_report.item():
            print(f"{item}:{data["qty"]} sold,{data["revenue"]} DA")
        print(f"Grand total: {grand_total} DA")
            
# ------------------------------------------------Main------------------------------------------------

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
    ),
    "C" : lambda: my_restaurant.cancel_table(
        input("Enter your name: ").strip(),
        int(input("Enter table number: "))
    ),
    "D" : lambda: my_restaurant.customer_order(
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
        