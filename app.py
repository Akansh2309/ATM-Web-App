from flask import Flask, render_template, request, redirect, url_for, session, flash
import database
import banking
import os

app = Flask(__name__)
app.secret_key = 'super_secret_government_key'

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        card_number = request.form.get('card_number')
        pin = request.form.get('pin')
        user_id = database.authenticate_user(card_number, pin)
        if user_id:
            session['user_id'] = user_id
            session['card_number'] = card_number
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid Card Number or PIN.', 'error')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    accounts = database.get_accounts(session['user_id'])
    return render_template('dashboard.html', accounts=accounts, card_number=session['card_number'])

@app.route('/action/<action_type>', methods=['GET', 'POST'])
def action(action_type):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        amount = float(request.form.get('amount', 0))
        account_id = request.form.get('account_id')
        
        if action_type == 'withdraw':
            success, message = banking.withdraw(account_id, amount)
        elif action_type == 'deposit':
            success, message = banking.deposit(account_id, amount)
        elif action_type == 'transfer':
            target_account = request.form.get('target_account')
            success, message = banking.transfer(account_id, target_account, amount)
        elif action_type == 'tax':
            success, message = banking.pay_tax(account_id, amount)
        else:
            success, message = False, "Invalid action."
            
        if success:
            flash(message, 'success')
            return redirect(url_for('dashboard'))
        else:
            flash(message, 'error')
            
    accounts = database.get_accounts(session['user_id'])
    return render_template('action.html', action_type=action_type, accounts=accounts)

@app.route('/statement')
def statement():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    accounts = database.get_accounts(session['user_id'])
    transactions = []
    for acc in accounts:
        acc_txs = banking.get_statement(acc['id'], limit=50)
        for tx in acc_txs:
            tx['account_type'] = acc['account_type']
            transactions.append(tx)
    # Sort by timestamp desc
    transactions.sort(key=lambda x: x['timestamp'], reverse=True)
    return render_template('statement.html', transactions=transactions)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    if not os.path.exists('atm.db'):
        banking.setup_mock_data()
    app.run(debug=True)
