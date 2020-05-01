#%% Libraries  
from django.db.models import Sum

from django.shortcuts import render
from datetime import datetime, timedelta, date

from constance import config
import numpy as np
import math

from serialdata.charts import ChartLiveGauge, ChartLiveLine
from serialdata.models import SerialLive

#%% Settings  
chart_gauge_n_intervals_big = 10
chart_gauge_n_stripes_per_big = 5

chart_colour_elec_in = "rgb(242, 186, 15)"
chart_colour_elec_out = "rgb(152, 208, 35)"
chart_colour_gas = "rgb(80, 122, 191)"

#%% functions
def funGetIntervalBig(chart_gauge_max):
    # interval generic
    f_1 = chart_gauge_max/1
    f_2 = chart_gauge_max/2
    f_5 = chart_gauge_max/5
    
    # interval generic normalised
    f_1_log10 = math.log10(f_1)
    f_2_log10 = math.log10(f_2)
    f_5_log10 = math.log10(f_5)
    f_1_log10_round = math.floor(f_1_log10)
    f_2_log10_round = math.floor(f_2_log10)
    f_5_log10_round = math.floor(f_5_log10)
    f_1_norm = f_1*math.pow(10,-(f_1_log10_round))
    f_2_norm = f_2*math.pow(10,-(f_2_log10_round))
    f_5_norm = f_5*math.pow(10,-(f_5_log10_round))
    
    # choose interval
    if (f_1_norm==max(f_1_norm,f_2_norm,f_5_norm)):
        interval = 1*math.pow(10,f_1_log10_round)
    elif (f_2_norm==max(f_1_norm,f_2_norm,f_5_norm)):
        interval = 2*math.pow(10,f_2_log10_round)
    elif (f_5_norm==max(f_1_norm,f_2_norm,f_5_norm)):
        interval = 5*math.pow(10,f_5_log10_round)
    
    # return
    return(interval)

#%% Views  
def serialdata_live(request,liveview):    
    # render
    context = {}
    context['config'] = config
    context['liveview'] = liveview
    return render(request, 'serialdata/serialdata_live.html', context=context)

def serialdata_live_charts(request,liveview):    
    # settings
    messages = ""
    Dataplot = SerialLive
    chart_colour_elec_in = "rgb(242, 186, 15)"
    chart_colour_elec_out = "rgb(152, 208, 35)"
    chart_colour_gas = "rgb(80, 122, 191)"
    if (liveview=="elecgas"):
        title1 = "verbruik elektriciteit"
        title2 = "verbruik gas"
    elif (liveview=="elec"):
        title1 = "verbruik elektriciteit"
        title2 = "levering elektriciteit"

    # last record, round
    record_live = Dataplot.objects.latest('timestamp')
    act_verbr_kw_170_live = round(record_live.act_verbr_kw_170,3)
    act_verbr_m3_live = round(record_live.act_verbr_kw_170,3)           # get gas values!
    act_gelvr_kw_270_live = round(record_live.act_gelvr_kw_270,3)    
    
    # chart gauge 1
    chart_gauge_max = config.G_LIVE_ELEK_VERBRUIK_MAX
    chart_interval_big = funGetIntervalBig(chart_gauge_max=chart_gauge_max)
    chart_scales = sorted(list(set(np.around(np.arange(0,chart_gauge_max+chart_interval_big,chart_interval_big),decimals=3))))
    chart_interval = (chart_scales[1]-chart_scales[0])/chart_gauge_n_stripes_per_big
    chart_gauge_1 = ChartLiveGauge(
            chart_data=act_verbr_kw_170_live,
            chart_data_unit = "kW",
            chart_colour = chart_colour_elec_in,
            chart_scales = chart_scales,
            chart_interval = chart_interval,
        )
    
    # chart gauge 2
    if (liveview=="elecgas"):
        chart_gauge_max = config.G_LIVE_GAS_MAX
        chart_interval_big = funGetIntervalBig(chart_gauge_max=chart_gauge_max)
        chart_scales = sorted(list(set(np.around(np.arange(0,chart_gauge_max+chart_interval_big,chart_interval_big),decimals=3))))
        chart_interval = (chart_scales[1]-chart_scales[0])/chart_gauge_n_stripes_per_big
        chart_gauge_2 = ChartLiveGauge(
                chart_data=act_verbr_m3_live,
                chart_data_unit = "m3/u",
                chart_colour = chart_colour_gas,
                chart_scales = chart_scales,
                chart_interval = chart_interval,
            )
    elif (liveview=="elec"):
        chart_gauge_max = config.G_LIVE_ELEK_GELEVERD_MAX
        chart_interval_big = funGetIntervalBig(chart_gauge_max=chart_gauge_max)
        chart_scales = sorted(list(set(np.around(np.arange(0,chart_gauge_max+chart_interval_big,chart_interval_big),decimals=3))))
        chart_interval = (chart_scales[1]-chart_scales[0])/chart_gauge_n_stripes_per_big
        chart_gauge_2 = ChartLiveGauge(
                chart_data=act_gelvr_kw_270_live,
                chart_data_unit = "kW",
                chart_colour = chart_colour_elec_out,
                chart_scales = chart_scales,
                chart_interval = chart_interval,
            )

    # chart line 1
    time_threshold = record_live.timestamp - timedelta(minutes=10)  # records last 10 minutes
    records = SerialLive.objects.filter(timestamp__gt=time_threshold)
    chart_line_1 = ChartLiveLine(
        chart_data=[{'x': record.timestamp, 'y': record.act_verbr_kw_170} for record in records],
        chart_title='laatste 10 minuten',
        chart_ylabel='kW',
        chart_label='P [kW]',
        chart_unit='minute',
        chart_colour=chart_colour_elec_in,
   )
    
    # chart line 2
    if (liveview=="elecgas"):
        time_threshold = record_live.timestamp - timedelta(hours=2)  # records last 2 hours
        records = SerialLive.objects.filter(timestamp__gt=time_threshold)
        chart_line_2 = ChartLiveLine(
            chart_data=[{'x': record.timestamp, 'y': record.act_verbr_kw_170} for record in records],
            chart_title='laatste 2 uur',
            chart_ylabel='m3/u',
            chart_label='Q [m3/u]',
            chart_unit='hour',
            chart_colour=chart_colour_gas,
        )
    elif (liveview=="elec"):
        time_threshold = record_live.timestamp - timedelta(minutes=10)  # records last 2 hours
        records = SerialLive.objects.filter(timestamp__gt=time_threshold)
        chart_line_2 = ChartLiveLine(
            chart_data=[{'x': record.timestamp, 'y': record.act_gelvr_kw_270} for record in records],
            chart_title='laatste 10 minuten',
            chart_ylabel='kW',
            chart_label='P [kW]',
            chart_unit='minute',
            chart_colour=chart_colour_elec_in,
        )
    
    # render
    context = {}
    context['config'] = config
    context['msg'] = messages
    context['title1'] = title1
    context['title2'] = title2
    context['chart_gauge_1'] = chart_gauge_1.as_html()
    context['chart_line_1'] = chart_line_1.as_html()
    context['chart_gauge_2'] = chart_gauge_2.as_html()
    context['chart_line_2'] = chart_line_2.as_html()
    return render(request, 'serialdata/serialdata_live_charts.html', context=context)# -*- coding: utf-8 -*-


def serialdata_today(request):    
    # render
    context = {}
    context['config'] = config
    return render(request, 'serialdata/serialdata_today.html', context=context)


def serialdata_today_charts(request):    
    # records today
    date_filter = date.today()
    date_filter = datetime.strptime('2019-06-12','%Y-%m-%d')
    records_today = SerialLive.objects.filter(timestamp__date=date_filter)
    record_today_earliest = records_today.earliest('timestamp')
    record_today_latest = records_today.latest('timestamp')
    
    # usage today
    verbr_kwh_181_min = record_today_earliest.verbr_kwh_181
    verbr_kwh_181_max = record_today_latest.verbr_kwh_181
    verbr_kwh_181_today = verbr_kwh_181_max-verbr_kwh_181_min
    verbr_kwh_182_min = record_today_earliest.verbr_kwh_182
    verbr_kwh_182_max = record_today_latest.verbr_kwh_182
    verbr_kwh_182_today = verbr_kwh_182_max-verbr_kwh_182_min
    verbr_kwh_x_today = verbr_kwh_181_today+verbr_kwh_182_today
    
    gelvr_kwh_281_min = record_today_earliest.gelvr_kwh_281
    gelvr_kwh_281_max = record_today_latest.gelvr_kwh_281
    gelvr_kwh_281_today = gelvr_kwh_281_max-gelvr_kwh_281_min
    gelvr_kwh_282_min = record_today_earliest.gelvr_kwh_282
    gelvr_kwh_282_max = record_today_latest.gelvr_kwh_282
    gelvr_kwh_282_today = gelvr_kwh_282_max-gelvr_kwh_282_min
    gelvr_kwh_x_today = gelvr_kwh_281_today+gelvr_kwh_282_today
    
    verbr_gas_2421_min = record_today_earliest.verbr_gas_2421
    verbr_gas_2421_max = record_today_latest.verbr_gas_2421
    verbr_gas_2421_today = verbr_gas_2421_max-verbr_gas_2421_min

    # round data
    verbr_kwh_x_today = round(verbr_kwh_x_today,3)
    gelvr_kwh_x_today = round(gelvr_kwh_x_today,3)
    verbr_gas_2421_today = round(verbr_gas_2421_today,3)
    
    # chart gauge 1
    chart_gauge_max = config.G_TODAY_ELEK_VERBRUIK_MAX
    chart_interval_big = funGetIntervalBig(chart_gauge_max=chart_gauge_max)
    chart_scales = sorted(list(set(np.around(np.arange(0,chart_gauge_max+chart_interval_big,chart_interval_big),decimals=3))))
    chart_interval = (chart_scales[1]-chart_scales[0])/chart_gauge_n_stripes_per_big
    chart_gauge_elec_in_today = ChartLiveGauge(
            chart_data=verbr_kwh_x_today,
            chart_data_unit = "kWh",
            chart_colour = chart_colour_elec_in,
            chart_scales = chart_scales,
            chart_interval = chart_interval,
        )
    
    # chart gauge 2
    chart_gauge_max = config.G_TODAY_ELEK_GELEVERD_MAX
    chart_interval_big = funGetIntervalBig(chart_gauge_max=chart_gauge_max)
    chart_scales = sorted(list(set(np.around(np.arange(0,chart_gauge_max+chart_interval_big,chart_interval_big),decimals=3))))
    chart_interval = (chart_scales[1]-chart_scales[0])/chart_gauge_n_stripes_per_big
    chart_gauge_elec_out_today = ChartLiveGauge(
            chart_data=gelvr_kwh_x_today,
            chart_data_unit = "kWh",
            chart_colour = chart_colour_elec_out,
            chart_scales = chart_scales,
            chart_interval = chart_interval,
        )

    # chart gauge 3 
    chart_gauge_max = config.G_TODAY_GAS_MAX
    chart_interval_big = funGetIntervalBig(chart_gauge_max=chart_gauge_max)
    chart_scales = sorted(list(set(np.around(np.arange(0,chart_gauge_max+chart_interval_big,chart_interval_big),decimals=3))))
    chart_interval = (chart_scales[1]-chart_scales[0])/chart_gauge_n_stripes_per_big
    chart_gauge_gas_today = ChartLiveGauge(
            chart_data=verbr_gas_2421_today,
            chart_data_unit = "m3",
            chart_colour = chart_colour_gas,
            chart_scales = chart_scales,
            chart_interval = chart_interval,
        )
    
    # render
    context = {}
    context['config'] = config
    context['chart_gauge_elec_in_today'] = chart_gauge_elec_in_today.as_html()
    context['chart_gauge_elec_out_today'] = chart_gauge_elec_out_today.as_html()
    context['chart_gauge_gas_today'] = chart_gauge_gas_today.as_html()
    return render(request, 'serialdata/serialdata_today_charts.html', context=context)# -*- coding: utf-8 -*-
