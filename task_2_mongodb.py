# -*- coding: utf-8 -*-
"""Task-2 MongoDb.py

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Y8zXF1-8CAOgc8mEMrJnsh81YoHrVhuS
"""

pip install pymongo

import pymongo
from pymongo import MongoClient
from pprint import pprint

uri="mongodb+srv://Ravirajmishra:Ravi789@cluster0.hamynqb.mongodb.net/?retryWrites=true&w=majority"

client=MongoClient(uri)

db=client["guvi"]
stu_col=db['students']

import pandas as pd
ds=pd.read_json("/content/students.json",lines=True)
print(ds)

ds1=ds.to_dict("records")
ds1

db.list_collection_names()

stu_col.find_one()

stu_col.insert_many(ds1)

#1) Find the student name who scored maximum scores in all (exam, quiz and homework)?
stage1={"$unwind":"$scores"}
stage2={"$group":{"_id":"$_id", "name":{"$addToSet":'$name'}, "total_Marks":{"$sum":"$scores.score"}}}
stage3={"$sort":{"total_Marks":-1}}
stage6={"$limit":1}
for i in stu_col.aggregate([stage1,stage2, stage3, stage6]):
    pprint(i)

#2) Find students who scored below average in the exam and pass mark is 40%?
stage1={"$unwind":"$scores"}
stage2 = {"$match":{"$and":[{"scores.type":{"$in":["exam"]} },{"scores.score":{"$gt":40}} ,{"scores.score":{"$lte":52.3}}   ]}}
# if we want result in all then ,"quiz","homework" should be added in $in  

for i in stu_col.aggregate([stage1,stage2]):
    pprint(i)

#3)Find students who scored below pass mark and assigned them as fail, and above pass mark as pass in all the categories.
def aggr(std):
 prcntg = std.aggregate([{'$unwind':'$scores'},
                          {'$group':{"_id":"$_id","name":{"$first":"$name"},"max_score":{'$sum':"$scores.score"}}},
                          {'$addFields':{"prctg":{'$divide':["$max_score",3]}}},
                           {'$addFields':{"status":{"$cond":{'if' :{"$gte":["$prctg",40]},'then':"Pass",'else':"Fail"}}}}])
 return prcntg

prcntg=aggr(stu_col)
for i in prcntg:
 if i['prctg']>=40 and i['prctg']<=55:
     print(i)

prcntg=aggr(stu_col)
for i in prcntg:
  print(i)

#4)Find the total and average of the exam, quiz and homework and store them in a separate collection.
db.create_collection('total_average')
x2 = stu_col.aggregate([{'$unwind':'$scores'},{'$group':{'_id':{'type':"$scores.type"},"total:":{'$sum':"$scores.score"},"average:":{'$avg':"$scores.score"}}}])
t_a=db.total_average
for i in x2:
  print(i)
  t_a.insert_one(i)

#5)Create a new collection which consists of students who scored below average and above 40% in all the categories.
prcntg=aggr(stu_col)
db.create_collection('passed_below_average')     #collection is created once hence commented
p_a=db.passed_below_average
for i in prcntg:
  if i['prctg']>40 and i['prctg']<=55:
      print(i)
      p_a.insert_one(i)

#6)Create a new collection which consists of students who scored below the fail mark in all the categories.
prcntg=aggr(stu_col)
db.create_collection('failed')    #collection is created once hence commented
fail=db.failed
for i in prcntg:
  if i['status']=='Fail':
      print(i)
      fail.insert_one(i)

#7)Create a new collection which consists of students who scored above pass mark in all the categories.prcntg=aggr(sanjay)
prcntg=aggr(stu_col)
db.create_collection('passed')        
p=db.passed
for i in prcntg:
  if i['prctg']>=40:
      print(i)
      p.insert_one(i)

""" Telephone Directory CRUD Operation

Telephone directory: Perform CRUD operation using mongodb and python.

You need to Import necessary modules.

Perform CRUD operations to manipulate data in MongoDB. Create, retrieve, update, and delete (CRUD)

Create a database using attribute style on a MongoClient instance. Declare a variable db and assign the new database as an attribute of the client.

Create a collection. For CRUD operation, create a directory which has fields like Name, Phone number, Place etc.,

Insert the record into the collection.

Make a query to find records you just created.

Modify the records, use the update_one() method. The update_one() method requires two arguments, query and update.

Delete the record, use delete_one() method. delete_one() requires a query parameter which specifies the document to delete. """

import pymongo
from pymongo import MongoClient

uri="mongodb+srv://Ravirajmishra:Ravi@789@cluster0.hamynqb.mongodb.net/?retryWrites=true&w=majority"

data = MongoClient(uri)

db=data['TELEPHONE_DIRECTORY']

data=db['directory']

data.insert_many([{"Name":"Karan","Age":23,"Phone_number":9632154678,"Address":"Banglore","State":"Karnataka"},{"Name":"Sharan","Age":26,"Phone_number"}])

a=data.find()
for i in a:
  print(i)

b=data.update_one({"Name":'Vishya'},{'$set':{'Age':'33'}})

c = data.update_one({"Name":"Karan"},{"$unset":{"State":"Karnataka"}})

d=data.delete_one({"Name":"Karan"})