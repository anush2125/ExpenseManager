from fastapi import FastAPI, HTTPException
from datetime import date
from typing import List
import db_helper
from pydantic import BaseModel

app = FastAPI()

class Expense(BaseModel):
    amount: float
    category: str
    notes: str

class DateRange(BaseModel):
    start_date : date
    end_date: date

@app.get('/expenses/{expense_date}', response_model=List[Expense])
def get_expenses(expense_date: date):
    return db_helper.fetch_expenses_for_date(expense_date)

@app.post('/expenses/{expense_date}')
def add_or_update_expense(expense_date: date, expenses: List[Expense]):
    db_helper.delete_expense(expense_date)
    for expense in expenses:
        db_helper.insert_expense(expense_date, expense.amount, expense.category, expense.notes)

    return {'message': 'Expenses updated successfully'}

@app.post('/analytics')
def get_analytics(date_range: DateRange):
    data = db_helper.fetch_expense_summary(date_range.start_date, date_range.end_date)
    if data is None:
        raise HTTPException(status_code=500, detail='failed to retrieve expense summary from the db')
    total = sum([ row['total_expense_category_wise'] for row in data])
    breakdown = {}
    for row in data:
        pct = (row['total_expense_category_wise']/total)*100 if total != 0 else 0
        breakdown[row['category']] = {'total' : row['total_expense_category_wise'], 'percentage' : pct}
    return breakdown

@app.get('/analytics/month')
def get_analytics_month_based():
    data = db_helper.fetch_expense_month_wise()
    if data is None:
        raise HTTPException(status_code=500, detail='failed to retrieve expense summary month wise from the db')
    total_expense_all_month = sum([row['total_amount'] for row in data])
    breakdown = {}
    for row in data:
        pct = (row['total_amount']/total_expense_all_month)*100 if total_expense_all_month != 0 else 0
        breakdown[row['month']] = {'total_month_wise' : row['total_amount'], 'percentage_month': pct}
    return breakdown