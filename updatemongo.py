"""
@author kazetora pratama.x.putra@gmail.com

simple python tool to manipulate mongo db at localhost
command line options (* is required field):
-d*: name of database
-c*: name of collection
-o*: type of operation
     currently support:
       - insert : insert/update data from csv file
       - save   : save collections to csv file
-g : create an "id" field with randomly generated 8 characters string (uuid). optional for insert operation
-i : specify input file. required for insert operation
-s : specify output file. optional for save operation (if not specified output file is out.csv by default)
-q : specify query in json format. optional for save operation
-v : specify field name for validation (to prevent duplication). required for insert operation
-t : specify datetime field (the specified field will be converted to datetime object). optional for insert operation

example:
   insert data from csv file:
      python updatemongo.py -d somedb -c somecollection -o insert -i input.csv -v name -t date_created
   save collection to csv file:
      python updatemongo.py -d somedb -c somecollection -o save -s output.csv
      # or with query
      python updatemongo.py -d somedb -c somecollection -o save -s output.csv -q '{"name":"foo"}'

Disclaimer: This tool can be used and modified freely without any restriction. 
Use it at your own risk. The author will not be held responsible for any troubles caused by usage. 
Feel free to contact the author for bug report or additional feature request (without guarantee to be responded).

"""
import sys, getopt
import csv
import json
import uuid
import dateutil.parser as dateparser
from datetime import datetime
from pymongo import MongoClient

dbname = ''
colname = ''
operation = ''
ifile = ''
savefile=''
generateID = False
query=None
validationifield = ''
timefield=''

def usage():
    print 'updatedb.py -d <dbname> -c <colname> -o <operation> [-g -i <input file> -s <output file> -q <query> -v <validation field> -t <time field>]'

def parsearg(argv):
    global dbname, colname, operation, ifile, savefile, query, generateID, validationifield, timefield
    try:
        opts, args = getopt.getopt(argv, "hgd:c:o:i:s:q:v:t:", ["db=","collection=","operation=","ifile=","savefile=","query=","validationifield=","timefield="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)   
    for opt, arg in opts:
       if opt == '-h':
           usage()
           sys.exit()
       elif opt == '-g':
           generateID=True
       elif opt in ("-d", "--db"):
           dbname = arg
       elif opt in ("-c", "--collection"):
           colname = arg
       elif opt in ("-o", "--operation"):
           operation = arg
       elif opt in ("-i", "--ifile"):
           ifile = arg
       elif opt in ("-s", "--savefile"):
           savefile = arg
       elif opt in ("-q", "--query"):
           query = json.loads(arg)
       elif opt in ("-v", "--validationifield"):
           validationifield = arg
       elif opt in ("-t", "--timefield"):
           timefield = arg

def main():
    global dbname, colname, operation, ifile, savefile, query
    if operation == 'insert':
        data = getDataFromFile()
        insert(data)
    elif operation == 'save':
        out2csv(dbname, colname, query, savefile)
    
def test():
    global dbname, colname, operation, ifile
    print dbname, colname, operation, ifile
    client = MongoClient()
    db = client[dbname]
 
    cursor=getattr(db[colname], operation)()
    cnt=0
    for doc in cursor:
        if cnt > 10:
            break
        print doc
        cnt += 1

def insert(data):
    global dbname, colname, operation, ifile, generateID, validationifield, timefield
    client = MongoClient()
    db = client[dbname]
    newdata = []
    if generateID:
        for d in data:
            d['id'] = str(uuid.uuid4())[:8]
    for d in data:
        nd = {}
        for key in d:
            if key == timefield and d[key] is not None :
                nd[key] = dateparser.parse(str(d[key]))
            elif key == '_id':
                continue
            else:
                nd[key] = d[key]
        newdata += [nd]
    for d in newdata:
        f = db[colname].find_one({validationifield:d[validationifield]})
        if f is not None:
            db[colname].update({validationifield:d[validationifield]}, {"$set":d})
        else:
            db[colname].insert(d)
            
    #result = getattr(db[colname], operation)(data)

def serialize(obj):
    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    else:
        return obj

def out2csv(dbname, colname, query, savefile = None):
    client = MongoClient()
    db = client[dbname]
    if not savefile:
        savefile = 'out.csv'
    out = open(savefile, 'w')
    cursor = db[colname].find(query)
    header = False
    colIDs = None
    for data in cursor:
        if not header:
            colIDs = [ key for key in data ]
            out.write(",".join(colIDs)+ "\n" )
            header = True
        val = []
        for key in colIDs:
            val += [data[key]]
        out.write(",".join([ str(serialize(value)) for value in val]) + "\n")
    out.close()

def getDataFromFile():
    global ifile
    if not ifile:
        usage()
        sys.exit(2)
    rownum = 0
    data = open(ifile, 'rb')
    reader = csv.reader(data)
    ret = []
    for row in reader:    
        if rownum == 0:
            header = row
        else:
            colnum = 0
            entry = {}
            for col in row:
                if col == 'None':
                    entry[header[colnum]] = None
                else:
                    entry[header[colnum]] = col
                colnum += 1
            ret += [entry]
        rownum += 1

    data.close()
    return ret   

if __name__ == "__main__":
    parsearg(sys.argv[1:])
    main()
