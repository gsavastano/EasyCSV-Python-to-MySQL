import sys, time
import MySQLdb as mysql

class CSVImport:
  def printhelp(self):
    print """
	******************************************
	MYSQL Easy CSV Import Command Line Client
	******************************************
	host: your mysql host
	user: your mysql username
	password: your database to import csv file to
	
	columns: the line number with column headings in the csv
	delimiter: the delimiter used to separate values
	table: the table to create and populate with values 
	
	usage:
	  python import.py host=123.456.789.456 un=someguy pw=fdsarewq db=somedb
	  
	  >file: file.csv columns=0 delimiter=, table=myTable
      """
      
  def __init__(self):		
	if sys.argv[1] == '--help': 
	  self.printhelp()
	elif sys.argv[1] == '--gui':
	  self.gui()
	else:	  
	  try:
	    args = dict([arg.split('=') for arg in sys.argv[1:]])		  
	    self.db = mysql.connect(args['host'], args['un'], args['pw'], args['db'])
	    self.cursor = self.db.cursor(mysql.cursors.DictCursor)
	    print("connected to "+args['host']+"\n"+"database: "+args['db']+" selected\n")
	    
	    
	    fname = raw_input("file: ")
	    if fname.find(".csv") != -1:
		args = fname.split(" ")
		columns = 0
		delimiter = ','
		table = args[0].split(".")[0]
		
		
		
		for x in args:
		  if x.find("columns") != -1:
		    columns = x.split("=")[1]
		  elif x.find("delimiter") != -1:
		    delimiter = x.split("=")[1]
		  elif x.find("table") != -1:
		    table = x.split("=")[1]
		    
		self.readFile(args[0], delimiter, columns, table)
	    else:
	      print("file does not have .csv extension\n is this really a csv? (kindof important) try again\n")	  
	  except Exception, e:
	    for x in e.args:
	      print x
	    sys.exit(1)

  def readFile(self, filename, delimiter, columns, table=''):
	csv = open(filename) 		
	for x in range(int(columns)+1):
	  c = csv.readline()
	  
	columns = c.split(delimiter)
	cols = ''
	
	for x in columns:
	  cols+=x+" varchar(255), "
	  
	cols = cols[:-2]
	
	sql = "create table if not exists "+table.replace("-", "_")+" (id int NOT NULL AUTO_INCREMENT, "+cols+", PRIMARY KEY (id))"
	
	
	try: 
	  self.cursor.execute(sql) 
	except Exception, e: 
	  print e
	  
	
	
	
	print "Here we go!!"
	cols = ''
	for x in columns:
	  cols+=x+", "
	  
	cols = cols[:-2]

	start = time.time()
	while True:
	  
	  row = csv.readline()
	  	  
	  if not row:
	    break
	  else:
	    row = row.split(delimiter)
	    values = ''
	    for x in row:
	      values += '"'+self.clean(x)+'", '
	      
	    values = values[:-2]
	  
	  
	    sql = "insert into "+table.replace("-", "_").lower()+" ("+cols+") values ("+values+")"
	    
	    try:
	      self.cursor.execute(sql)
	    except Exception, e:
	      self.db.commit()
	      print e
	self.db.commit()
	end = time.time()
	print "\nAll DONE EVERYTHING WORKED!!\ndam that was fast...\nstarted at: "
	print start
	print "\nended at: "
	print end
	print "\noperation took: "
	print end-start
	
	   
  def clean(self, string):
    return string.replace('"', "").replace("\n", "")
	
	
CSVImport()