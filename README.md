# Clockify API
This is a simple app to work with https://clockify.me/developers-api <br/>
# Installation <br/>
`Install requirements:` <br/>
1. Simply run  pip install -r requirements.txt (or pip3 install -r requirements.txt if you're on linux) <br/>
2. Clone repository: <br/>
git clone https://github.com/lyyubava/clockifyAPI <br/>
3. cd clockifyAPI<br/>

`Add your X_API_KEY in configuration.py` <br/>
# Overview
To get json responses, just create an instance of class GetJsonData in module processing_requests.py and use all methods to serve your needs:) <br/>
To get 'more readable' info create an instance of class GetInfo in module processing_requests.py and also use any methods to get required information.<br/>
To view your data in more convenient way create an instance of class Analyzes in anlyzing_tasks.py module. To see analyzable info about task just call 
show_df_grouped_by_total_time() method of the class
