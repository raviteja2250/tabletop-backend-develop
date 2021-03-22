import json

from locust import HttpUser, task

from tabletop_backend.settings import base as settings


class CustomerLoadTest(HttpUser):
    def __init__(self, *args, **kwargs):
        self.token = ''
        self.headers = {}
        super(CustomerLoadTest, self).__init__(*args, **kwargs)

    @task
    def check_public_endpoint(self):
        # Public endpoints that app uses
        self.client.get("/api/brands")
        self.client.get("/api/menu-items")
        self.client.get("/api/categories")
        self.client.get("/api/chefs")
        self.client.get("/api/chef-posts")
        self.client.get("/api/chef-media")
        self.client.get("/api/chef-post-tags")
        self.client.get("/api/chef-recipes")
        self.client.get("/api/promotions")
        self.client.get("/api/special-items")
        self.client.get("/api/tags")
        self.client.get("/api/fees")
        self.client.get("/api/discounts")

    @task
    def check_user_endpoint(self):
        # Endpoint bases on user token
        self.client.get("/api/favorite-items", headers=self.headers)
        self.client.get("/api/chef-followers", headers=self.headers)

    @task
    def check_place_order_endpoint(self):
        # Endpoint bases on user token
        self.client.post("/api/orders", headers=self.headers, json={  # Should change the id base on server we want to test
            "order_items": [
                {"menu_item": 2, "price": 1, "quantity": 2},
                {"menu_item": 3, "price": 1, "quantity": 2}
            ],
            "discount": 8,
            "brand": 2,
            "table_no": 1,
            "type": "dine_in"
        })

    def on_start(self):
        self.token = self.get_token()
        self.headers = {'Authorization': 'Bearer ' + self.token}

    def get_token(self):
        response = self.client.post(
            "/auth/otp", json={"phone_number": settings.DEMO_USER['phone_number'], "confirmation_code": settings.DEMO_USER['otp']})  # This is demo user

        return json.loads(getattr(response, 'content', {})).get('access', '')
