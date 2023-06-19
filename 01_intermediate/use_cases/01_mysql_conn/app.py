import pymysql.cursors

# Connect to the MySQL server
cnx = pymysql.connect(
    host='your_host',
    user='your_username',
    password='your_password',
    database='your_database',
    cursorclass=pymysql.cursors.DictCursor
)

# Create a cursor object to interact with the database
cursor = cnx.cursor()

# Execute a query to select data from a table
query = "SELECT * FROM your_table limit 5"
cursor.execute(query)

# Fetch all the rows from the resultset
rows = cursor.fetchall()

# Iterate over the rows and print the data
for row in rows:
    print(row)

# Close the cursor and the database connection
cursor.close()
cnx.close()
