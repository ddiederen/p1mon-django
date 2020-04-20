# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 14:36:16 2019

@author: ddi
"""
from jchart import Chart

class ChartHistory(Chart):
    chart_type = 'bar'
    
    def get_options(self):
        options = {
            'responsive': True,
            'title': {
                'display': False,
                'text': 'Chart.js Line Chart'
            },
            'tooltips': {
                'mode': 'index',
                'intersect': False,
            },
            #                    'hover': {
            #                    'mode': 'nearest',
            #                    'intersect': True
            #                    },
            'scales': {
                'xAxes': [{
                    'stacked': True,
                    'type': 'time',
                    'time': {
                        'tooltipFormat': "YY-MM-DD HH:mm",
                        'unit': self.chart_unit,
                        'unitStepSize': 1,
                        'displayFormats': {
                            'second': 'YY-MM-DD HH:mm:ss',
                            'minute': 'YY-MM-DD HH:mm',
                            'hour': 'YY-MM-DD HH:mm',
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
                    'stacked': True,
                    'scaleLabel': {
                        'labelString': self.chart_ylabel,
                        'display': True,
                    }
                }],            
            
            },
            'plugins': {
                'zoom': {
                    'zoom': {
                        'enabled': True,
                        'drag': False,
                        'mode': 'x',
                        'speed': 0.5
                    },
                    'pan': {
                        'enabled': True,
                        'mode': 'x',
                        'speed': 10,
                        'threshold': 10
                    },
                }
            },
            'elements': {
                'rectangle': {
                    'borderWidth': 1,
                    'borderColor': "rgb(150, 150, 150)",
                }
            },
        }
                    
        # options
        return(options)

    def get_datasets(self):
        return self.chart_datasets

    def __init__(self,chart_datasets={},chart_unit='hour',chart_ylabel='no label'):
        Chart.__init__(self)
        self.chart_datasets = chart_datasets
        self.chart_ylabel = chart_ylabel
        self.chart_unit = chart_unit
        self.options = self.get_options()
