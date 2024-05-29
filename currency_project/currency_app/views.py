from django.http import FileResponse
from django.shortcuts import render, redirect
from .forms import DateRangeForm, DataGraph
from .models import *
from .parsers import CurrencyParser
import matplotlib.pyplot as plt
def index(request):
    if request.method == "POST":
        form = DateRangeForm(request.POST)
        if form.is_valid() and "load_data" in request.POST:
            start_date = form.cleaned_data["start_date"]
            end_date = form.cleaned_data["end_date"]
            currency_code = form.cleaned_data["currency"]
            CurrencyParser.parse_countries()
            CurrencyParser.parse_rates(start_date, end_date, currency_code)
            countries = Country.objects.all()
            last_date = end_date
            exchange_rates = ExchangeRate.objects.filter(country=currency_code, date__gte=start_date, date__lte=end_date).order_by("date")
            currency_rates = CurrencyRate.objects.filter(code=currency_code, date__gte=start_date, date__lte=end_date).order_by("date")
            context = {
                "form": form,
                "countries": countries,
                "exchange_rates": exchange_rates,
                "currency_rates": currency_rates,
                "last_date": last_date,
            }
            return render(request, "currency_app/index.html", context)

    else:
        form = DateRangeForm()

    context = {
        "form": form,
        "countries": None,
        "exchange_rates": None,
        "currency_rates": None,
        "last_date": None,
    }

    return render(request, "currency_app/index.html", context)

def create_graph(request):
    if request.method == "POST":
        form = DataGraph(request.POST)
        if form.is_valid():
            date_list = []
            start_date = form.cleaned_data["start_date"]
            end_date = form.cleaned_data["end_date"]
            currencies = form.cleaned_data["currencies"]
            plt.figure(figsize=(12, 6))
            for currency_code in currencies:

                currency_list = ExchangeRate.objects.filter(country=currency_code, date__gte=start_date,
                                                            date__lte=end_date).order_by("date")
                if not (len(date_list)):
                    for element in currency_list:
                        date_list.append(element.date.strftime("%d.%m.%Y"))
                new_row = []
                for element in currency_list:
                    if element.date.strftime("%d.%m.%Y") in date_list:
                        new_row.append(element.relative_change)
                if len(new_row) < len(date_list):
                    new_row.extend([None] * (len(date_list) - len(new_row)))
                plt.plot(date_list, new_row, label=currency_code)
            plt.legend()
            plt.grid()
            plt.xticks(rotation=45,fontsize=8)
            plt.ylabel('Относительное изменение, %')
            plt.savefig('graph.png', dpi=100)
            plt.clf()

            context = {
                "graph_form": form,
                "graph_url": open("graph.png", 'rb')
            }
            return render(request, "currency_app/graph.html", context)

    else:
        form = DataGraph()
    context = {
        "graph_form": form,
    }
    return render(request, "currency_app/graph.html", context)

def graph_view(request):
    if (open('graph.png', 'rb')):
        return FileResponse(open('graph.png', 'rb'))
    else:
        return redirect("currency_app/graph.html")