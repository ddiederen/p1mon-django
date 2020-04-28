# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 14:36:16 2019

@author: ddi
"""
from jchart import Chart
    
class ChartLiveGauge(Chart):
    chart_type = 'gauge'
    
    def get_options(self):
        options = {
            "panel": {
                "min": 0,
                "max": max(self.chart_scales),
                "current": self.chart_data,
                "tickInterval": self.chart_interval,
                "tickColor": "rgb(0, 0, 0)",
                "tickOuterRadius": 99,
                "tickInnerRadius": 90,
                "scales": self.chart_scales,
                "scaleColor": "rgb(0, 0, 0)",
                "scaleBackgroundColor": self.chart_colour,
                "scaleTextRadius": 50,
                "scaleTextSize": 20,
                "scaleTextColor": "rgba(0, 0, 0, 1)",
                "scaleOuterRadius": 98,
                "scaleInnerRadius": 80,
            },
            "needle": {
                "lengthRadius": 100,
                "circleColor": "rgba(188, 188, 188, 1)",
                "color": "rgba(180, 0, 0, 0.8)",
                "circleRadius": 20,
                "width": 10,
            },
            "cutoutPercentage": 70,
            "rotation": (1/2+1/3)*3.14,
            "circumference": 2*2/3*3.14,
            "legend": {
                "display": False,
                "text": "legend"
            },
            "tooltips": {
                "enabled": False
            },
            "title": {
                "display": True,
                "text": str(self.chart_data)+" "+self.chart_data_unit,
                "position": "bottom"
            },
            "animation": {
                "animateRotate": False,
                "animateScale": False
            },
        }
                    
        # options
        return(options)

    def get_datasets(self):
        datasets = [
            {
            'label': self.chart_label,
            'data': self.chart_data,
            'backgroundColor': 
                [
					"rgb(0, 255, 0)",
					"rgb(255, 0, 0)",
					"rgb(0, 0, 255)",
                ],
            }
        ]
        
        # datasets
        return(datasets)
    
    def __init__(self,chart_data=1.2,chart_data_unit='',chart_unit='hour',chart_label='no label',chart_ylabel='no label',chart_labels=[],chart_colour='rgba(255,187,205,1)',chart_scales=list(range(8+1)),chart_interval=0.1):
        Chart.__init__(self)
        self.chart_data = chart_data        
        self.chart_data_unit = chart_data_unit
        self.chart_label = chart_label
        self.chart_labels = chart_labels
        self.chart_ylabel = chart_ylabel
        self.chart_unit = chart_unit
        self.chart_colour = chart_colour
        self.chart_scales = chart_scales
        self.chart_interval = chart_interval
        self.options = self.get_options()
        self.labels = self.get_labels()
        self.datasets = self.get_datasets()
        
class ChartLiveLine(Chart):
    chart_type = 'line'
    
    def get_options(self):
        options = {
            'responsive': True,
            'title': {
                'display': True,
                'text': self.chart_title,
            },
            'legend':{
                'display': False,                    
            },
            'tooltips': {
                'mode': 'index',
                'intersect': False,
            },
            'hover': {
            'mode': 'nearest',
            'intersect': True,
            },
            'scales': {
                'xAxes': [{
                    'type': 'time',
                    'time': {
                        'tooltipFormat': "YY-MM-DD HH:mm",
                        'unit': self.chart_unit,
                        'unitStepSize': 1,
                        'displayFormats': {
                            'second': 'HH:mm:ss',
                            'minute': 'HH:mm',
                            'hour': 'HH:mm',
                            'day': 'YY-MM-DD',
                            'week': 'YY-MM-DD',
                            'month': 'MMM YYYY',
                            'quarter': 'MMM YYYY',
                            'year': 'YYYY',
                        }
                    },
                    'position': 'bottom',
                }],
                'yAxes': [{
                    'scaleLabel': {
                        'labelString': self.chart_ylabel,
                        'display': True,
                    }
                }],
            },
            'elements': {
                'point': { 
                    'radius': 0 
                } 
            },
        }
                    
        # options
        return(options)

    def get_datasets(self):
        return [{
            'label': self.chart_label,
            'data': self.chart_data,
            'backgroundColor': self.chart_colour,
#            'borderWidth': 2,
#			'borderColor': 'rgb(0, 255, 0)',
        }]

    def __init__(self,chart_data={},chart_unit='hour',chart_label='no label',chart_ylabel='no label',chart_title='no title',chart_colour='rgba(255,187,205,1)'):
        Chart.__init__(self)
        self.chart_data = chart_data
        self.chart_label = chart_label
        self.chart_ylabel = chart_ylabel
        self.chart_title = chart_title
        self.chart_unit = chart_unit
        self.chart_colour = chart_colour
        self.options = self.get_options()