from locust import HttpUser, between, task
import random
import pymysql as p
import pymysql.cursors

def random_user_id():
    return random.randint(0,100000)

class twincity_info:
    def connect(self):
        connection =  p.connect(host="localhost", user="root", password="", database="twincitiesautoauctions", charset='utf8mb4')
        return connection.cursor(pymysql.cursors.DictCursor)

    # def fetch_user_info(self):
    #     cursor = self.connect()
    #     try:
    #         cursor.execute("SELECT * FROM manage_customer WHERE ")

class locust_test(HttpUser):
    wait_time = between(1, 3)
    host = "http://192.168.1.184:9000"
    used_user_id = set()

    # @task
    def user_registration(self):
        user_email = self.generate_random_email()
        # payload_string = f"registrationtabno=5&account_type=Individual public buyer&email={user_email}&confirm_email_id={user_email}&password=Test@123&confirm_password=Test@123&firstname=userf&middlename=userf&lastname=userf&gender=Male&date_of_birth=&phonecode=1&primary_phone=&phonecode2=1&secondary_phone=&address=&city=&county=&state=&zipcode=&country=&latitude=41.30213612&longitude=-72.63419727&seller_access=disable&license_numbere=&license_expirationdate=&car_insurance=&policy_number=&expirationdate=&driverlicense=5c8b65f1dab64d4c9dee22809649a4ce.jpeg&dealer_license=&file_2license=&same_as_personl_address=1&billingaddress=Opening+Hill+Rd&billingcountry=India&billingcity=Ahmedabad&billingstate=Connecticut&billing_zip=06437"
        if user_email !="":
            payload = {
                "registrationtabno": "5",
                "account_type" : "Individual public buyer",
                "email": user_email,
                "confirm_email_id": user_email,
                "password" : "Test@123",
                "confirm_password" : "Test@123",
                "firstname": "userf",
                "middlename": "userm",
                "lastname": "userl",
                "gender": "Male",
                "date_of_birth": "07/20/2021",
                "phonecode": "77",
                "primary_phone": "25644212225",
                "phonecode2": "1",
                "secondary_phone": "25644212225",
                "address": "Opening Hill Rd",
                "city": "Ahmedabad",
                "county": "Gujarat",
                "state": "Connecticut",
                "zipcode": "6437",
                "country": "India",
                "latitude": "41.30213612",
                "longitude": "-72.63419727",
                "seller_access": "disable",
                "license_numbere": "776455412313",
                "license_expirationdate": "08/31/2026",
                "car_insurance": "Cyblance Technologies",
                "policy_number": "4645131321",
                "expirationdate": "10/31/2027",
                "driverlicense": "5c8b65f1dab64d4c9dee22809649a4ce.jpeg",
                "dealer_license": "",
                "file_2license": "",
                "same_as_personl_address": "1",
                "billingaddress": "Nehru Bridge Road",
                "billingcountry": "India",
                "billingcity": "Ahmedabad",
                "billingstate": "Gujrat",
                "billing_zip": "10001"
            }
            self.client.post("/registration", data=payload)
        else:
            pass

    def generate_random_email(self):
        while True:
            u_id = random_user_id()
            if(u_id not in self.used_user_id):
                self.used_user_id.add(u_id)
                return f"user{u_id}@example.com"

    def pre_bid_single(self):
        user_id = random.randint(0,24)
        payload = {
            "add-bid": "add-bid",
            "type" : "pre bid",
            "user_id" : user_id,
            "auction_id" : "5",
            "inventory_id": "30",
            "reserve_price": "5450000.0",
            "bid_type": "single bid",
            "bid_amount": "",
            "get_single_bid":"",
            "get_max_bid":"",
            "current_win_user":"",
            "current_bid_amount":""
        }
        # /bidding/add-user-vehicle-bid