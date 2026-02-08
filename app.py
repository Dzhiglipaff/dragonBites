from flask import Flask, jsonify, request, render_template, session
import dataQuery
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/", methods=["GET", "POST"])
def index():
    # Initialize session filters if not exists
    if 'filters' not in session:
        session['filters'] = []
    
    # Handle AJAX JSON requests for filter updates
    if request.is_json:
        filters = request.get_json().get('filters', [])
        session['filters'] = filters
        session.modified = True
        
        # Create query with all active filters
        b = dataQuery.booleanQuery()
        
        if 'dragonDollars' in session['filters']:
            b.usesDragonDollars()
        if 'diningDollars' in session['filters']:
            b.usesDiningDollars()
        if 'card' in session['filters']:
            b.takesCard()
        if 'cash' in session['filters']:
            b.takesCash()
        
        restaurants = b.executeQueries()
        return jsonify({'restaurants': restaurants})
    
    # Handle regular page load
    # Create query with all active filters
    b = dataQuery.booleanQuery()
    
    if 'dragonDollars' in session['filters']:
        b.usesDragonDollars()
    if 'diningDollars' in session['filters']:
        b.usesDiningDollars()
    if 'card' in session['filters']:
        b.takesCard()
    if 'cash' in session['filters']:
        b.takesCash()
    
    restaurants = b.executeQueries()
    
    return render_template("website2.html", restaurants=restaurants, active_filters=session['filters'])

if __name__ == "__main__":
    app.run(debug=True)