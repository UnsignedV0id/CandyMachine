from cs50 import SQL
from sys import argv

db = SQL("sqlite:///students.db")

if len(argv) != 2:
    print("wrong usage")
    exit(0)
    

student = db.execute("SELECT first, middle, last , birth FROM students WHERE house == (?) ORDER BY last ASC, first ASC ", argv[1] )
for dictionary in student:
    print(f"{dictionary['first']} {dictionary['middle'] + ' ' if dictionary['middle'] != None else '' }{dictionary['last']}, born {dictionary['birth']}")