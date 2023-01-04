## Importing CSV files into DataGrip
1. Open DataGrip and connect to your database.

2. Go to File > Import Data, or right-click on the target schema in the Database pane and select Import Data.

3. Select the CSV file type and browse for the CSV file you want to import.

4. Choose the target schema and table for the import, or create a new table.

5. Specify the CSV file options, such as the field delimiter, quote character, and encoding.

6. Preview the data to verify the import, and click Import to start the process.

7. Wait for the import to complete, and check the results in the Messages pane.

## Running the Python file
1. Make sure you have Python, MySQL, and the required libraries installed.
2. Set the database connection parameters in the code, such as the host, port, username, and password. You can modify the following lines to specify your 
'''SQL
MySQL credentials:

Copy code
# Define mydb Connection
mydb = mysql.connector.connect(user='root',
                               password='Rja181029!',
                               host='localhost',
                               database='sportsodds')
cursor = mydb.cursor()
Run the Python file by using the following command:
Copy code
python filename.py
'''
3. Wait for the code to execute, and follow the prompts to select an option from the menu.


