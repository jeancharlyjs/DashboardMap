#Importaciones de librerias
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px

#Importaciones del sistema
import os
import sys
from dotenv import dotenv_values

#Importacion libreria de Analisis.
import polars as pl
from pandas import DataFrame

# Importaciones Utilidades
from src import utilidades as utl




# fig = px.scatter_mapbox(df, lat="latitude", lon="longitude", 
#                   color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=7.1, width=1200, height=800)

#Data
def dataFuncion(value, value1):
	df = DataFrame(utl.readFile(value, value1)["coord"].to_dicts())
	print(df)
	return df

def dataFuncionSerie(value, value1, serie="serie"):
	# if serie == "serie":
	# 	df = DataFrame(utl.readFile(value, value1)[serie].to_dicts())
	# else:
	# 	df = DataFrame(utl.readFile(value, value1)[serie].to_dicts())
	# 	# print(df[df["TOPONIMIA"]=="SANTO DOMINGO"].sort_values(by=["acq_date"]))
	# print(DataFrame(utl.readFile(value, value1)["serie2"].to_dicts()).sort_values(by=["acq_date"]))
	match serie:
		case "serie":
			df = DataFrame(utl.readFile(value, value1)[serie].to_dicts()).sort_values(by=["acq_date"])
			return df
		case "serie1":
			df = DataFrame(utl.readFile(value, value1)[serie].to_dicts()).sort_values(by=["acq_date"])
			return df
		case "serie2":
			df = DataFrame(utl.readFile(value, value1)[serie].to_dicts()).sort_values(by=["acq_date"])
			return df
	

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div(children=[
	html.Br(),
	dbc.Row(
			dbc.Col(
					html.Div(
						html.Center(html.H1("Fundacion Dominicana del Software Libre - Mapa de Incendio Forestal")),

						)
				)
		),
	html.Br(),
	dbc.Row(
			[
				dbc.Col(width=1, lg=0.5),
				dbc.Col(
						html.Div(children=[

							html.Br(),
							html.Br(),
							html.Br(),
							dcc.Dropdown(["MODIS", "VIIRS"], value="MODIS", id="IdInstrumento"),
							html.Br(),
							dcc.Dropdown(sorted(DataFrame(utl.readFile(2022, "MODIS")["prov"]).values[0]), id="IdProv"),
							html.Br(),
							dcc.Slider(2000, 2023, marks={i: "%d"%i for i in range(2000, 2023, 5)}, id="idSlider", value=2022), 
							html.Br(),
							dbc.Card([
									dbc.CardHeader(
										html.H4("Cantidad de Incendio")
										),
									dbc.CardBody(
										html.Center(html.H1(id="idText1")),
										)
								]),
							html.Br(),
							dbc.Card([
									dbc.CardHeader(
											html.H4("Prueba")
										),
									dbc.CardBody(
										dcc.Graph(id="idHist"),
										)
								])
							]), lg=2
					),
				dbc.Col(
					html.Div(children=[
						dbc.Card([
								dbc.CardHeader(
									html.H3("Mapa de Incendio Forestal")
									),
								dbc.CardBody(
									[
									dcc.Graph(id="IdGraphMap"),
									html.Br(),
									dcc.Graph(id="idLinea"),]
									)
							], style={"width": "70%"})
						])

					)
			]
		),
	html.Br(),
	html.Br(),
	
	html.Div(children=[
		])
	])
@app.callback(Output("IdGraphMap", "figure"),
			  Output("idLinea", "figure"),
			  Output("idHist", "figure"),
			  [Input("IdInstrumento", "value"),
			   Input("idSlider", "value"),
			   Input("IdProv", "value")])
def display(value1, value, value2):
	from datetime import datetime

	TOKEN = dotenv_values(".env")["TOKEMAPBOX"]
	px.set_mapbox_access_token(TOKEN)

	# df = DataFrame(utl.readFile(value, value1)["coord"].to_dicts())
	df = dataFuncion(value, value1)
	
	if value2 == None:
		fig = px.scatter_mapbox(df, lat="latitude", lon="longitude", size="Celsius",
	              color_continuous_scale=px.colors.cyclical.IceFire, 
	              size_max=15, zoom=7,  height=500, opacity=0.7)
		fig2 = px.line(dataFuncionSerie(value, value1, "serie"), x="acq_date", y="Celsius")
		fig3 = px.line(dataFuncionSerie(value, value1, "serie"), x="acq_date", y="Celsius")
		# print()
	else:
		df2 = dataFuncionSerie(value, value1, "serie1")
		df3 = dataFuncionSerie(value, value1, "serie2")
		print(df3)
		fig = px.scatter_mapbox(df[(df["TOPONIMIA"] == value2)], lat="latitude", lon="longitude", size="Celsius",
	              color_continuous_scale=px.colors.cyclical.IceFire, 
	              size_max=15, zoom=8,  height=500, opacity=0.7)
		fig2 = px.line(df2[(df2["TOPONIMIA"]==value2)], x="acq_date", y="Celsius")
		fig3 = px.line(df3[(df3["TOPONIMIA"]==value2) ], x="acq_date", y="Celsius")
	

	if datetime.now().hour >= 18 or datetime.now().hour in [i for i in range(0, 6)]:
		fig.update_layout(mapbox_style="carto-darkmatter")
	fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
	fig2.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
	fig3.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

	return fig, fig2, fig3	              

@app.callback(Output("idText1", "children"),
			[Input("IdInstrumento", "value"),
			Input("idSlider", "value"),
			Input("IdProv", "value")]
	)
def display1(value1, value, value2):
	# df = DataFrame(utl.readFile(value, value1)["coord"].to_dicts())
	df = dataFuncion(value, value1)
	if value2 == None:
		return (len(df))
	else:
		return (len(df[df["TOPONIMIA"]==value2]))

if __name__ == "__main__":
	app.run_server(debug=True)