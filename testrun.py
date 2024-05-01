from twinlocustfile import locust_test
from locust.env import Environment

# Create an instance of the locust_test class
locust_instance = locust_test(environment=Environment())

# Call the method on the instance
response_text = locust_instance.get_live_auction_details()

# Print the response text
print(response_text)