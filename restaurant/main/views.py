from django.shortcuts import render, get_object_or_404

# Sample fixed data (keep existing data)
USERS = [
    {'id': 1, 'name': 'John Doe', 'email': 'john@example.com'},
    {'id': 2, 'name': 'Jane Smith', 'email': 'jane@example.com'}
]

DISHES = [
    {'id': 1, 'name': 'Pizza', 'price': 10.99, 'description': 'Cheese pizza'},
    {'id': 2, 'name': 'Burger', 'price': 8.50, 'description': 'Classic burger'}
]

ORDERS = [
    {'id': 1, 'user_id': 1, 'dish_id': 1, 'status': 'pending'},
    {'id': 2, 'user_id': 2, 'dish_id': 2, 'status': 'completed'}
]

def home(request):
    return render(request, 'home.html', {
        'users_count': len(USERS),
        'dishes_count': len(DISHES),
        'orders_count': len(ORDERS)
    })

def users_list(request):
    return render(request, 'users_list.html', {'users': USERS})

def dishes_list(request):
    return render(request, 'dishes_list.html', {'dishes': DISHES})

def orders_list(request):
    return render(request, 'orders_list.html', {'orders': ORDERS})

def order_detail(request, order_id):
    # Find the specific order
    order = next((order for order in ORDERS if order['id'] == order_id), None)
    
    if order:
        # Find associated user and dish
        user = next((user for user in USERS if user['id'] == order['user_id']), None)
        dish = next((dish for dish in DISHES if dish['id'] == order['dish_id']), None)
        
        return render(request, 'order_detail.html', {
            'order': order,
            'user': user,
            'dish': dish
        })
    
    # Handle case where order is not found
    return render(request, 'order_detail.html', {'error': 'Order not found'})

def user_detail(request, user_id):
    # Find the specific user
    user = next((user for user in USERS if user['id'] == user_id), None)
    
    if user:
        # Find orders for this user
        user_orders = [order for order in ORDERS if order['user_id'] == user_id]
        
        return render(request, 'user_detail.html', {
            'user': user,
            'orders': user_orders
        })
    
    # Handle case where user is not found
    return render(request, 'user_detail.html', {'error': 'User not found'})

def dish_detail(request, dish_id):
    # Find the specific dish
    dish = next((dish for dish in DISHES if dish['id'] == dish_id), None)
    
    if dish:
        # Find orders for this dish
        dish_orders = [order for order in ORDERS if order['dish_id'] == dish_id]
        
        return render(request, 'dish_detail.html', {
            'dish': dish,
            'orders': dish_orders
        })
    
    # Handle case where dish is not found
    return render(request, 'dish_detail.html', {'error': 'Dish not found'})