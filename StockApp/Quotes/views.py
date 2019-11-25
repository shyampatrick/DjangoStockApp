from django.shortcuts import render, redirect
from datetime import datetime
from .models import Stock
from .forms import StockForm
from django.contrib import messages

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

def add_stock(request):
	import requests
	import json

	if request.method == 'POST':
		form = StockForm(request.POST or None)
		if form.is_valid():
			form.save()
			messages.success(request, ("Stock has been added"))
			return redirect('/Quotes/add_stock')

	else:
		ticker = Stock.objects.all()
		output = []
		for ticker_item in ticker:
			api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + str(ticker_item) + "/quote?token=pk_c2696c100d354a178ef31cfe812ca949")
			try:
				api = json.loads(api_request.content)
				output.append(api)
			except Exception as e:
				api = "Error"
		
		return render(request, 
				'Quotes/add_stock.html', 
				{	
					'output': output,
					'ticker': ticker,
					'year':datetime.now().year,
				})


def delete(request, stock_id):
	item = Stock.objects.get(pk=stock_id)
	item.delete()
	messages.success(request, ('Stock deleted'))
	return redirect('/Quotes/delete_stock')


def delete_stock(request):
	ticker = Stock.objects.all()
	return render(request, 
			'Quotes/delete_stock.html', 
			{	
				'ticker': ticker,
				'year':datetime.now().year,
			})



