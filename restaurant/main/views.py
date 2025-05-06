from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from .models import User, Dish, Order
from .forms import UserForm, DishForm, OrderForm, LoginForm, RegisterForm

# Authentication views
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            try:
                # Try to find user by email (assuming username field contains email)
                user = User.objects.get(email=username)
                if user.check_password(password):
                    # Successful login
                    request.session['user_id'] = user.id
                    return redirect('home')
                else:
                    form.add_error(None, "Invalid username or password")
            except User.DoesNotExist:
                form.add_error(None, "Invalid username or password")
    else:
        form = LoginForm()
    
    context = {
        'form': form,
        'current_user': get_current_user(request),
        'is_admin': is_admin(request)
    }
    return render(request, 'login.html', context)

def logout_view(request):
    # Clear the session
    if 'user_id' in request.session:
        del request.session['user_id']
    return redirect('home')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.role = 'customer'  # Default role is customer
            user.save()
            
            # Auto login after registration
            request.session['user_id'] = user.id
            return redirect('home')
    else:
        form = RegisterForm()
    
    return render(request, 'register.html', {'form': form})

# Helper functions
def get_current_user(request):
    user_id = request.session.get('user_id')
    if user_id:
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
    return None

def is_admin(request):
    user = get_current_user(request)
    return user and user.role == 'admin'

def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not get_current_user(request):
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not is_admin(request):
            return HttpResponseForbidden("Access denied. Admin privileges required.")
        return view_func(request, *args, **kwargs)
    return wrapper

# Home view - accessible to all
def home(request):
    context = {
        'users_count': User.objects.count(),
        'dishes_count': Dish.objects.count(),
        'orders_count': Order.objects.count(),
        'current_user': get_current_user(request),
        'is_admin': is_admin(request)
    }
    return render(request, 'home.html', context)

# User management views - admin only
@admin_required
def users_list(request):
    users = User.objects.all()
    context = {
        'users': users,
        'current_user': get_current_user(request),
        'is_admin': is_admin(request)
    }
    return render(request, 'users_list.html', context)

@admin_required
def user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user_orders = user.orders.all()
    context = {
        'user': user,
        'orders': user_orders,
        'current_user': get_current_user(request),
        'is_admin': is_admin(request)
    }
    return render(request, 'user_detail.html', context)

@admin_required
def user_create(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Set a default password for users created by admin
            user.set_password('changeme')
            user.save()
            return redirect('users_list')
    else:
        form = UserForm()
    context = {
        'form': form,
        'current_user': get_current_user(request),
        'is_admin': is_admin(request)
    }
    return render(request, 'user_form.html', context)

@admin_required
def user_update(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_detail', user_id=user.id)
    else:
        form = UserForm(instance=user)
    context = {
        'form': form, 
        'user': user,
        'current_user': get_current_user(request),
        'is_admin': is_admin(request)
    }
    return render(request, 'user_form.html', context)

@admin_required
def user_delete(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('users_list')
    context = {
        'user': user,
        'current_user': get_current_user(request),
        'is_admin': is_admin(request)
    }
    return render(request, 'user_confirm_delete.html', context)

# Dish management views - view for all, create/edit/delete for admin only
def dishes_list(request):
    dishes = Dish.objects.all()
    context = {
        'dishes': dishes,
        'current_user': get_current_user(request),
        'is_admin': is_admin(request)
    }
    return render(request, 'dishes_list.html', context)

def dish_detail(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    dish_orders = dish.orders.all() if is_admin(request) else []
    context = {
        'dish': dish,
        'orders': dish_orders,
        'current_user': get_current_user(request),
        'is_admin': is_admin(request)
    }
    return render(request, 'dish_detail.html', context)

@admin_required
def dish_create(request):
    if request.method == 'POST':
        form = DishForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dishes_list')
    else:
        form = DishForm()
    context = {
        'form': form,
        'current_user': get_current_user(request),
        'is_admin': is_admin(request)
    }
    return render(request, 'dish_form.html', context)

@admin_required
def dish_update(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    if request.method == 'POST':
        form = DishForm(request.POST, instance=dish)
        if form.is_valid():
            form.save()
            return redirect('dish_detail', dish_id=dish.id)
    else:
        form = DishForm(instance=dish)
    context = {
        'form': form, 
        'dish': dish,
        'current_user': get_current_user(request),
        'is_admin': is_admin(request)
    }
    return render(request, 'dish_form.html', context)

@admin_required
def dish_delete(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    if request.method == 'POST':
        dish.delete()
        return redirect('dishes_list')
    context = {
        'dish': dish,
        'current_user': get_current_user(request),
        'is_admin': is_admin(request)
    }
    return render(request, 'dish_confirm_delete.html', context)

# Order management views
@login_required
def orders_list(request):
    if is_admin(request):
        # Admins can see all orders
        orders = Order.objects.all()
    else:
        # Customers see only their orders
        current_user = get_current_user(request)
        orders = Order.objects.filter(user=current_user)
    
    context = {
        'orders': orders,
        'current_user': get_current_user(request),
        'is_admin': is_admin(request)
    }
    return render(request, 'orders_list.html', context)

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    current_user = get_current_user(request)
    
    # Check permissions
    if not is_admin(request) and order.user.id != current_user.id:
        return HttpResponseForbidden("You don't have permission to view this order.")
    
    context = {
        'order': order,
        'user': order.user,
        'dish': order.dish,
        'current_user': current_user,
        'is_admin': is_admin(request)
    }
    return render(request, 'order_detail.html', context)

@login_required
def order_create(request):
    current_user = get_current_user(request)
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # If customer, force their user ID
            if not is_admin(request):
                order = form.save(commit=False)
                order.user = current_user
                order.save()
            else:
                form.save()
            return redirect('orders_list')
    else:
        initial_data = {}
        if not is_admin(request):
            initial_data = {'user': current_user.id}
        
        form = OrderForm(initial=initial_data)
        
        # If customer, disable user field
        if not is_admin(request):
            form.fields['user'].disabled = True
    
    context = {
        'form': form,
        'current_user': current_user,
        'is_admin': is_admin(request)
    }
    return render(request, 'order_form.html', context)

@login_required
def order_update(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    current_user = get_current_user(request)
    
    # Only admin or the order owner can update
    if not is_admin(request) and order.user.id != current_user.id:
        return HttpResponseForbidden("You don't have permission to update this order.")
    
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            # If customer, ensure they can't change user
            if not is_admin(request):
                updated_order = form.save(commit=False)
                updated_order.user = current_user
                updated_order.save()
            else:
                form.save()
            return redirect('order_detail', order_id=order.id)
    else:
        form = OrderForm(instance=order)
        # If customer, disable user field
        if not is_admin(request):
            form.fields['user'].disabled = True
    
    context = {
        'form': form, 
        'order': order,
        'current_user': current_user,
        'is_admin': is_admin(request)
    }
    return render(request, 'order_form.html', context)

@login_required
def order_delete(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    current_user = get_current_user(request)
    
    # Only admin or the order owner can delete
    if not is_admin(request) and order.user.id != current_user.id:
        return HttpResponseForbidden("You don't have permission to delete this order.")
    
    if request.method == 'POST':
        order.delete()
        return redirect('orders_list')
    
    context = {
        'order': order,
        'current_user': current_user,
        'is_admin': is_admin(request)
    }
    return render(request, 'order_confirm_delete.html', context)