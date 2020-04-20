#%% Libraries   
from django.shortcuts import render
from datetime import datetime

from constance import config

from history.charts import ChartHistory
from history.models import HistoryMin,HistoryUur,HistoryDag,HistoryMaand,HistoryJaar

#%% Settings
chart_colour_elec_in = "rgb(242, 186, 15)"
chart_colour_elec_out = "rgb(152, 208, 35)"
chart_colour_gas = "rgb(80, 122, 191)"

#%% General functions
# get data sets
def get_dataset(chart_data={},chart_label='no label',chart_backgroundColor='rgba(255,187,205,1)'):
    return{
        'label': chart_label,
        'data': chart_data,
        'backgroundColor': chart_backgroundColor,
        'borderWidth': 2,
        'borderColor': "rgb(150, 150, 150)",
    }

#%% Views   
def history_chart_elec(request,timestep):    
    # settings
    messages = ""
    datatype = "electricity"

    # get items from request
    dict_items = {}
    if request.method == 'GET':
        for key, value in request.GET.items():
            if key != 'csrfmiddlewaretoken':
                dict_items[key] = value

    elif request.method == 'POST':
        for key, value in request.POST.items():
            if key != 'csrfmiddlewaretoken':
                dict_items[key] = value 
    
    # unpack request items
    dict_types = {}
    for key, value in dict_items.items():
        dict_types[key] = type(value)  
    
    # plot data and settings based on timestep of data
    chart_label = str(timestep)+'ly data'
    if timestep=='minute':
        Dataplot = HistoryMin
        chart_unit = 'hour'
    elif timestep=='hour':
        Dataplot = HistoryUur
        chart_unit = 'day'
    elif timestep=='day':
        Dataplot = HistoryDag
        chart_label = 'daily data'
        chart_unit = 'week'
    elif timestep=='month':
        Dataplot = HistoryMaand
        chart_unit = 'month'
    elif timestep=='year':
        Dataplot = HistoryJaar
        chart_unit = 'year'
    
    # query data
    if ('tmin' in dict_items.keys()) & ('tmax' in dict_items.keys()):
        date_min = datetime.strptime(dict_items['tmin'],'%Y-%m-%d')
        date_max = datetime.strptime(dict_items['tmax'],'%Y-%m-%d')          
    else:
        date_min = datetime.strptime('2000-01-01','%Y-%m-%d')
        date_max = datetime.strptime('2100-01-01','%Y-%m-%d')          
    records = Dataplot.objects.filter(timestamp__range=(date_min,date_max))

    # get current date range
    date_min_records = records.earliest('timestamp').timestamp.strftime('%Y-%m-%d')
    date_max_records = records.latest('timestamp').timestamp.strftime('%Y-%m-%d')

    # subset data to plot
    if ('n_records_max' in dict_items.keys()):
        n_records_max = int(dict_items['n_records_max'])
    else:
        n_records_max = 1440
    n_records = len(records)
    if n_records>n_records_max:
        messages = messages+" Too many records in range, showing only the last "+str(n_records_max)+". Adjust the maximum number of records or the range.."
        records = records[0:n_records_max]
    
    # data type
    if datatype=='electricity':
        chart_ylabel = 'kWh'
        chart_data = [{'x': record.timestamp, 'y': record.verbr_kwh_x} for record in records]
        datasets = [get_dataset(
            chart_data=chart_data,
            chart_label=chart_label,
            chart_backgroundColor=chart_colour_elec_in,
       )]
    
    # chart
    chart_datasets = datasets
    chart_history = ChartHistory(
            chart_datasets=chart_datasets,
            chart_ylabel=chart_ylabel,
            chart_unit=chart_unit,
        )
    
    # render
    context = {}
    context['date_min_records'] = date_min_records
    context['date_max_records'] = date_max_records
    context['dict_items'] = dict_items
    context['dict_types'] = dict_types
    context['n_records'] = "Number of records: "+str(n_records)
    context['msg'] = messages
    context['chart_history'] = chart_history.as_html()
    return render(request, 'history/history_chart_elec.html', context=context)# -*- coding: utf-8 -*-

def history_chart_gas(request,timestep):    
    # settings
    messages = ""
    datatype = "gas"
    chart_colour_elec_in = "rgb(242, 186, 15)"
    chart_colour_elec_out = "rgb(152, 208, 35)"
    chart_colour_gas = "rgb(80, 122, 191)"

    # get items from request
    dict_items = {}
    if request.method == 'GET':
        for key, value in request.GET.items():
            if key != 'csrfmiddlewaretoken':
                dict_items[key] = value

    elif request.method == 'POST':
        for key, value in request.POST.items():
            if key != 'csrfmiddlewaretoken':
                dict_items[key] = value 
    
    # unpack request items
    dict_types = {}
    for key, value in dict_items.items():
        dict_types[key] = type(value)  
    
    # plot data and settings based on timestep of data
    chart_label = str(timestep)+'ly data'
    if timestep=='minute':
        Dataplot = HistoryMin
        chart_unit = 'hour'
    elif timestep=='hour':
        Dataplot = HistoryUur
        chart_unit = 'day'
    elif timestep=='day':
        Dataplot = HistoryDag
        chart_label = 'daily data'
        chart_unit = 'week'
    elif timestep=='month':
        Dataplot = HistoryMaand
        chart_unit = 'month'
    elif timestep=='year':
        Dataplot = HistoryJaar
        chart_unit = 'year'
    
    # query data
    if ('tmin' in dict_items.keys()) & ('tmax' in dict_items.keys()):
        date_min = datetime.strptime(dict_items['tmin'],'%Y-%m-%d')
        date_max = datetime.strptime(dict_items['tmax'],'%Y-%m-%d')          
    else:
        date_min = datetime.strptime('2000-01-01','%Y-%m-%d')
        date_max = datetime.strptime('2100-01-01','%Y-%m-%d')          
    records = Dataplot.objects.filter(timestamp__range=(date_min,date_max))

    # get current date range
    date_min_records = records.earliest('timestamp').timestamp.strftime('%Y-%m-%d')
    date_max_records = records.latest('timestamp').timestamp.strftime('%Y-%m-%d')

    # subset data to plot
    if ('n_records_max' in dict_items.keys()):
        n_records_max = int(dict_items['n_records_max'])
    else:
        n_records_max = 1440
    n_records = len(records)
    if n_records>n_records_max:
        messages = messages+" Too many records in range, showing only the last "+str(n_records_max)+". Adjust the maximum number of records or the range.."
        records = records[0:n_records_max]
    
    # data type      
    if datatype=='gas':
        chart_ylabel = 'm3'
        chart_data = [{'x': record.timestamp, 'y': record.verbr_gas_x} for record in records]
        datasets = [get_dataset(
            chart_data=chart_data,
            chart_label=chart_label,
            chart_backgroundColor=chart_colour_gas,
        )]
    
    # chart
    chart_datasets = datasets
    chart_history = ChartHistory(
            chart_datasets=chart_datasets,
            chart_ylabel=chart_ylabel,
            chart_unit=chart_unit,
        )
    
    # render
    context = {}
    context['date_min_records'] = date_min_records
    context['date_max_records'] = date_max_records
    context['dict_items'] = dict_items
    context['dict_types'] = dict_types
    context['n_records'] = "Number of records: "+str(n_records)
    context['msg'] = messages
    context['chart_history'] = chart_history.as_html()
    return render(request, 'history/history_chart_gas.html', context=context)# -*- coding: utf-8 -*-

def history_chart_costs(request,timestep):    
    # settings
    messages = ""
    datatype = "costs"
    list_datasets = []
    
    # get items from request
    dict_items = {}
    if request.method == 'GET':
        for key, value in request.GET.items():
            if key != 'csrfmiddlewaretoken':
                dict_items[key] = value

    elif request.method == 'POST':
        for key, value in request.POST.items():
            if key != 'csrfmiddlewaretoken':
                dict_items[key] = value 
    
    # unpack request items
    dict_types = {}
    for key, value in dict_items.items():
        dict_types[key] = type(value)  
    
    # plot data and settings based on timestep of data
    chart_label = str(timestep)+'ly data'
    if timestep=='minute':
        Dataplot = HistoryMin
        chart_unit = 'hour'
    elif timestep=='hour':
        Dataplot = HistoryUur
        chart_unit = 'day'
    elif timestep=='day':
        Dataplot = HistoryDag
        chart_label = 'daily data'
        chart_unit = 'week'
    elif timestep=='month':
        Dataplot = HistoryMaand
        chart_unit = 'month'
    elif timestep=='year':
        Dataplot = HistoryJaar
        chart_unit = 'year'
    
    # query data
    if ('tmin' in dict_items.keys()) & ('tmax' in dict_items.keys()):
        date_min = datetime.strptime(dict_items['tmin'],'%Y-%m-%d')
        date_max = datetime.strptime(dict_items['tmax'],'%Y-%m-%d')          
    else:
        date_min = datetime.strptime('2000-01-01','%Y-%m-%d')
        date_max = datetime.strptime('2100-01-01','%Y-%m-%d')          
    records = Dataplot.objects.filter(timestamp__range=(date_min,date_max))

    # get current date range
    date_min_records = records.earliest('timestamp').timestamp.strftime('%Y-%m-%d')
    date_max_records = records.latest('timestamp').timestamp.strftime('%Y-%m-%d')

    # subset data to plot
    if ('n_records_max' in dict_items.keys()):
        n_records_max = int(dict_items['n_records_max'])
    else:
        n_records_max = 1440
    n_records = len(records)
    if n_records>n_records_max:
        messages = messages+" Too many records in range, showing only the last "+str(n_records_max)+". Adjust the maximum number of records or the range.."
        records = records[0:n_records_max]
    

    # data sets 
    chart_label = 'elektriciteit (verbruikt)'
    chart_data = [{'x': record.timestamp, 'y': record.verbr_kwh_x*config.E_VERBRUIK_ELEK} for record in records]
    list_datasets.append(
        get_dataset(
            chart_data=chart_data,
            chart_label=chart_label,
            chart_backgroundColor=chart_colour_elec_in,
        )
    )

    chart_label = 'elektriciteit (geleverd)'
    chart_data = [{'x': record.timestamp, 'y': record.gelvr_kwh_x*config.E_GELEVERD_ELEK} for record in records]
    list_datasets.append(
        get_dataset(
            chart_data=chart_data,
            chart_label=chart_label,
            chart_backgroundColor=chart_colour_elec_out,
        )
    )

    chart_label = 'gas (verbruikt)'
    chart_data = [{'x': record.timestamp, 'y': record.verbr_gas_x*config.G_VERBRUIK_GAS} for record in records]
    list_datasets.append(
        get_dataset(
            chart_data=chart_data,
            chart_label=chart_label,
            chart_backgroundColor=chart_colour_gas,
        )
    )

    # chart
    chart_datasets = list_datasets
    chart_ylabel = '€'
    chart_history = ChartHistory(
            chart_ylabel=chart_ylabel,
            chart_unit=chart_unit,
            chart_datasets=chart_datasets,
        )
    
    # render
    context = {}
    context['date_min_records'] = date_min_records
    context['date_max_records'] = date_max_records
    context['dict_items'] = dict_items
    context['dict_types'] = dict_types
    context['n_records'] = "Number of records: "+str(n_records)
    context['msg'] = messages
    context['chart_history'] = chart_history.as_html()
    return render(request, 'history/history_chart_costs.html', context=context)# -*- coding: utf-8 -*-
