# from locust import HttpUser, between, task

# class MyUser(HttpUser):
#     wait_time = between(1, 3)
#     host = "http://localhost:5000"

#     @task
#     def hello_world(self):
#         self.client.get("/")

from locust import HttpUser, between, task
import random

class RegistrationUser(HttpUser):
    wait_time = between(1, 3)
    host = "http://localhost:5000"
    user_id = random.randint(0,100)

    @task
    def register_user(self):
        payload = {
            "username": self.generate_random_username(),
            "email": self.generate_random_email(),
            "password": "Test@123"
        }
        self.client.post("/register", data=payload)

    def generate_random_username(self):
        return "user_" + str(self.user_id)

    def generate_random_email(self):
        return f"user{self.user_id}@example.com"
