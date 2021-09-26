import dbcreds
import mariadb

conn = None
cursor = None

try:
    conn = mariadb.connect(
                        user=dbcreds.user,
                        password=dbcreds.password, 
                        host=dbcreds.host, 
                        port=dbcreds.port, 
                        database=dbcreds.database,
                        )
    cursor = conn.cursor()

    tryAgain = True
    while True:
        print("Please type in your username:")
        username_input = input()
        if not username_input:
            print("Error: Please input a valid username")
            continue
        else:
            break

    while True:
        print("You have 3 choices: \n1.Write a new post \n2.See all other posts \n3.Exit application")
        userChoice = int(input())
        
        if (userChoice == 1):
            print("Please type content")
            usr_content_input = input()
            try:
                cursor.execute("INSERT INTO blog_post(username, content) VALUES(?, ?)", [username_input, usr_content_input])
            except mariadb.DataError:
                print("Something wrong with your data")
            except mariadb.OperationalError:
                print("Operational error on query")
            if(cursor.rowcount == 1):
                print("Update sucessful")
                conn.commit()
            else:
                print("Failed to update")
        elif (userChoice == 2):
            cursor.execute("SELECT username FROM blog_post")
            user_list = cursor.fetchall()
            print("There are ", cursor.rowcount, " users!")
            for usr in user_list:
                print(usr)
        elif (userChoice == 3):
            break
        else:
            print("Error, please input either 1 or 2")
            continue
    
except mariadb.DataError:
    print("Something wrong with your data")
except mariadb.OperationalError: #Creating already existing table falls under OperationalError
    print("Something wrong with the connection")
except mariadb.ProgrammingError:
    print("Your query was wrong")
except mariadb.IntegrityError:
    print("Your query would have broken the database")
except:
    print("Something went wrong")

finally:
    if (cursor != None):
        cursor.close()
    else:
        print("Cursor was never opened, nothing to close here.")
    if (conn != None):
        conn.close()
    else:
        print("Connection was never opened, nothing to close here.")