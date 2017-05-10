# Simple python tool to manipulate mongo db at localhost

command line options (\* is required field):<br>
-d\*: name of database<br>
-c\*: name of collection<br>
-o\*: type of operation<br>
 currently support: <br>
       - insert : insert/update data from csv file <br>
       - save   : save collections to csv file <br>
-g : create an "id" field with randomly generated 8 characters string (uuid). optional for insert operation <br>
-i : specify input file. required for insert operation <br>
-s : specify output file. optional for save operation (if not specified output file is out.csv by default) <br>
-q : specify query in json format. optional for save operation <br>
-v : specify field name for validation (to prevent duplication). required for insert operation <br>
-t : specify datetime field (the specified field will be converted to datetime object). optional for insert operation <br>
<br>
* example: <br>
   insert data from csv file: <br> 
      python updatemongo.py -d somedb -c somecollection -o insert -i input.csv -v name -t date_created <br>
   save collection to csv file: <br>
      python updatemongo.py -d somedb -c somecollection -o save -s output.csv <br>
      # or with query <br>
      python updatemongo.py -d somedb -c somecollection -o save -s output.csv -q '{"name":"foo"}' <br>

Disclaimer: This tool can be used and modified freely without any restriction. <br>
Use it at your own risk. The author will not be held responsible for any troubles caused by usage. <br>
Feel free to contact the author for bug report or additional feature request (without guarantee to be responded).<br>

