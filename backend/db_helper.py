import mysql.connector
from contextlib import contextmanager
from logging_setup import setup_logger
logger = setup_logger('db_helper')


'''
what this really does is it is like a generator and when we call this method as it is done in side the fetch_all_records, 
fetch_expenses_for_date methods, it will basically call this method get_db_cursor and execute the statements till the yield cursor stmt.
once the methods fetch_all_records, fetch_expenses_for_date or any method that invokes this get_db_cursor method (which has the contextmanager annotation)
goes out of scope, then the statements post to the yield stmt will be executed and in our case it will be cursor , connection closing.
this maks the code reusable.

'''
@contextmanager
def get_db_cursor(commit=False):
    connection = mysql.connector.connect(host='localhost', user='root', password='sairam123', database='expense_manager')
    if connection.is_connected():
        print('Connection Successful')
    else:
        print('Failed in connection to a database')
        return None
    cursor = connection.cursor(dictionary=True)
    #return cursor, connection
    yield cursor
    if commit:
        connection.commit()
    cursor.close()
    connection.close()

def fetch_all_records():
    with get_db_cursor(commit=False) as cursor:
        cursor.execute('SELECT * FROM expenses')
        return cursor.fetchall()

def fetch_expenses_for_date(expense_date):
    logger.info(f'fetch_expenses_for_date  called with {expense_date}')
    with get_db_cursor(commit=False) as cursor:
        cursor.execute('SELECT * FROM expenses WHERE expense_date = %s', (expense_date,))
        result = cursor.fetchall()
        return result

def insert_expense(expense_date, amount, category, notes):
    logger.info(f'insert_expense  called with date: {expense_date}, amount: {amount}, category: {category}, notes: {notes}')
    with get_db_cursor(commit=True) as cursor:
        cursor.execute('INSERT INTO expenses (expense_date, amount, category, notes ) VALUES (%s, %s, %s,%s)',
                       (expense_date, amount, category, notes))
def delete_expense(expense_date):
    with get_db_cursor(commit=True) as cursor:
        cursor.execute('DELETE FROM expenses WHERE expense_date = %s', (expense_date,))

def fetch_expense_summary(start_date, end_date):
    logger.info(f'fetch_expense_summary called with start_date :{start_date}, end_date: {end_date}')
    with get_db_cursor(commit=False) as cursor:
        cursor.execute('SELECT category, SUM(amount) as total_expense_category_wise FROM expenses WHERE expense_date BETWEEN %s and %s GROUP BY category;', (start_date, end_date))
        result = cursor.fetchall()
        return result

def fetch_expense_month_wise():
    logger.info(f'fetch_expense_month_wise called ')
    with get_db_cursor(commit=False) as cursor:
        cursor.execute('''
        SELECT DATE_FORMAT(expense_date, '%Y-%m') AS month, SUM(AMOUNT) total_amount 
        FROM expenses
        GROUP BY DATE_FORMAT(expense_date, '%Y-%m')
        ORDER BY DATE_FORMAT(expense_date, '%Y-%m') ASC
        ''')
        result = cursor.fetchall()
        return result


if __name__ == '__main__':

    expenses = fetch_expenses_for_date('2024-08-01')
    insert_expense('2024-08-25', 40, 'Food', 'Samosa Chat')
    print(expenses)
    print(fetch_expense_summary('2024-08-01', '2024-12-25'))