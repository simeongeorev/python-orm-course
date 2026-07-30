import os
import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Profile, Product, Order
from django.db.models import Q, F, Case, When, Value
from django.db.models.aggregates import Count


# Create queries within functions
# def populate_db():
#     # --- 1. Populate Profiles (2 records) ---
#     profile_1 = Profile.objects.create(
#         full_name="Alice Smith",
#         email="alice@example.com",
#         phone_number="+1234567890",
#         address="123 Main St, New York, NY",
#         is_active=True,
#     )
#
#     profile_2 = Profile.objects.create(
#         full_name="Bob Jones",
#         email="bob@example.com",
#         phone_number="+0987654321",
#         address="456 Oak Ave, Los Angeles, CA",
#         is_active=True,
#     )
#
#     # --- 2. Populate Products (2 records) ---
#     product_1 = Product.objects.create(
#         name="Wireless Ergonomic Mouse",
#         description="High-precision optical sensor with comfortable grip.",
#         price=Decimal("29.99"),
#         in_stock=50,
#         is_available=True,
#     )
#
#     product_2 = Product.objects.create(
#         name="Mechanical Gaming Keyboard",
#         description="RGB backlit keyboard with tactile mechanical switches.",
#         price=Decimal("89.99"),
#         in_stock=20,
#         is_available=True,
#     )
#
#     # --- 3. Populate Orders (2 records with relationships) ---
#     order_1 = Order.objects.create(
#         profile=profile_1,
#         total_price=Decimal("29.99"),
#         is_completed=True,
#     )
#     # Add Many-to-Many products to order 1
#     order_1.products.add(product_1)
#
#     order_2 = Order.objects.create(
#         profile=profile_2,
#         total_price=Decimal("119.98"),
#         is_completed=False,
#     )
#     # Add Many-to-Many products to order 2
#     order_2.products.add(product_1, product_2)
#
# if __name__ == "__main__":
#     populate_db()

def get_profiles(search_string=None) -> str:
    if search_string is None:
        return ""

    filtered_profiles = Profile.objects.filter(
        Q(full_name__icontains=search_string) |
        Q(email__icontains=search_string) |
        Q(phone_number__icontains=search_string)
    ).order_by('full_name')

    if not filtered_profiles.exists():
        return ""

    return "\n".join(f"Profile: {x.full_name},"
                     f" email: {x.email},"
                     f" phone number: {x.phone_number},"
                     f" orders: {x.order_set.count()}"
                     for x in filtered_profiles)


def get_loyal_profiles() -> str:
    filtered_profiles = Profile.objects.get_regular_customers()

    if not filtered_profiles.exists():
        return ""

    return "\n".join(
        f"Profile: {x.full_name}, orders: {x.order_set.count()}"
        for x in filtered_profiles
    )


def get_last_sold_products() -> str:
    last_order = Order.objects.order_by('creation_date').last()

    if not last_order:
        return ""

    products = last_order.products.order_by('name')

    if not products.exists():
        return ""

    product_names = [product.name for product in products]

    return f"Last sold products: {', '.join(product_names)}"


def get_top_products():
    most_sold_products = (Product.objects
                          .annotate(order_counts=Count('orders'))
                          .filter(order_counts__gt=0)
                          .order_by('-order_counts', 'name'))[:5]

    if not most_sold_products.exists():
        return ""

    result = "\n".join(f"{x.name}, sold {x.order_counts} times"
                       for x in most_sold_products)

    return f"Top products:\n{result}"


def apply_discounts():
    filtered_orders = (Order.objects
                       .annotate(products_count=Count('products'))
                       .filter(Q(products_count__gt=2) & Q(is_completed=False)))


    num_of_updated_orders = filtered_orders.update(total_price=F("total_price") * 0.9)

    return f"Discount applied to {num_of_updated_orders} orders."


def complete_order():
    first_order = Order.objects.order_by('creation_date').filter(is_completed=False).first()

    if not first_order:
        return ""

    first_order.is_completed = True

    Product.objects.filter(order=first_order).update(
        in_stock=F('in_stock') - 1,
        is_available=Case(
            When(in_stock=1, then=Value(False)),
            default=F('is_available')
        )
    )

    first_order.save()
    return "Order has been completed!"

# print(Profile.objects.get_regular_customers())
# print(get_profiles('Co'))
# print(get_profiles('9zz'))
# print(get_loyal_profiles())
# print(get_last_sold_products())
# print(get_top_products())
# print(apply_discounts())
# print(complete_order())
