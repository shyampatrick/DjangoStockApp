from django.shortcuts import render
from datetime import datetime

# Create your views here.
def Quotes(request):
	import requests
	import json

	if request.method == 'POST':
		ticker = request.POST['ticker']
		api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + ticker + "/quote?token=pk_c2696c100d354a178ef31cfe812ca949")

		try:
			api = json.loads(api_request.content)
		except Exception as e:
			api = "Error"

		return render(request, 
			'Quotes/index.html', 
			{									   
				'year':datetime.now().year,
				'api':api
			})

	else:
		return render(request, 
			'Quotes/index.html', 
			{	
				'ticker': 'Search for quotes: Enter ticker in the search field above',
				'year':datetime.now().year,
			})



