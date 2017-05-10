# Simple python tool to manipulate mongo db at localhost

command line options (\* is required field):
-d\*: name of database
-c\*: name of collection
-o\*: type of operation
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

