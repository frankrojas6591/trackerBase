# ===== app.py (Main Flask Application) =====
"""
Expense Tracker - Complete Flask App with Microservices
For PythonAnywhere deployment
"""
# ===== MICROSERVICE: EXPENSE SERVICE =====
class ExpenseService:
    @staticmethod
    def get_all_expenses(user_id=None):
        expenses = load_json(EXPENSES_FILE)
        if user_id:
            expenses = [e for e in expenses if e['user_id'] == user_id]
        return sorted(expenses, key=lambda x: x['date'], reverse=True)
    
    @staticmethod
    def get_expense(expense_id):
        expenses = load_json(EXPENSES_FILE)
        return next((e for e in expenses if e['id'] == expense_id), None)
    
    @staticmethod
    def create_expense(user_id, category, amount, description, date):
        expenses = load_json(EXPENSES_FILE)
        
        expense = {
            'id': max([e['id'] for e in expenses], default=0) + 1,
            'user_id': user_id,
            'category': category,
            'amount': float(amount),
            'description': description,
            'date': date,
            'created_at': datetime.now().isoformat()
        }
        expenses.append(expense)
        save_json(EXPENSES_FILE, expenses)
        return {'success': True, 'expense': expense}
    
    @staticmethod
    def update_expense(expense_id, category, amount, description, date):
        expenses = load_json(EXPENSES_FILE)
        
        for expense in expenses:
            if expense['id'] == expense_id:
                expense['category'] = category
                expense['amount'] = float(amount)
                expense['description'] = description
                expense['date'] = date
                expense['updated_at'] = datetime.now().isoformat()
                save_json(EXPENSES_FILE, expenses)
                return {'success': True, 'expense': expense}
        
        return {'success': False, 'message': 'Expense not found'}
    
    @staticmethod
    def delete_expense(expense_id):
        expenses = load_json(EXPENSES_FILE)
        expenses = [e for e in expenses if e['id'] != expense_id]
        save_json(EXPENSES_FILE, expenses)
        return {'success': True}
    
    @staticmethod
    def get_statistics(user_id):
        expenses = ExpenseService.get_all_expenses(user_id)
        
        if not expenses:
            return {'total': 0, 'count': 0, 'by_category': {}}
        
        total = sum(e['amount'] for e in expenses)
        by_category = {}
        
        for expense in expenses:
            cat = expense['category']
            if cat not in by_category:
                by_category[cat] = 0
            by_category[cat] += expense['amount']
        
        return {
            'total': total,
            'count': len(expenses),
            'by_category': by_category
        }

