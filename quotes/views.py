from django.shortcuts import render, redirect
from .models import Stock
from django.contrib import messages
from .forms import StockForm
def home(request):
    import requests
    import json

    if request.method == 'POST':
        ticker = request.POST['ticker']
        #4X2TJF8AXGBR7UVC
        api_request = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol="+ticker.upper()+ "&interval=1min&apikey=4X2TJF8AXGBR7UVC")
        #api_request_overview = request.get('https://www.alphavantage.co/query?function=OVERVIEW&symbol=AAPL&apikey=4X2TJF8AXGBR7UVC')
        try:
            api = json.loads(api_request.content)
            #overview = json.loads(api_request_overview.content)
            company_name = api['Meta Data']['2. Symbol']
            latest_price = api['Time Series (1min)'][next(iter(api['Time Series (1min)']))]['4. close']
            previous_close = None
            count = 0
            for key in api['Time Series (1min)']:
                if(count==0):
                    count+=1
                    continue
                if previous_close is None:
                    previous_close = api['Time Series (1min)'][key]['4. close']
                else:
                    break
        except Exception as e:
            api = "Error..."
            ticker = "Error..."
            company_name = ""
            latest_price = ""
            previous_close = ""
        return render(request, 'home.html', {'api':api, 'company_name':ticker.upper(), 'latest_price':latest_price, 'previous_close':previous_close})
    else:
        return render(request, 'home.html', {'ticker':"Enter a Ticker Symbol Above"})




def about(request):
    return render(request, 'about.html', {})

def add_stock(request):
    import requests
    import json
    if request.method=='POST':
        form = StockForm(request.POST or None)

        if form.is_valid():
            form.save()
            messages.success(request, ("Stock has been added!"))
            return redirect('add_stock')
    else:
        ticker = Stock.objects.all()
        output = []
        for ticker_item in ticker:
            temp = []
            api_request = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol="+str(ticker_item).upper()+ "&interval=1min&apikey=4X2TJF8AXGBR7UVC")
            #api_request_overview = request.get('https://www.alphavantage.co/query?function=OVERVIEW&symbol=AAPL&apikey=4X2TJF8AXGBR7UVC')
            try:
                api = json.loads(api_request.content)
                temp.append(api)
                #overview = json.loads(api_request_overview.content)
                company_name = api['Meta Data']['2. Symbol']
                temp.append(company_name)
                latest_price = api['Time Series (1min)'][next(iter(api['Time Series (1min)']))]['4. close']
                temp.append('$'+latest_price)
                previous_close = None
                count = 0
                for key in api['Time Series (1min)']:
                    if(count==0):
                        count+=1
                        continue
                    if previous_close is None:
                        previous_close = api['Time Series (1min)'][key]['4. close']
                        temp.append('$'+previous_close)
                    else:
                        break
                output.append(temp)
            except Exception as e:
                api = "Error..."
                ticker = "Error..."
                company_name = ""
                latest_price = ""
                previous_close = ""
        return render(request, 'add_stock.html', {'ticker':ticker, 'output':output})

def delete(request, stock_id):
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request, ('Stock has been deleted!'))
    return redirect(delete_stock)

def delete_stock(request):
    ticker = Stock.objects.all()
    return render(request, 'delete_stock.html', {'ticker':ticker})
