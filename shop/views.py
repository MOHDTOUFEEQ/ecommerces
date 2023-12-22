from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.http.response import HttpResponse
from .models import Product
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView ,ListView , FormView , CreateView , DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from .models import CartItem
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
# Create your views here.

class index(ListView):
    model = Product
    template_name = "shop/index1.html"
    context_object_name = "products"


class product_detail(DetailView):
    model = Product
    template_name = "shop/product_detail.html"
    context_object_name = "product_data"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        related_products = Product.objects.filter(category=self.object.category).exclude(prod_id=self.object.prod_id)[:4]
        context['related_products'] = related_products
        return context
 # Use the appropriate login URL
def send(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        product_name = request.POST.get('product_name')
        num = request.POST.get('num')
        product_image = request.POST.get('product_image')
        price = request.POST.get('price')

        # Assuming you have a logged-in user (login_required decorator ensures this)
        user = request.user
        # Try to get the existing cart item, or create a new one if not found
        cart_item, created = CartItem.objects.get_or_create(user=user, product_name=product_name,image=product_image,price = price)

        # If the cart item exists, update the quantity
        if not created:
            cart_item.quantity += int(num)
            cart_item.save()

        response_data = {
            'message': 'Data received and stored in the cart successfully',
            'username': username,
            'product_name': product_name,
            'num': num,
        }

        return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'Please login to view the cart'})

from django.contrib.auth.forms import UserCreationForm
class signup(CreateView):
    form_class = UserCreationForm
    template_name = "shop/signup.html"  
    success_url = "/login"
    def get(self,request,*args,**kwargs):
        if self.request.user.is_authenticated:
           return redirect("page1.note")
        return super().get(request,*args,**kwargs)

class login(LoginView):
    template_name = "shop/login.html"  
    success_url = "/"
    def get(self, request , *args , **kwargs):
        if self.request.user.is_authenticated:
           return redirect("page1.note")
        return super().get(request,*args,**kwargs)
    
class logout(LogoutView):
    template_name = "shop/logout.html"  
    success_url = "/login"
    
def cart_list(request):
    # Fetch cart items for the logged-in user
    cart_items = CartItem.objects.filter(user=request.user)

    total_items = cart_items.count()

    for item in cart_items:
        item.total = item.price * item.quantity

    context = {
        'cart_items': cart_items,
        'total_items': total_items,
    }
    print("Server Response:", context)
    return render(request, 'shop/cart_list.html', context)

from django.core.serializers import serialize
def get_data(request):
    if request.method == "GET" and request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        total_items = cart_items.count()
        total_price = sum(item.price * item.quantity for item in cart_items)

        # Serialize cart items
        cart_items_serialized = serialize('json', cart_items)

        return JsonResponse({
            "total_items": total_items,
            "total_price": total_price,
            "cart_items": cart_items_serialized,
        }, safe=False)  # Set safe to False to allow serializing lists
    else:
        return JsonResponse({"error": "User not authenticated"}, status=403)
    

def delete_add_item(request):
    if request.method == "POST":
        product_name = request.POST.get("product_name")
        
        if product_name is not None:
            try:
                cart_item = CartItem.objects.get(product_name=product_name)
                cart_item.delete()
                return JsonResponse({"product_name": product_name})
            except CartItem.DoesNotExist:
                return JsonResponse({"error": f"Product with name {product_name} not found"}, status=404)
        else:
            return JsonResponse({"error": "Product name not provided"}, status=400)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)


def payment(request):   
    cart_items = CartItem.objects.filter(user = request.user)
    total_price = sum(item.price * item.quantity for item in cart_items)

    return render(request, "shop/payment.html",{"total_price": total_price})
from .models import UserAddress
class checkout(ListView):
    model = CartItem
    template_name = "shop/checkout.html"
    context_object_name = "data"

    def get_queryset(self):
        # Filter CartItem instances for the current user
        return CartItem.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        for item in context["object_list"]:
            item.total = item.price * item.quantity

        total_price = sum(item.price * item.quantity for item in context["data"])
        context["totalPrice"] = total_price
        
        return context
    
    def post(self, request, *args, **kwargs):
    # Extract user address information from the form
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        house = request.POST.get('house')
        postalcode = request.POST.get('postalcode')
        zip_code = request.POST.get('zip')
        message_to_seller = request.POST.get('message_to_seller')

        # Create a UserAddress instance and save it to the database
        user_address = UserAddress.objects.create(
            firstname=firstname,
            lastname=lastname,
            phone=phone,
            email=email,
            address=address,
            city=city,
            house=house,
            postalcode=postalcode,
            zip=zip_code,
            message_to_seller=message_to_seller
        )

        # Additional logic if needed

        # Clear the user's cart after completing the checkout

        return redirect('payment')
    

class PopularItemListView(ListView):
    model = CartItem  # Assuming you have a Product model
    template_name = "shop/popular_item.html"
    context_object_name = "data"

class newArrivals(ListView):
    model = Product  # Assuming you have a Product model
    template_name = "shop/newArrivals.html"
    context_object_name = "data"
    def get_queryset(self):
        # Order by the date_added field in descending order (most recent first)
        return Product.objects.order_by('-pub_date')[:10]

class Boys(ListView):
    model = Product  # Assuming you have a Product model
    template_name = "shop/boys.html"
    context_object_name = "data"
    def get_queryset(self):
        # Order by the date_added field in descending order (most recent first)
        return Product.objects.filter(category = "boys")

class girls(ListView):
    model = Product  # Assuming you have a Product model
    template_name = "shop/girls.html"
    context_object_name = "data"
    def get_queryset(self):
        # Order by the date_added field in descending order (most recent first)
        return Product.objects.filter(category = "girls")

class Electronics(ListView):
    model = Product  # Assuming you have a Product model
    template_name = "shop/Electronics.html"
    context_object_name = "data"
    def get_queryset(self):
        # Order by the date_added field in descending order (most recent first)
        return Product.objects.filter(category = "Electronics")

class Accessories(ListView):
    model = Product  # Assuming you have a Product model
    template_name = "shop/Accessories.html"
    context_object_name = "data"
    def get_queryset(self):
        # Order by the date_added field in descending order (most recent first)
        return Product.objects.filter(category = "accessories")


