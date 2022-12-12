# -*- coding: utf-8 -*-
"""Copy of house pyspark.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1lsruKT_4xt8DBGXEBOAu2O-WluG-0c3d
"""

!pip install pyspark

import pyspark

from pyspark.sql import SparkSession

spark=SparkSession.builder.appName("test").getOrCreate()

spark

df=spark.read.csv("/content/drive/MyDrive/data/house price pyspark/train.csv",header=True,inferSchema=True)

df=df.drop("ADDRESS")

df.show()

type(df)

df.printSchema()

df.groupBy("POSTED_BY").count().show()

df.groupBy("BHK_OR_RK").count().show()

df=df.drop("BHK_OR_RK")
df=df.drop("READY_TO_MOVE")

df.groupBy("UNDER_CONSTRUCTION").count().show()

#RERA, the full form of which is Real Estate Regulatory Authority, stands for transparency in the real estate industry.
df.groupBy("RERA").count().show()

df.groupBy("RESALE").count().show()

df.groupBy("`BHK_NO.`").count().show()

df=df.withColumnRenamed('BHK_NO.', "BHK")

df.groupBy("BHK").count().show()

df.show()

from pyspark.ml.feature import StringIndexer

indexer=StringIndexer(inputCol="POSTED_BY",outputCol="POSTED_BY_encoded")
df=indexer.fit(df).transform(df)

df=df.drop("POSTED_BY")

from pyspark.ml.feature import VectorAssembler

featureassembler=VectorAssembler(inputCols=["UNDER_CONSTRUCTION","BHK","POSTED_BY_encoded","RERA","SQUARE_FT","RESALE","LONGITUDE","LATITUDE"],outputCol="Indepedent Features")
result=featureassembler.transform(df)

result.show()

result=result.select("Indepedent Features","TARGET(PRICE_IN_LACS)")

result.show(truncate=0)

from pyspark.ml.regression import LinearRegression

train_data,test_data=result.randomSplit([0.75,0.25])

model=LinearRegression(featuresCol="Indepedent Features",labelCol="TARGET(PRICE_IN_LACS)")

model=model.fit(train_data)

model.coefficients

model.intercept

pred=model.evaluate(test_data)

print(pred.predictions.show(100,truncate=0))

trainingSummary = model.summary

print("RMSE: %f" % trainingSummary.rootMeanSquaredError)

