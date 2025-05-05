from django.shortcuts import render, get_object_or_404, redirect
from .models import User, Dish, Order
from .forms import UserForm, DishForm, OrderForm


def home(request):
    return render(request, 'home.html', {
        'users_count': User.objects.count(),
        'dishes_count': Dish.objects.count(),
        'orders_count': Order.objects.count()
    })

def users_list(request):
    users = User.objects.all()
    return render(request, 'users_list.html', {'users': users})

def dishes_list(request):
    dishes = Dish.objects.all()
    return render(request, 'dishes_list.html', {'dishes': dishes})

def orders_list(request):
    orders = Order.objects.all()
    return render(request, 'orders_list.html', {'orders': orders})

def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order_detail.html', {
        'order': order,
        'user': order.user,
        'dish': order.dish
    })

def user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user_orders = user.orders.all()
    return render(request, 'user_detail.html', {
        'user': user,
        'orders': user_orders
    })

def dish_detail(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    dish_orders = dish.orders.all()
    return render(request, 'dish_detail.html', {
        'dish': dish,
        'orders': dish_orders
    })

# User CRUD operations
def user_create(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users_list')
    else:
        form = UserForm()
    return render(request, 'user_form.html', {'form': form})

def user_update(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_detail', user_id=user.id)
    else:
        form = UserForm(instance=user)
    return render(request, 'user_form.html', {'form': form, 'user': user})

def user_delete(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('users_list')
    return render(request, 'user_confirm_delete.html', {'user': user})

# Dish CRUD operations
def dish_create(request):
    if request.method == 'POST':
        form = DishForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dishes_list')
    else:
        form = DishForm()
    return render(request, 'dish_form.html', {'form': form})

def dish_update(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    if request.method == 'POST':
        form = DishForm(request.POST, instance=dish)
        if form.is_valid():
            form.save()
            return redirect('dish_detail', dish_id=dish.id)
    else:
        form = DishForm(instance=dish)
    return render(request, 'dish_form.html', {'form': form, 'dish': dish})

def dish_delete(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    if request.method == 'POST':
        dish.delete()
        return redirect('dishes_list')
    return render(request, 'dish_confirm_delete.html', {'dish': dish})

# Order CRUD operations
def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('orders_list')
    else:
        form = OrderForm()
    return render(request, 'order_form.html', {'form': form})

def order_update(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('order_detail', order_id=order.id)
    else:
        form = OrderForm(instance=order)
    return render(request, 'order_form.html', {'form': form, 'order': order})

def order_delete(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        order.delete()
        return redirect('orders_list')
    return render(request, 'order_confirm_delete.html', {'order': order})