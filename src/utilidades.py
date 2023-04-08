#Importaciones de librerias

import os
import sys
from glob import glob
import polars as pl
from pathlib import Path

from pandas import DataFrame
def readFile(year, instrumento):


	BASE_DIR = Path(__file__).resolve().parent.parent
	PATH = BASE_DIR /"dataset/csv"
	dataset = []
	for i in PATH.rglob("*.csv"):
		df = pl.read_csv(i)
		df = df.select(pl.col("*").exclude(["type", "satellite", "confidence", "version"]))
		dataset.append(df)
	df = pl.concat(dataset)
	df = df.with_columns([(
			pl.col("brightness") - 273.15).alias("Celsius"), 
			pl.col("acq_date").str.strptime(pl.Date, fmt="%Y-%m-%d")])
	# print(df.groupby([pl.col("acq_date").dt.year()]).agg(pl.count()))
	return {
			"df": df,
			"serie": df.select(pl.col(["acq_date", "latitude", "longitude", "TOPONIMIA", "Celsius", "instrument"])).groupby([pl.col("acq_date").dt.year()]).agg(pl.mean("Celsius")),
			"serie1": df.select(pl.col(["acq_date", "latitude", "longitude", "TOPONIMIA", "Celsius", "instrument"])).groupby([pl.col("acq_date").dt.year(), pl.col("TOPONIMIA"), pl.col("instrument")]).agg(pl.mean("Celsius")),
			"serie2": df.select(pl.col(["acq_date", "latitude", "longitude", "TOPONIMIA", "Celsius", "instrument"])).groupby([pl.col("acq_date").dt.month(), pl.col("TOPONIMIA"), pl.col("instrument")]).agg(pl.mean("Celsius")),
			"serie3": df.groupby([pl.col("acq_date").dt.year()]).agg(pl.count()),
			"instrumento": df[["instrument", "Celsius"]].groupby(df["instrument"]).agg(pl.mean("Celsius")),
			"filtro": df.filter(pl.col("acq_date").dt.year() == int(year))
			.select(pl.col(["latitude", "longitude", "instrument", "Celsius"])),
			"coord": df.select(pl.col(["acq_date", "latitude", "longitude", "TOPONIMIA", "Celsius", "instrument"]).filter((pl.col("acq_date").dt.year() == int(year)) & (pl.col("instrument")==instrumento))),
			"prov": df.select(pl.col("TOPONIMIA").unique()),
			}
