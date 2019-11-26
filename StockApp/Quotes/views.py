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

def singlepage_delete(request, stock_id):
	item = Stock.objects.get(pk=stock_id)
	item.delete()
	messages.success(request, ('Stock deleted'))
	return redirect('/Quotes/singlepage')

def singlepage_addstock(request):
	form = StockForm(request.POST or None)
	if form.is_valid():
		form.save()
		messages.success(request, ("Stock has been added"))
		return redirect('/Quotes/singlepage')

def singlepage(request):
	import requests
	import json

	ticker_list = Stock.objects.all()
	favorites = []
	for ticker_item in ticker_list:
		api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + str(ticker_item) + "/quote?token=pk_c2696c100d354a178ef31cfe812ca949")
		try:
			stock_info_fav = json.loads(api_request.content)
			favorites.append(stock_info_fav)
		except Exception as e:
			api = "Error"

	if request.method == 'POST':
		search_ticker = request.POST['ticker']
		api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + search_ticker + "/quote?token=pk_c2696c100d354a178ef31cfe812ca949")
		try:
			stock_info = json.loads(api_request.content)
		except Exception as e:
			stock_info = "Error"
		return render(request, 
			'Quotes/singlepage.html', 
			{	
				'ticker_list': ticker_list,
				'favorites': favorites,
				'stock_info': stock_info,
				'year':datetime.now().year,
			})
	else:
		stock_info = ''
		return render(request, 
			'Quotes/singlepage.html', 
			{	
				'ticker_list': ticker_list,
				'favorites': favorites,
				'stock_info': stock_info,
				'year':datetime.now().year,
			})



