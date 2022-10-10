from cs50 import SQL
from sys import argv
import csv

db = SQL("sqlite:///students.db")

if len(argv) != 2:
    print("wrong usage")
    exit(0)
    
with open(argv[1]) as studentsData:
    reader = csv.reader(studentsData)
    next(reader)
    
    for row in reader:
        name = row[0].split(' ')
         
        if len(name) < 3:
            db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES(?, ?, ?, ?, ?)",
                               name[0], None, name[1], row[1], row[2])
        else:
             db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES(?, ?, ?, ?, ?)",
                               name[0], name[1], name[2], row[1], row[2])
