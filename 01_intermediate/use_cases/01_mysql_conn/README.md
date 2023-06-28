# Connect to MySQL

This code does the following:
- establishes a connection to the MySQL server, 
- creates a cursor object, 
- executes a SELECT query to retrieve all rows from a table, 
- fetches the resultset, 
- and then iterates over the rows to print the data. 
- Finally, it closes the cursor and the database connection.

Replace following text with actual values:
- `your_host`
- `your_username`
- `your_password`
- `your_database`

## To Clone the code on Unix

```shell
mkdir /tmp/code; cd /tmp/code
git clone git@gitlab.nonprod.mt.oh.transformco.com:kkoneru/learn-python-scripting-basics.git
```

## To setup Virtual environment on Unix

```shell
mkdir -p /tmp/venv
virtualenv -p python3 01_mysql_conn.venv
cd /tmp/venv/01_mysql_conn.venv
source bin/activate
cd /tmp/code/learn-python-scripting-basics/01_intermediate/use_cases/01_mysql_conn
pip install -r requirements.txt
deactivate
```

## To run the code

```shell
source /tmp/venv/01_mysql_conn.venv/bin/activate
python /tmp/code/learn-python-scripting-basics/01_intermediate/use_cases/01_mysql_conn/app.py
deactivate
```

