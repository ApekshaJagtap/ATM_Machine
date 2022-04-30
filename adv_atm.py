from time import strftime,gmtime,ctime
import mysql.connector

# ....connection to database
conn = mysql.connector.connect(user='root', password='Apps@0303', host='localhost', database='adv_atm')
cur=conn.cursor()

# s="CREATE TABLE users(user_id integer(4), card_num integer(12), balance integer(10)),user_name varchar(20)"
# cur.execute(s)

# s="INSERT INTO users VALUES(%s, %s, %s, %s)"
# b=[(1,123456,10000,'Apeksha Jagtap'),(2,234567,25000,'Sayali Mule'),(3,345678,6700,'Rohit Pagar')]
# cur.executemany(s,b)
# conn.commit()


print("\t\t\t\t\t Welcome to ATM machine")
class atm:
    try:
        # ........method to withdraw money
        list = []
        def withdraw(self):
            try:
                s = "SELECT * FROM users"
                cur.execute(s)
                result = cur.fetchall()
                for rec in result:
                    self.amount = int(input("Enter your amount: "))
                    if self.amount < 0:
                        print("Oops! Negative amount cannot withdraw.")
                    elif self.amount == 0:
                        print("Oops! Zero amount cannot withdraw.")
                    elif self.amount <= rec[3]:
                        self.balance = rec[3] - self.amount
                        s = "UPDATE users SET balance=%s WHERE card_num=%s"
                        b = (self.balance, card_number)
                        cur.execute(s, b)
                        conn.commit()
                        t = strftime("%d %b %Y %H:%M", gmtime())
                        atm.list.append([self.amount, t, "Debited"])
                        print(f"Successfully debited {format(self.amount, ',.2f')} Rs. from your current account.")
                        print(f"Current balance is {format(self.balance, ',.2f')} Rs.\n")
                    else:
                        print("Insufficient balance!")
                    break
            except:
                print("Please enter valid amount!")

        def credit_amount(self):
            # ..........method to credit money
            try:
                s="SELECT * FROM users"
                cur.execute(s)
                result=cur.fetchall()
                for rec in result:
                    self.amount = int(input("Enter your amount: "))
                    self.balance = rec[3] + self.amount
                    s="UPDATE users SET balance=%s WHERE card_num=%s"
                    b=(self.balance,card_number)
                    cur.execute(s,b)
                    conn.commit()
                    print(f"Successfully credited {format(self.amount, ',.2f')} Rs. to your account.")
                    print(f"Current balance is {format(self.balance, ',.2f')} Rs.\n")
                    t = strftime("%d %b %Y %H:%M", gmtime())
                    atm.list.append([self.amount, t, "Credited"])
                    break
            except:
                print("Please enter valid amount!")
    except:
        print("Error!")

try:
    choise = int(input(" Select 1: Register 2: Login "))
    if choise==1:
        # .......registration for new user
        card_num=int(input("Enter your 6-digit card number: "))
        s = "SELECT * FROM users"
        cur.execute(s)
        result = cur.fetchall()
        for rec in result:
            if card_num ==rec[1]:
                print("Enter valid card number!Card number already exists.")
                break
            else:
                user_name = input("Enter your first and last name: ")
                pin = int(input("Set pin for your account: "))
                conf_pin = int(input("Confirm pin: "))
                balance = int(input("Enter balance in your account: "))
                if pin == conf_pin:
                    s = "INSERT INTO users  VALUES(%s,%s,%s,%s)"
                    b = (user_name, card_num, pin, balance)
                    cur.execute(s,b)
                    conn.commit()
                    print("Sucessfully registered.")
                else:
                    print("Please enter valid pin!")
                break
    elif choise==2:
        # ...........log in
        card_num=int(input("Enter your card number: "))
        s="SELECT * FROM users"
        cur.execute(s)
        result=cur.fetchall()
        for rec in result:
            if card_num==rec[1] :
                card_number=rec[1]
                password=rec[2]
                name=rec[0]
                pin=int(input("Enter pin:"))
                while pin == rec[2]:
                    try:
                        print(f" Welcome {name}..")
                        print("1.Credit Money\n2.Withdraw Money\n3.Balance Enquiry\n4.Mini Statement\n5.Pin Change\n6.Quit")
                        option = int(input("\nSelect 1,2,3,4,5 or 6: "))
                        print()
                        obj = atm()
                        if option == 1:
                            obj.credit_amount()
                        elif option == 2:
                            obj.withdraw()
                        elif option == 3:
                            s = "SELECT * FROM users WHERE card_num=%s AND atm_pin=%s"
                            b=(card_number,password)
                            cur.execute(s,b)
                            result = cur.fetchall()
                            for rec in result:
                                print(f"Available Balance: Rs.{rec[3]}\n")
                        elif option == 4:
                            print("\t\tMini Statement")
                            print(f'''{strftime("%d %b %Y %H:%M", gmtime())}''')
                            print(f"CARD NO.{card_number}")
                            for i in range(len(atm.list)):
                                print(f'''{atm.list[i][1]} \t {atm.list[i][0]}Rs. {atm.list[i][2]}\n''')
                        elif option == 5:
                            try:
                                current_pin = int(input("Enter Current Pin :"))
                                for rec in result:
                                    while current_pin == rec[2]:
                                        try:
                                            new_pin = int(input("Enter New Pin: "))
                                            confirm_pin = int(input("Confirm New Pin: "))
                                            if new_pin == confirm_pin:
                                                s="UPDATE users SET atm_pin=%s WHERE card_num=%s"
                                                b=(new_pin,card_number)
                                                cur.execute(s,b)
                                                conn.commit()
                                                print("Your pin has been changed successfully!\n")
                                                try:
                                                    f = open("pass.txt", "w")
                                                    f.write(f"Your Current Pin is {pin}")
                                                    f.close()
                                                except:
                                                    print("ahaaaa")
                                                try:
                                                    pin_num = int(input("Enter new pin: "))
                                                except:
                                                    print("Invalid pin!")
                                                break
                                            else:
                                                print("Pin didnt match try again!")
                                        except:
                                            print("Enter valid pin")
                                    else:
                                        print("Invalid current pin!")

                            except:
                                print("Enter valid pin!")
                        elif option == 6:
                            pass
                            print("\nThanks for visiting!")
                            break
                        else:
                            print("Please select valid option.")
                    except:
                        print("Please select valid option...")
                else:
                    print("Invalid pin!")
except:
    print("Enter valid input")



