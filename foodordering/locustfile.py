from locust import HttpUser, task, between

class QuickStart(HttpUser):
    wait_time = between(2,5)

    def __int__(self):
        self.token = None
        self.username = None

    def on_start(self):
        self.login()
        self.logout()

    '''
    Load Test on User Login API.
    '''
    def login(self):
        login_data = {
            "username" : "harsha-mangena",
            "password" : "qwertyuiop"
        }

        response = self.client.post("login/", json=login_data)
        self.token = response.json()['access']
        self.username = response.json()['user']

    '''
    Lod Test on User Logout API
    '''
    def logout(self):
        response = self.client.get("logout/", headers={"Authorization": "Bearer " + self.token},)


    '''
    Load Test on listing all stores API
    Permission : Merchant
    '''
    @task 
    def view_stores_list(self):
        response = self.client.get("stores/", headers={"Authorization": "Bearer " + self.token},)

    
    '''
    Load Test on listing all orders API
    Permission : Merchant | Users
    '''
    @task
    def view_orders_list(self):
        response = self.client.get("orders/", headers={"Authorization": "Bearer " + self.token}, )

    
    '''
    Load Test on listing all items API
    Permission : Merchant 
    '''
    @task
    def view_items_list(self):
        response = self.client.get("items/", headers = {"Authorization" : "Beared "+ self.token}, )


    '''
    Load Test on listing all Users API
    Permission : Admin
    '''
    @task
    def view_user_list(self):
        response = self.client.get("users/", headers={"Authorization" : "Beared "+ self.token}, )


    '''
    Load Test on listing all Merchants API
    Permission : Admin
    '''
    @task 
    def view_merchant_list(self):
        response = self.client.get("merchants/", headers = {"Authorization" : "Beared" + self.token}, )
    
    

