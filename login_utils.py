import sqlite3


def authenticate(uname,pword):
    connection = sqlite3.connect("login.db")
    c = connection.cursor()
    ans = c.execute('SELECT * FROM logins where username = "' + uname + '" and password = "' + pword + '";')
    for r in ans:
        print 1
        return True
    print 0
    return False

def create_user(uname,pword):
    connection = sqlite3.connect("login.db")
    c = connection.cursor()
    ans = c.execute('SELECT * FROM logins where username = "' + uname + '";')
    for r in ans:
        return False
    ans = c.execute('INSERT INTO logins values("' + uname + '", "' + pword + '");')
    connection.commit()
    return True

        
#create_user("asdf@gmail.com", "asdfasdf")


#if authenticate("asdf@gmail.com", "asdfasdf"):
#    print "authenticate works"
#if authenticate("zcva@gmail.com", "asdxzaqwe") == False:
#    print "did not authenticate because not created account"
