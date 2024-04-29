from locust import HttpUser, between, task
import random
from infodatabase import twincity_info

def random_user_id():
    return random.randint(0,100000)

class locust_test(HttpUser):
    wait_time = between(1, 3)
    host = "http://127.0.0.1:9000"
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
            
    @task
    def pre_bid_task(self):
        choice = random.choice([0,1])
        if choice == 0:
            self.pre_bid_single()
        else:
            self.pre_bid_max()

    def pre_bid_single(self):
        inventory_id=30
        user_id = random.randint(1,24)
        bid_info = twincity_info.get_current_bid(inventory_id)
        current_bid_amt = bid_info['bid_amount']
        bid_amount = random.randrange(start=(int(current_bid_amt)+50),stop=None)
        if bid_amount>current_bid_amt:
            winning_bid = twincity_info.get_winning_user(inventory_id)
            payload = {
                "add-bid": "add-bid",
                "type" : "pre bid",
                "user_id" : user_id,
                "auction_id" : "5",
                "inventory_id": "30",
                "reserve_price": "5450000.0",
                "bid_type": "single bid",
                "bid_amount": bid_amount,
                "get_single_bid":bid_amount,
                "get_max_bid":"0",
                "current_win_user":winning_bid,
                "current_bid_amount":current_bid_amt
            }
            self.client.post("/bidding/add-user-vehicle-bid",data=payload)
        else:
            pass
        
    def pre_bid_max(self):
        inventory_id=30
        user_id = random.randint(1,24)
        bid_info = twincity_info.get_current_bid(inventory_id)
        current_bid_amt = bid_info['bid_amount']
        bid_amount = random.randrange(start=(int(current_bid_amt)+50),stop=None)
        if bid_amount>current_bid_amt:
            winning_bid = twincity_info.get_winning_user(inventory_id)
            payload = {
                "add-bid": "add-bid",
                "type" : "pre bid",
                "user_id" : user_id,
                "auction_id" : "5",
                "inventory_id": "30",
                "reserve_price": "5450000.0",
                "bid_type": "max bid",
                "bid_amount": bid_amount,
                "get_single_bid":"0",
                "get_max_bid":bid_amount,
                "current_win_user":winning_bid,
                "current_bid_amount":current_bid_amt
            }
            self.client.post("/bidding/add-user-vehicle-bid",data=payload)
        else:
            pass