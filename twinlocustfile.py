from locust import HttpUser, between, task
import random
from infodatabase import twincity_info

# run command
# locust -f twinlocustfile.py --web-host=127.0.0.1 --web-port=8888

def random_user_id():
    return random.randint(1,100000)

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

    # @task
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

    @task
    def get_live_auction_details(self):
        user_id = random.randint(1,24)
        payload = {
            "auction_id": "6",
            "user_id": user_id,
            "livebid": "livebid"
        }
        response = self.client.post("/bidding/get-live-bidding",data=payload)
        # return response.text
        if response.status_code == 200:
            auction_details = response.json()
            # print(auction_details)
            choice = random.choice([0,1])
            if choice == 1:
                self.live_bid_single(auction_details,user_id)
            else:
                self.live_bid_max(auction_details,user_id)
            return ({'auction_details':auction_details,'current_user_id':user_id})

    def live_bid_single(self,auction_details,current_user_id):
        data = auction_details.get("data")
        user_id = data['user_id']
        inventory_extend_time = auction_details.get("inventory_extend_time")
        bid_history = auction_details.get("user_bid_history")

        # Get the latest bid amount
        latest_bid_amount = bid_history[-1]['bid_amount'] if bid_history else 0
        payload = {
            "customer_id": current_user_id,
            "progressbar_count": 30000,
            "bid_type": "single bid",
            "live-bid": "live-bid",
            "inventory_id":inventory_extend_time['id'],
            "type": "live bid",
            "user_id": current_user_id,
            "auction_id": 6,
            "extend_time": 15,
            "duration_time": 300,
            "auto_extend_time": 15,
            "reserve_price": inventory_extend_time['reserve_price'],
            "get_single_bid": latest_bid_amount,
            "get_max_bid": 0,
            "current_win_user":user_id,
            "current_bid_amount":data['bid_amount'],
            "bid_amount":data['bid_amount']+50,
            "bid_amount":data['bid_amount']+50
        }
        # print(payload)
        response = self.client.post('/bidding/live-vehicle-bid-user-add',data=payload)
        # print("this is response:",response.text)

    def live_bid_max(self,auction_details,current_user_id):
        data = auction_details.get("data")
        user_id = data['user_id']
        inventory_extend_time = auction_details.get("inventory_extend_time")
        bid_history = auction_details.get("user_bid_history")
        max_bid_amount = max([bid['bid_amount'] for bid in bid_history]) if bid_history else 0
        payload = {
            "customer_id": current_user_id,
            "progressbar_count": 30000,
            "bid_type": "max bid",
            "live-bid": "live-bid",
            "inventory_id":inventory_extend_time['id'],
            "type": "live bid",
            "user_id": current_user_id,
            "auction_id": 6,
            "extend_time": 15,
            "duration_time": 300,
            "auto_extend_time": 15,
            "reserve_price": inventory_extend_time['reserve_price'],
            "get_single_bid": max_bid_amount,
            "get_max_bid": 0,
            "current_win_user":user_id,
            "bid_amount":data['bid_amount']+50,
            "bid_amount":data['bid_amount']+50
        }
        # print(payload)
        response = self.client.post('/bidding/live-vehicle-bid-user-add',data=payload)
        # print("this is response:",response.text)