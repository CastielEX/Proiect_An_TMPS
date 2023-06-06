import requests
import json

BASE_URL = "http://localhost:5000/"

# Creational Design Patterns

# Singleton
class StoreClient:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(StoreClient, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.base_url = BASE_URL

# Factory Method
class APIRequestFactory:
    @staticmethod
    def create_request(url, method, data=None):
        if method == 'GET':
            return GetRequest(url)
        elif method == 'POST':
            return PostRequest(url, data)
        elif method == 'PATCH':
            return PatchRequest(url, data)
        elif method == 'DELETE':
            return DeleteRequest(url)

class GetRequest:
    def __init__(self, url):
        self.url = url

    def send(self):
        return requests.get(self.url)

class PostRequest:
    def __init__(self, url, data):
        self.url = url
        self.data = data

    def send(self):
        return requests.post(self.url, json=self.data)

class PatchRequest:
    def __init__(self, url, data):
        self.url = url
        self.data = data

    def send(self):
        return requests.patch(self.url, json=self.data)

class DeleteRequest:
    def __init__(self, url):
        self.url = url

    def send(self):
        return requests.delete(self.url)

# Structural Design Patterns

# Adapter
class CategoryAdapter:
    def __init__(self, category):
        self.category = category

    def display(self):
        print(f"{self.category['title']} (ID: {self.category['id']})")
        print(self.category['description'])

# Decorator
class CategoryDecorator:
    def __init__(self, category):
        self.category = category

    def display(self):
        self.category.display()
        self.additional_info()

    def additional_info(self):
        print("Additional information...")

# Behavioral Design Patterns

# Observer
class CategoryObserver:
    def update(self, category):
        print(f"Category updated: {category['title']}")

class ObservableCategory:
    def __init__(self):
        self.observers = []

    def attach(self, observer):
        self.observers.append(observer)

    def detach(self, observer):
        self.observers.remove(observer)

    def notify(self, category):
        for observer in self.observers:
            observer.update(category)

# Strategy
class CategoryListStrategy:
    def __init__(self, request):
        self.request = request

    def list_categories(self):
        response = self.request.send()
        if response.ok:
            categories = json.loads(response.content)
            for category in categories:
                adapter = CategoryAdapter(category)
                adapter.display()
                print()
        else:
            print(f"Error fetching categories: {response.status_code}")

class CategoryStrategyContext:
    def __init__(self, strategy):
        self.strategy = strategy

    def list_categories(self):
        self.strategy.list_categories()

class ProductAdapter:
    def __init__(self, product):
        self.product = product

    def display(self):
        print(f"{self.product['name']} (ID: {self.product['id']}, Price: {self.product['price']})")
        print(self.product['description'])

# API Functions

def list_categories():
    url = f"{BASE_URL}/categories"
    request = APIRequestFactory.create_request(url, 'GET')
    strategy = CategoryListStrategy(request)
    context = CategoryStrategyContext(strategy)
    context.list_categories()

def show_category(category_id):
    url = f"{BASE_URL}/categories/{category_id}"
    request = APIRequestFactory.create_request(url, 'GET')
    response = request.send()
    if response.ok:
        category = json.loads(response.content)
        adapter = CategoryAdapter(category)
        adapter.display()
    else:
        print(f"Error fetching category: {response.status_code}")

def create_category(title, description):
    url = f"{BASE_URL}/categories"
    data = {'title': title, 'description': description}
    request = APIRequestFactory.create_request(url, 'POST', data)
    response = request.send()
    if response.ok:
        category = json.loads(response.content)
        print(f"Category created with ID: {category['id']}")
    else:
        print(f"Error creating category: {response.status_code}")

def delete_category(category_id):
    url = f"{BASE_URL}/categories/{category_id}"
    request = APIRequestFactory.create_request(url, 'DELETE')
    response = request.send()
    if response.ok:
        print("Category deleted")
    else:
        print(f"Error deleting category: {response.status_code}")

def change_category_title(category_id, new_title):
    url = f"{BASE_URL}/categories/{category_id}"
    data = {'title': new_title}
    request = APIRequestFactory.create_request(url, 'PATCH', data)
    response = request.send()
    if response.ok:
        print("Category title updated")
    else:
        print(f"Error updating category title: {response.status_code}")

def create_product(category_id, name, price, description):
    url = f"{BASE_URL}/categories/{category_id}/products"
    data = {'name': name, 'price': price, 'description': description}
    request = APIRequestFactory.create_request(url, 'POST', data)
    response = request.send()
    if response.ok:
        product = json.loads(response.content)
        print(f"Product created with ID: {product['id']}")
    else:
        print(f"Error creating product: {response.status_code}")

def list_products(category_id):
    url = f"{BASE_URL}/categories/{category_id}/products"
    request = APIRequestFactory.create_request(url, 'GET')
    response = request.send()
    if response.ok:
        products = json.loads(response.content)
        for product in products:
            adapter = ProductAdapter(product)
            adapter.display()
            print()
    else:
        print(f"Error fetching products: {response.status_code}")

# Usage
store_client = StoreClient()

while True:
    print("1. List categories")
    print("2. Show category details")
    print("3. Create a category")
    print("4. Delete a category")
    print("5. Change category title")
    print("6. Create a product")
    print("7. List products in a category")
    print("0. Exit")
    choice = input("Enter your choice: ")

    if choice == '1':
        list_categories()
    elif choice == '2':
        category_id = input("Enter category ID: ")
        show_category(category_id)
    elif choice == '3':
        title = input("Enter category title: ")
        description = input("Enter category description: ")
        create_category(title, description)
    elif choice == '4':
        category_id = input("Enter category ID: ")
        delete_category(category_id)
    elif choice == '5':
        category_id = input("Enter category ID: ")
        new_title = input("Enter new category title: ")
        change_category_title(category_id, new_title)
    elif choice == '6':
        category_id = input("Enter category ID: ")
        name = input("Enter product name: ")
        price = float(input("Enter product price: "))
        description = input("Enter product description: ")
        create_product(category_id, name, price, description)
    elif choice == '7':
        category_id = input("Enter category ID: ")
        list_products(category_id)
    elif choice == '0':
        break
    else:
        print("Invalid choice. Please try again.")
