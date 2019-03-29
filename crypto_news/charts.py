from django.shortcuts import render, render_to_response
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
from bokeh.palettes import Category20
from bokeh.transform import cumsum

from math import pi
import pandas as pd



def pieCoins(portfolio):
	data = pd.Series(portfolio).reset_index(name='value').rename(columns={'index' : 'symbol'})
	data['angle'] = data['value']/data['value'].sum() * 2 * pi
	data['color'] = Category20[len(portfolio)]

	p = figure(plot_height=500, plot_width=500, title="Portfolio Distribution by Coin Type", toolbar_location=None, 
		tools="hover", tooltips="@symbol: @value", x_range=(-0.5, 1.0))
	p.wedge(x=0, y=1, radius=0.4,
		start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'), 
		line_color="white", fill_color="color", legend='symbol', source=data)

	p.axis.axis_label=None
	p.axis.visible=False
	p.grid.grid_line_color=None

	script, div = components(p)
	
	result = {
		'script' : script,
		'div' : div
	}

	return result


def pieValue(portfolio, price):
	values = {}
	for symbol, amount in portfolio.items():
		for coin in price['data']:
			if coin['symbol'] == symbol:
				values[symbol] = ((coin['quote']['USD']['price'])*amount)
	data = pd.Series(values).reset_index(name='value').rename(columns={'index' : 'symbol'})
	data['angle'] = data['value']/data['value'].sum() * 2 * pi
	data['color'] = Category20[len(values)]

	for index, row in data.iterrows():
		data.loc[index, 'value'] = ("{0:.2f}".format(data.loc[index, 'value']))

	p = figure(plot_height=500, plot_width=500, title="Portfolio Distribution by Coin $ Value", toolbar_location=None, 
		tools="hover", tooltips="@symbol: $@value", x_range=(-0.5, 1.0))
	p.wedge(x=0, y=1, radius=0.4,
		start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'), 
		line_color="white", fill_color="color", legend='symbol', source=data)

	p.axis.axis_label=None
	p.axis.visible=False
	p.grid.grid_line_color=None

	script, div = components(p)
	
	result = {
		'script' : script,
		'div' : div
	}

	return result