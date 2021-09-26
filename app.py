import dbcreds
import mariadb

conn = None
cursor = None

def addContent():
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

def lookupUsers():
    cursor.execute("SELECT content FROM blog_post")
    post_list = cursor.fetchall()
    print("There are ", cursor.rowcount, " users!")
    for posts in post_list:
        print(posts)

def checkLoginCreds(usrname, password):
    cursor.execute("SELECT username, password FROM users WHERE username=?",[usrname])
    getUserInfo = cursor.fetchone()
    #check inputs against database
    if (getUserInfo[0] == usrname and getUserInfo[1] == password):
        print("Login Successful")
    else:
        print("Incorrect username/password combination")
    cursor.close()
    conn.close()
try:
    conn = mariadb.connect(
                        user=dbcreds.user,
                        password=dbcreds.password, 
                        host=dbcreds.host, 
                        port=dbcreds.port, 
                        database=dbcreds.database,
                        )
    cursor = conn.cursor()

    #Run login code
    user_input_name = input("Input username: ")
    user_input_pw = input("Input password: ")
    checkLoginCreds(user_input_name, user_input_pw)
    
    tryAgain = True
    while True:
        print("Please type in your username:")
        username_input = input()
        if not username_input:
            raise ValueError
        else:
            break

    while True:
        print("You have 3 choices: \n1.Write a new post \n2.See all other posts \n3.Exit application")
        userChoice = int(input())
        
        if (userChoice == 1):
            addContent()
        elif (userChoice == 2):
            lookupUsers()
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
except ValueError:
    print("Please input a username")
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