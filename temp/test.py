import csv

mydata = [['This', 'is', 'a', 'test', 'row'], 
['This', 'is', 'another', 'test', 'row', 'my', 'dude'],
['100', '200', '300', '400', '500']]

with open('test.csv', 'w') as target:
  writer = csv.writer(target)
  writer.writerows(mydata)