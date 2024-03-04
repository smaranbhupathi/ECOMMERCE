from datetime import datetime

from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Contact, Orders, OrderUpdate, User, Admin, ProductReview, Address
# from mac.loginapp.models import UserModel

from math import ceil
import json
from django.db.models import Avg
from django.http import JsonResponse
from django.db.models import Q



# Create your views here.
from django.http import HttpResponse
#


def index(request):
    # pd = Product.objects.all()
    # print(pd)
    print(request.session)
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds':allProds}
    return render(request, 'shop/index.html', params)

def searchMatch(query, item):
    '''return true only if query matches the item'''
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False

def search(request):
    query = request.GET.get('search','')
    query = query.lower()
    print(query)
    # return HttpResponse("ok")
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]

        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds, "msg": ""}
    if len(allProds) == 0 or len(query)<3:
        params = {'msg': "Please make sure to enter relevant search query"}
    return render(request, 'shop/search.html', params)


def about(request):
    return render(request, 'shop/about.html')


def contact(request):
    if request.method=="POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
    return render(request, 'shop/contact.html')


def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                response = json.dumps([updates, order[0].items_json], default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')

    return render(request, 'shop/tracker.html')



# def productView(request, myid):
#
#     # Fetch the product using the id
#     product = Product.objects.filter(id=myid)
#     return render(request, 'shop/prodView.html', {'product':product[0]})


def checkout(request):
    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        amount = request.POST.get('amount', '')
        print(amount)
        order = Orders(items_json=items_json, shipfrom= request.session.get("username"), shipto=name, email=email, address=address, city=city,
                       state=state, zip_code=zip_code, phone=phone, amount = amount)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id
        return render(request, 'shop/checkout.html', {'thank':thank, 'id': id})
    try:
        request.session.get("username")
        addresses = Address.objects.filter(user=request.session.get("username"))
        return render(request, 'shop/checkout.html', {'addresses': addresses})
    except:
        return render(request, 'shop/login.html')

# def orders(request):
#     # Retrieve orders for the current user (filtered by shipfrom)
#     username = request.session.get("username", "")
#     user_orders = Orders.objects.filter(shipfrom=username)
#
#     # Loop through orders and modify item_json to include product.image
#     for order in user_orders:
#         print(type(order.items_json))
#         print(order.items_json)
#         order.items_json = json.loads(order.items_json)
#         print(type(order.items_json))
#         print(order.items_json)
#
#
#
#         for key, item_data in order.items_json.items():
#             product_id = key[2:]  # Assuming your product key is in the format "pr10", "pr11", etc.
#             product = Product.objects.get(id=product_id)
#             item_data.append(str(product.image))  # Add product.image URL to the item_data
#
#     # Pass the orders data to the template
#     context = {'orders': user_orders}
#     return render(request, 'shop/orders.html', context)


def orders(request):
    # Retrieve orders for the current user (filtered by shipfrom)
    username = request.session["username"]
    user_orders = Orders.objects.filter(shipfrom=username)
    # print(username)

    # Loop through orders and modify item_json to include product.image
    for order in user_orders:
        # print(type(order.items_json))
        # print(order.items_json)
        order.items_json = json.loads(order.items_json)
        # print(type(order.items_json))
        # print(order.items_json)



        for key, item_data in order.items_json.items():
            product_id = key[2:]  # Assuming your product key is in the format "pr10", "pr11", etc.
            product = Product.objects.get(id=product_id)
            item_data.append(str(product.image))  # Add product.image URL to the item_data
            rating = -1
            if ProductReview.objects.filter(product=product, username=username).exists():
                product_reviev  = ProductReview.objects.filter(product=product, username=username)[0]
                # print(product_reviev.product, product_reviev.rating)
                rating = product_reviev.rating
            # print(product_id, username)
            # print(product_reviev)
            item_data.append(rating)

    # Pass the orders data to the template
    context = {'orders': user_orders, 'len': len(user_orders)}
    return render(request, 'shop/orders.html', context)


def productView(request, myid):
    # Fetch the product using the id
    product = get_object_or_404(Product, id=myid)

    # Fetch product reviews including comments
    reviews = ProductReview.objects.filter(product=product)

    # Calculate average rating
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']

    return render(request, 'shop/prodView.html',
                  {'product': product, 'reviews': reviews, 'average_rating': average_rating})

def add_rating(request, order_id, product_key):
    if request.method == 'POST':
        # order = # Fetch the order based on order_id (if needed)
        product_id = int(product_key[2:])  # Extract product_id from "pr" + product_id
        product = get_object_or_404(Product, id=product_id)

        username = request.session["username"]  # Adjust this based on your authentication logic
        rating = int(request.POST.get('rating', 0))

        print(product, username, rating, "eee")
        # comment = "None"
        # if ProductReview.objects.filter(product=product, username=username).exists():
        #     if ProductReview.objects.filter(product=product, username=username)[0].comment:
        #         comment = ProductReview.objects.filter(product=product, username=username)[0]
        #     ProductReview.objects.filter(product=product, username=username)[0].delete()
        # pr = ProductReview()
        # pr.product = product
        # pr.username = username
        # pr.rating = rating
        # pr.comment = comment
        # pr.save()

        existing_review = ProductReview.objects.filter(product=product, username=username).first()

        if existing_review:
            # Update the existing ProductReview instance with a new comment
            existing_review.rating = rating
            existing_review.save()
        else:
            # Create a new ProductReview instance with a new comment
            pr = ProductReview(product=product, username=username, rating=rating)
            pr.save()

    return redirect('/orders')

def add_comment(request, order_id, product_key):
    if request.method == 'POST':

        product_id = int(product_key[2:])  # Extract product_id from "pr" + product_id
        product = get_object_or_404(Product, id=product_id)

        username = request.session.get("username")  # Adjust this based on your authentication logic
        comment_text = request.POST.get('comment', '')
        print("aaa")
        print(comment_text)

            # Check if a ProductReview instance exists for the given product and username
        existing_review = ProductReview.objects.filter(product=product, username=username).first()

        if existing_review:
            # Update the existing ProductReview instance with a new comment
            existing_review.comment = comment_text
            existing_review.save()
        else:
            # Create a new ProductReview instance with a new comment
            pr = ProductReview(product=product, username=username, comment=comment_text)
            pr.save()

    return redirect('/orders')


def search_recommendations(request):
    if request.method == 'GET':
        search_input = request.GET.get('search_input', '')
        if len(search_input)<2:
            return JsonResponse([], safe=False)
        print(search_input)

        # Perform a case-insensitive search on both product_name and category
        results = Product.objects.filter(
            Q(product_name__icontains=search_input)
        ).values('product_name')[:5]

        recommendations = [result['product_name'] for result in results]
        print(recommendations)

        return JsonResponse(recommendations, safe=False)
    else:
        return JsonResponse([], safe=False)


from django.shortcuts import redirect
def my_logout_page(request):
    if "username" in request.session:
        print(request.session["username"])
        request.session.clear()


    if "adminusername" in request.session:
        request.session.clear()
    return redirect("/login")


from django.shortcuts import render
from django.db.models import Count, Sum
from .models import Orders

def adminpage(request):
    if request.session["adminusername"]:
        # Calculate total number of unique ship_from values
        ship_from_count = Orders.objects.values('shipfrom').distinct().count()

        # Calculate total number of orders
        total_orders = Orders.objects.count()

        # Calculate total revenue
        # total_revenue = Orders.objects.aggregate(Sum('amount'))['amount__sum'] or 0

        context = {
            'ship_from_count': ship_from_count,
            'total_orders': total_orders,
            'total_revenue': 0,
        }

        return render(request, 'shop/adminpage.html', context)
    else:
        return redirect("/login/admin")



from django.shortcuts import render
from .models import Orders
import json

def allOrders(request):
    if request.session.get("adminusername"):
        # Fetch all orders in descending order of timestamp
        all_orders = Orders.objects.all().order_by('-timestamp')

        # Parse items_json to extract product names
        for order in all_orders:
            items_data = json.loads(order.items_json)
            product_names = [item_data[1] for item_data in items_data.values()]
            order.product_names = ', '.join(product_names)

        context = {
            'all_orders': all_orders,
        }

        return render(request, 'shop/allOrders.html', context)
    else:
        return redirect("/login/admin")


def addProductPage(request):
    return render(request, 'shop/addProduct.html', {})

def updateStatusPage(request):
    return render(request, 'shop/updateProduct.html', {})

from .models import Product


def addtoDB(request):
    if request.method == 'POST' and request.session.get("adminusername"):
        if request.method == 'POST':
            # Process the form data and save it to the database
            product_name = request.POST['product_name']
            category = request.POST['category']
            subcategory = request.POST['subcategory']
            price = request.POST['price']
            desc = request.POST['desc']
            pub_date_str = request.POST['pub_date']
            image = request.FILES.get('image', None)

            try:
                # Validate and convert pub_date to a datetime object
                pub_date = datetime.strptime(pub_date_str, "%Y-%m-%d").date()
            except ValueError:
                # Handle invalid date format
                return render(request, 'adminpage.html', {'error_message': 'Invalid date format'})

            # Check if required fields are filled correctly
            if not (product_name and category and price and desc and pub_date):
                return render(request, 'adminpage.html', {'error_message': 'All fields are required'})

            # Save the product to the database
            Product.objects.create(
                product_name=product_name,
                category=category,
                subcategory=subcategory,
                price=price,
                desc=desc,
                pub_date=pub_date,
                image=image
            )

        # Redirect to a success page or any other desired page
        return redirect('/adminpage/addProduct/?success=1')

    # Render the form or any other page if not a POST request
    return redirect('/login')

from django.utils import timezone
def updatecurrentStatus(request):
    if request.method == 'POST' and request.session.get("adminusername") :
        order_id = request.POST.get('order_id')
        update_desc = request.POST.get('update_desc')

        # Perform any additional validation if needed

        # Save the order update
        order_update = OrderUpdate(order_id=order_id, update_desc=update_desc, timestamp=timezone.now())
        order_update.save()

        # Redirect to a success page or the same page
        return redirect('/adminpage/updateStatus/?success=1')  # Adjust the URL name or use a specific URL

    return redirect('/login')


def address(request):
    username = request.session["username"]
    print(username)

    # Retrieve user details
    # user = UserModel.objects.get(username=username)

    # Retrieve all addresses for the given username
    addresses = Address.objects.filter(user=username)

    # for address in addresses:
    #     print(address.address_id)

    context = {'addresses': addresses}
    return render(request, 'shop/address.html', context)


def add_address(request):
    if request.method == 'POST':
        # Retrieve form data from POST request
        shipto = request.POST.get('shipto')
        email = request.POST.get('email')
        address_text = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')
        phone = request.POST.get('phone')


        # Create a new Address instance and save it to the database
        new_address = Address(
            shipto=shipto,
            email=email,
            address=address_text,
            city=city,
            state=state,
            zip_code=zip_code,
            phone=phone,
            user=request.session["username"]
        )
        new_address.save()

        return redirect('/profile/address')  # Adjust the redirect URL as needed

    return render(request, '/profile/address')


def delete(request, address_id):
    address = Address.objects.get(address_id=address_id)
    address.delete()
    return redirect('/profile/address')






