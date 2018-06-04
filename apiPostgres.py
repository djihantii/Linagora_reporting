import psycopg2
import sys
import pprint
import os

#Ouverture du fichier markdown qui contiendra les informations
client_id = str(sys.argv[1])
contract_id = str(sys.argv[2])
output_md = open(""+contract_id+".md" , "w")

#Recovering client ID

#Recovering contract id

#Categories' title
categories = ["**Contrat**" , "**Reporting**" , "**Cloture**" ]

comite = ["**Linagora**"]
customer_contract = [ "**Nom du client**" , "**Client depuis**", "**Nomdu contrat**"  , "**description du contrat**" , "**Debut du contrat**" , "**Fin du contrat**"]
contrat = ["**Nom**"  , "**description**" , "**Debut du contrat**" , "**Fin du contrat**"]
vla = ["****" , "****" , "****" , "****"]



queries = []

query_contract = []
query_contract_VLA = []
query_contract_client=[]

query_contract.append(query_contract_client)
query_contract.append(query_contract_VLA)

query_reporting = []
query_closure = []


queries.append(query_contract)





def connexion_db():
	conn_string = " host='tosca2.linagora.dc1' dbname='tosca2dev' user='tosca2dev' password='tosca2dev' "
	print "Connecting to database \n ->%s" %(conn_string)
	conn = psycopg2.connect(conn_string)
	return conn

#Preparing queries
def queries_contract_list():
	customer_name = "SELECT name  FROM customer WHERE id = "+client_id+" ;"
	customer_since= "SELECT creation_date::timestamp::date FROM customer WHERE id = "+client_id+" ;"
	contract_name = "SELECT name FROM contract WHERE id = "+contract_id+" ;"
	contract_description = "SELECT description FROM contract WHERE id = "+contract_id+" ;"
	contract_start_date = "SELECT start_date::timestamp::date FROM contract WHERE id = "+contract_id+" ;"
	contract_end_date = "SELECT end_date::timestamp::date FROM contract WHERE id = "+contract_id+" ;"
	
	VLA_software_name = "SELECT sf.name FROM software sf INNER JOIN contract_software_version csv ON csv.software_id = sf.id where csv.contract_id = "+contract_id+" limit 22;"
	VLA_software_version = "SELECT sv.name from software_version sv inner join contract_software_version csv on csv.software_id = sv.software_id and csv.contract_id = "+contract_id+" limit 22;"
#	VLA_OS = ""

	query_contract_client.append(customer_name)
	query_contract_client.append(customer_since)
	query_contract_client.append(contract_name)
	query_contract_client.append(contract_description)
	query_contract_client.append(contract_start_date)
	query_contract_client.append(contract_end_date)
	

	query_contract_VLA.append(VLA_software_name)
	query_contract_VLA.append(VLA_software_version)
	#query_contract.append(VLA_OS)


def queries_reporting_list():
	return 1

def queries_closure_list():
	return 1


def category_contract_customer(conn):
		
	queries_contract_list()
	
	cursor = []
	cursor_client_contract=[]
	cursor_VLA_contract = []
	x=0
	while x<len(queries[0][0]):
		cursor_client_contract.append(conn.cursor())
		cursor_client_contract[x].execute(queries[0][0][x])
		x=x+1
	x=0
	while x<len(queries[0][1]):
		cursor_VLA_contract.append(conn.cursor())
		cursor_VLA_contract[x].execute(queries[0][1][x])
		x=x+1

	cursor.append(cursor_client_contract)
	cursor.append(cursor_VLA_contract)
	return cursor


def category_reporting():
	queries.append(query_reporting)
	queries.append(query_closure)
	return 1



def category_closure():
	return 1

def end_line():
	output_md.write("\n \n")

def tield():
	output_md.write("~~~")

def img_insert(name , link):
	output_md.write("!["+name+"]("+link+")")

def new_slide(title):
	output_md.write("## "+title)
	end_line()


def contract_writer(contract_dict):
	new_slide(categories[0])
	output_md.write(""+customer[0]+" : "+contract_dict["customer_name"])
	end_line()
	output_md.write(""+customer[1]+" : "+str(contract_dict["start_date"]))

def slide_contract_creator(titles , cursors , title):
	new_slide(title)
	x=0
	while x < len(titles):
		#print str( cursors[x].fetchone() )
		output_md.write(""+titles[x]+" : "+str(( cursors[x].fetchone() )[0]) )
		end_line()
		x=x+1

def slide_VLA_creator(title , cursors):
	new_slide(title)
	# i=0
	# while i<len(cursors):
	# 	output_md.write("Software : "+cursors[0].fetchone())
	# 	output_md.write(" Version : "+cursors[1])

	software = cursors[0].fetchone()
	version = cursors[1].fetchone()
	i=1
	while software is not None:
		if (i % 10) == 0:
			new_slide(title)
		output_md.write("**Software** : "+software[0]+"\t **version** : "+version[0])
		end_line()
		software = cursors[0].fetchone()
		version = cursors[1].fetchone()		
		i=i+1

def convert_odpdown(fileMD , template):
	os.system("odpdown "+fileMD +" "+ template +" " +contract_id+"report.odp")	







if __name__=="__main__":
	conn = connexion_db()
	cursors = category_contract_customer(conn)

	




	slide_contract_creator(customer_contract , cursors[0] , categories[0])	

	slide_VLA_creator("Softwares" , cursors[1])
	# contract_writer(result)


	output_md.close()
	convert_odpdown(""+contract_id+".md" , "tmplt.odp")





























