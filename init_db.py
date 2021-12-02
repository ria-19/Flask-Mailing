'''
To initialise the birthday database
'''

import sqlite3

conn = sqlite3.connect('./birthdays.db')

with open('birthdays.sql') as f:
	conn.executescript(f.read())

conn.close()