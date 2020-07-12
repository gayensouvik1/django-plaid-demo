# django-plaid-demo
In this project, we integrate django with plaid for fetching transaction history and account details.

### Prerequisites
* Python 3.x
* Install django
  - **$ python -m pip install Django**
* Install ngrok
  - **$ brew cask install ngrok**
  
### Getting Started
Open a terminal and run
1. **$ git clone https://github.com/gayensouvik1/django-plaid-demo.git**
2. Open *bright/view.py* and replace the values of *public_key*,*client_id* & *secret* defined in https://dashboard.plaid.com/overview/sandbox. Change value of *webhook_url* as mentioned in step 5
3. **$ cd django-plaid-demo**
4. **$ python3 manage.py runserver**
5. Open another terminal and run **$ ngrok http 8000**. Here find the http url cooresponding to Session Status:Forward and replace the domain of *webhook_url* in *bright/view.py*.
6. Now open a browser and go to <webhook_url>/login
