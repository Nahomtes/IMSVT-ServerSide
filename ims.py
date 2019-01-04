#!/usr/bin/env python
import os, sys
import cgi
import json

import MySQLdb
import string

from optparse import OptionParser


###################################

	# To insert data into the dataBases
def Main_save_data_into_church_data(inJson, email, time_stamp):
	##### print "\t***** Main_save_data_into_church_data() FUNCTION START HERE *****" #####
	# making connection with MySQL server
	db_name = "church_DB"
	db_userid = "churchdbadmin"
	db_password = "pass123"
	db_host = "127.0.0.1" ## localhost
	dbh = MySQLdb.connect(host=db_host, user=db_userid, passwd = db_password, db = db_name)

	# inistialing email and time stamp from inJson
	
	serviceType = inJson["serviceType"]
	##### print "service Type ===> %s" % serviceType
	
	
	
	if (serviceType == "lecture"):
		service_type_table_name = "lecture_service_table"
		service_type_id = lecture_table(dbh, inJson, email, time_stamp, service_type_table_name)
	
	elif (serviceType == "teach"):
		service_type_table_name = "teach_service_table"
		service_type_id = teach_table(dbh, inJson, email, time_stamp, service_type_table_name)
		
	elif (serviceType == "help"):
		service_type_table_name = "help_service_table"
		service_type_id = help_table(dbh, inJson, email, time_stamp, service_type_table_name)

	elif (serviceType == "drive"):
		service_type_table_name = "drive_service_table"
		service_type_id = drive_table(dbh, inJson, email, time_stamp, service_type_table_name)

	####### print "This is the id we gotfrom our %s ===> %d" % (service_type_table_name, service_type_id) #####
		
	individual_information_id = individual_information_table(dbh, inJson, email, time_stamp)
	##### print "This is the id we got from our individual_information_id ==>", individual_information_id #####

	if service_type_id is not 0 and individual_information_id is not 0:		
		try:
			sql = "INSERT INTO %s (%s, %s, %s) VALUE ('%s','%d','%d')" %("church_data_table", "service_type_table_name", "service_type_id","individual_information_id", service_type_table_name, service_type_id, individual_information_id)

			cur = dbh.cursor()
			cur.execute(sql)
			dbh.commit()
	
			cur.close()
			"""
			sql2 ="SELECT church_data_id FROM church_data_table WHERE service_type_table_name='%s' AND service_type_id='%s' AND individual_information_id='%s'" % (service_type_table_name , service_type_id, individual_information_id)
			...
			...
			"""
		except:
			""""
			sql2 ="SELECT church_data_id FROM church_data_table WHERE service_type_table_name='%s' AND service_type_id='%s' AND individual_information_id='%s'" % (service_type_table_name , service_type_id, individual_information_id)

			cursor = dbh.cursor()
			cursor.execute(sql2)
			fetched_data = cursor.fetchall()
			#dbh.commit() ### This line has to be put here, make you that the data acullty put on in the dataBase. if you don't have this your data won't be on the database. I got stuck trying to give why I couldn't see my data in the databases for days because I didn' put this lone of code.
			cursor.close()

			church_data_id = getId(fetched_data)
			##### print "This is the id we got from our church_data_id ==>", church_data_id #####

			dbh.close()
			##### print "\n\t***** Main_save_data_into_church_data() FUNCTION END HERE*****\n" #####
			"""	
	return ##### "OUR PROGRAM IS COMPLETELY WORKING" #####

#########################################
def lecture_table(dbh, inJson, email, time_stamp, table_name):
	
	##### print "\n\t\t***** lecture_table() FUNCTION START HERE *****" #####

	
	lecture_duration = inJson["serviceDuration"]
	service_date = inJson["serviceDay"]
	description = inJson["lectureTopic"]

	# Insert into the database table called lecture_service_table into three column
	#lecture_service_Auto_inc_id = 0

	try:
		sql = "INSERT INTO %s (%s, %s,%s) VALUES ('%s', '%s', '%s')" % (table_name,"lecture_duration","service_date","description", lecture_duration, service_date, description)
	
		cursor = dbh.cursor()
		cursor.execute(sql)
		dbh.commit()  # make sure data carry out[committed] to database
		sql2 = "SELECT %s FROM %s WHERE %s='%s' AND %s='%s' AND %s='%s'" % ("lecture_service_id",table_name, "lecture_duration",lecture_duration, "service_date",service_date, "description",description)

		cursor = dbh.cursor()
		cursor.execute(sql2)
	
		fetched_data = cursor.fetchall() # comes like this ((2L,),(4L),) if there is data, if there is n data then ()
	##### print "\t\tfetched_data ==> ", fetched_data #####

		lecture_service_Auto_inc_id = getId(fetched_data) # this is function that return single id i.e 1 or 4 from ((2L,),(4L),) 
		

	except: # if the data already exist then just return the id of it
		sql2 = "SELECT %s FROM %s WHERE %s='%s' AND %s='%s' AND %s='%s'" % ("lecture_service_id",table_name, "lecture_duration",lecture_duration, "service_date",service_date, "description",description)

		cursor = dbh.cursor()
		cursor.execute(sql2)
	
		fetched_data = cursor.fetchall() # comes like this ((2L,),(4L),) if there is data, if there is n data then ()
	##### print "\t\tfetched_data ==> ", fetched_data #####

		lecture_service_Auto_inc_id = getId(fetched_data) # this is function that return single id i.e 1 or 4 from ((2L,),(4L),) 

		
	

	###### print "\n\t\t***** lecture_table() FUNCTION END HERE *****\n" #####
	
	return lecture_service_Auto_inc_id

####################################################
def teach_table(dbh, inJson, email, time_stamp, table_name):
	
	##### print "\n\t\t***** teach_table() FUNCTION START HERE *****" #####

	
	student_age_group = inJson["studentAgeGroup"]
	service_date= inJson["serviceDay"]
	
	
	# Insert into the database table called teach_service_table into two column
	try:
		sql = "INSERT INTO %s (%s, %s) VALUE ('%s','%s')" %(table_name, "student_age_group", "service_date",student_age_group, service_date)
	
		cursor = dbh.cursor()
		cursor.execute(sql)
		dbh.commit()  # make sure data carry out[committed] to database
	
		sql2 = "SELECT %s FROM %s WHERE %s='%s' AND %s='%s'" % ("teach_service_id",table_name, "student_age_group",student_age_group, "service_date",service_date)

		cursor = dbh.cursor()
		cursor.execute(sql2)
	
		fetched_data = cursor.fetchall() # comes like this ((2L,),(4L),) if there is data, if there is n data then ()
		##### print "\t\tfetched_data ==> ", fetched_data #####

		teach_service_Auto_inc_id = getId(fetched_data) # this is function that return single id i.e 1 or 4 from ((2L,),(4L),) 
	except:
		sql2 = "SELECT %s FROM %s WHERE %s='%s' AND %s='%s'" % ("teach_service_id",table_name, "student_age_group",student_age_group, "service_date",service_date)

		cursor = dbh.cursor()
		cursor.execute(sql2)
	
		fetched_data = cursor.fetchall() # comes like this ((2L,),(4L),) if there is data, if there is n data then ()
		##### print "\t\tfetched_data ==> ", fetched_data #####

		teach_service_Auto_inc_id = getId(fetched_data) # this is function that return single id i.e 1 or 4 from ((2L,),(4L),) 

		

		
	

	##### print "\n\t\t***** teach_table() FUNCTION END HERE *****\n" #####
	
	return teach_service_Auto_inc_id

####################################################
def help_table(dbh, inJson, email, time_stamp, table_name):
	
	##### print "\n\t\t***** help_table() FUNCTION START HERE *****" #####

	
	holiday_name = inJson["serviceDay"]
	holiday_service= inJson["whichService"]
	
	
	
	# Insert into the database table called help_service_table into two column
	try:
		sql = "INSERT INTO %s (%s, %s) VALUE ('%s','%s')" %(table_name, "holiday_name", "holiday_service", holiday_name, holiday_service)
	
		cursor = dbh.cursor()
		cursor.execute(sql)
		dbh.commit()  # make sure data carry out[committed] to database
	
		sql2 = "SELECT %s FROM %s WHERE %s='%s' AND %s='%s'" % ("help_service_id",table_name, "holiday_name",holiday_name, "holiday_service",holiday_service)

		cursor = dbh.cursor()
		cursor.execute(sql2)
	
		fetched_data = cursor.fetchall() # comes like this ((2L,),(4L),) if there is data, if there is n data then ()
		##### print "\t\tfetched_data ==> ", fetched_data #####

		teach_service_Auto_inc_id = getId(fetched_data) # this is function that return single id i.e 1 or 4 from ((2L,),(4L),) 

	except:
		sql2 = "SELECT %s FROM %s WHERE %s='%s' AND %s='%s'" % ("help_service_id",table_name, "holiday_name",holiday_name, "holiday_service",holiday_service)

		cursor = dbh.cursor()
		cursor.execute(sql2)
	
		fetched_data = cursor.fetchall() # comes like this ((2L,),(4L),) if there is data, if there is n data then ()
		##### print "\t\tfetched_data ==> ", fetched_data #####

		teach_service_Auto_inc_id = getId(fetched_data) # this is function that return single id i.e 1 or 4 from ((2L,),(4L),) 

		
	

	###### print "\n\t\t***** help_table() FUNCTION END HERE *****\n" #####
	return teach_service_Auto_inc_id

####################################################
def drive_table(dbh, inJson, email, time_stamp, service_type_table_name):
	
	##### print "\n\t\t***** drive_table() FUNCTION START HERE *****" #####

	# These two libe belw are geting the especife data we have to store that define the drive service type which is availableSit, and the serviceDay from inJson. inJon is the data we get from the brower as a form and send by javaScript as a Json format and we got inJSon when we loads into object from string json format.
	available_seats = inJson["availableSit"]
	service_date= inJson["serviceDay"]
	# Insert into the database table called drive_service_table into two column
	try:
		sql = "INSERT INTO drive_service_table (available_seats, service_date) VALUES ('%s', '%s')" % (available_seats, service_date)
	
		cursor = dbh.cursor()
		cursor.execute(sql)
		 # make sure data carry out[committed] to database

		sql2 = "SELECT drive_service_id FROM drive_service_table WHERE available_seats='%s' AND service_date='%s'" % (available_seats, service_date)
		cursor = dbh.cursor()
		cursor.execute(sql2)
		dbh.commit()
		fetched_data = cursor.fetchall() # comes like this ((2L,),(4L),) if there is data, if there is n data then ()
		#print "\t\tfetched_data ==> ", fetched_data

		drive_service_Auto_inc_id = getId(fetched_data) # this is function that return single id i.e 1 or 4 from ((2L,),(4L),) 

	except:
		sql2 = "SELECT drive_service_id FROM drive_service_table WHERE available_seats='%s' AND service_date='%s'" % (available_seats, service_date)
		cursor = dbh.cursor()
		cursor.execute(sql2)
		dbh.commit()
		fetched_data = cursor.fetchall() # comes like this ((2L,),(4L),) if there is data, if there is n data then ()
		#print "\t\tfetched_data ==> ", fetched_data

		drive_service_Auto_inc_id = getId(fetched_data) # this is function that return single id i.e 1 or 4 from ((2L,),(4L),) 		

		
	#dbh.close() Don't close the database conection bc dbh is given as an input to drive_table() function from the Main_save_data_into_church_data(), so if you close it now then you can't be connected anymore even in other place like Main_save_data_into_church_data() function, so prevent this close the connection to DB at the end of Main_save_data_into_church_data() function
	

		##### print "\n\t\t***** drive_table() FUNCTION END HERE *****\n" #####
	return drive_service_Auto_inc_id

####################################################
def getId(fetchall_data):

	if fetchall_data is not ():
		for outer in list(fetchall_data): # Now turn to this [(2L,), (4L,)] format
			for inner in list(outer): # Now turn to this [[2],[4]] format
				auto_inc_id = inner
		
	
	else:
		#return 0 as an id if there isn't any data that in the [table] that is same as the input you gave it when you did SELECT .. FROM [table] (..)..."
		auto_inc_id = 0

	return auto_inc_id
###################################################################	
def individual_information_table(dbh, inJson, email, time_stamp):
	
	##### print "\n\t\t***** individual_information_table() FUNCTION START HERE *****\n"
	
	table_name = "individual_information_table"
	first_name = inJson["firstName"]
	last_name= inJson["lastName"]
	telephone = inJson["telephone"]
	prefered_contact = inJson["contactPreference"] 
	zip_code = inJson["zipcode"]

	try:
		sql = "INSERT INTO individual_information_table (first_name,last_name, telephone, email, prefered_contact, zip_code, time_stamp) VALUE ('%s', '%s', '%s', '%s', '%s', '%s', '%s')" %(first_name, last_name, telephone, email, prefered_contact, zip_code, time_stamp)


		cursor = dbh.cursor()
		cursor.execute(sql)

		sql2 = "SELECT individual_information_id FROM individual_information_table WHERE first_name='%s' AND last_name='%s' AND telephone='%s' AND email='%s' AND prefered_contact='%s' AND zip_code='%s' AND time_stamp='%s'" % (first_name, last_name, telephone, email, prefered_contact, zip_code, time_stamp)

		cursor = dbh.cursor()
		cursor.execute(sql2)
		fetched_data = cursor.fetchall()
	
		individual_information_auto_inc_id = getId(fetched_data)

	
	except:
		sql2 = "SELECT individual_information_id FROM individual_information_table WHERE first_name='%s' AND last_name='%s' AND telephone='%s' AND email='%s' AND prefered_contact='%s' AND zip_code='%s' AND time_stamp='%s'" % (first_name, last_name, telephone, email, prefered_contact, zip_code, time_stamp)

		cursor = dbh.cursor()
		cursor.execute(sql2)
		fetched_data = cursor.fetchall()
	
		individual_information_auto_inc_id = getId(fetched_data)




	dbh.commit()
	##### print "\n\t\t***** individual_information_table() FUNCTION END HERE *****\n"

	return individual_information_auto_inc_id

##################################################
def joinTables():
	
	db_host = "127.0.0.1" #<==> localhost
	db_user = "churchdbadmin"
	db_password = "pass123"
	db_name = "church_DB"

	dbh = MySQLdb.connect(host=db_host, user=db_user, passwd=db_password, db=db_name)

	sql = "SELECT * FROM church_data_table"
	cursor = dbh.cursor() ## cursor class help/allow for command you are trying to run from python to execute  
	cursor.execute(sql)
	
	cdf = cursor.fetchall() ## fetch data from church_data_table
	
	
	for outer in xrange(0,len(cdf)):
								
		if (cdf[outer][1] == "lecture_service_table"):
			print "LLLLLLLLLLLLLLLLLL %d ==> %s"% (outer, cdf[outer][1])
		elif (cdf[outer][1] == "teach_service_table"):
			print "SSSSSSSSSSSSSSSSSSSSSS %d ==> %s"% (outer, cdf[outer][1])
		elif (cdf[outer][1] == "help_service_table"):
			print "HHHHHHHHHHHHHHHHHHHHH %d ==> %s"% (outer, cdf[outer][1])
		elif (cdf[outer][1] == "drive_service_table"):
			print "DDDDDDDDDDDDDDDDDDDD %d ==> %s"% (outer, cdf[outer][1])

	return 


##################################################
def saveSurveyNew(myObj, recordKey1, recordKey2):

	jsonFile = "/volunteerdb/newdatabase.json"
	jsonText1 = open(jsonFile).read()
	jsonDb = json.loads(jsonText1) # String to Oject (deserialization)
	if recordKey1 not in jsonDb:
		jsonDb[recordKey1] = {recordKey2:myObj}
	else:
		jsonDb[recordKey1][recordKey2] = myObj

	jsonDb[recordKey1][recordKey2] = myObj
	jsonText2 = json.dumps(jsonDb, indent=4) # Object to String (serialization)

	FW=open(jsonFile, "w")
	FW.write("%s" % (jsonText2))
	FW.close()

       
	return ""
################################
def main():


	global form

 	inJson = {}
	#This is how we should get input values from command line user or remote user
   
   

	if len(sys.argv) == 2:
 		inJson = json.loads(sys.argv[1])
	else:
		form = cgi.FieldStorage()
		inJson = json.loads(form["injson"].value) if "injson" in form else {}

	outJson = {}
	myObj = {}
	if inJson["pageid"] == "home":
		if inJson["action"] == "getfirstpage":
			outJson = {
				"serviceTypeObj":{
					"lecture":"Give a lecture after church"
					,"teach":"Teach a class(young youth starting from 6-14 and older)"
					,"help":"Help on holiday\'s(such as helping with setting up food, cleaning or directing people to free parking spaces)"
					,"drive":"Volunteer to drive people who have no means of transportaion"
				}
			}
			outJson["taskStatus"] = 1
		elif inJson["action"] == "getsecondpage":
			if inJson["serviceTypeObj"] == "lecture":
				outJson = {
					"serviceDurationObj":{#change to serviceDurationObj
						"1/2hour":"half hour"
						,"1hour":"one hour"
						,"1&1/2hour":"one and half hour"
						,"2hour":"two hours"
					}
					,"serviceDayObj":{#change to serviceDayObj
						"first":"jan 1st 2018"
						,"eighth":"jan 8th 2018"
						,"seventeenth":"jan 17 2018"
						,"twentyforth":"jan 24 2018"
					}
           
				}
				outJson["taskStatus"] = 1

           
			elif inJson["serviceTypeObj"] == "teach":
				outJson = {
					"studentAgeGroupObj":{#
						"3-5oldclass":"3-5 years old class(10:30am-11:00am)"
						,"6-9oldclass":"6-9 years old class(10:30am-11:00am)"
						,"10-14oldclass":"10-14 years old class(10:20-11:40)"
						,"14&abv":"14 and above years old class(10:20-11:40)"
					}
					,"serviceDayObj":{#change to serviceDayObj
						"first":"jan 1st 2018"
						,"eighth":"jan 8th 2018"
						,"seventheenth":"jan 17 2018"
						,"twentyforth":"jan 24 2018"
					}
				}
				outJson["taskStatus"] = 1
               
			elif inJson["serviceTypeObj"] == "help":
				outJson = {
					"serviceDayObj":{
						"medhaneAlem":"Medhane Alem holiday"
						,"easter":"Easter Holiday"
						,"christmas":"Christmas"
					}
					,"whichServiceObj":{
						"Setting Up":"Setting up ahead of time"
						,"findParking":"helping people find parking spots"
						,"cleaning":"Cleaning up"
					}
				}
				outJson["taskStatus"] = 1
           
           
			elif inJson["serviceTypeObj"] == "drive":
				outJson = {
					"serviceDayObj":{
						"first":"Mar 4st 2018"
						,"eighth":"Mar 11th 2018"
						,"seventheenth":"Mar 18 2018"
						,"twentyforth":"Mar 25 2018"
					}
					,"availableSitObj":{
						"one":"One available sit"
						,"two":"Two available sits"
						,"three":"Three available sits"
						,"four":"Four avilable sits"
					}
				}
				outJson["taskStatus"] = 1
			elif inJson["serviceTypeObj"] == "":
				outJson["errorMsg"] = "service type not selected";
		elif inJson["action"] == "getthirdpage":
			outJson = {
				"format":["name","type","placeholder"]   
				,"fname":["fname","text","First Name"]
				,"lname":["lname","text","Last Name"]
				,"telephone":["telephone","text","Telephone Number"]
				,"email":["email","email","E-mail"]
				,"zipcode":["zipcode","text","Zip Code"]
				,"pcontact":{
					"email":"Email"
					,"telephone":"Telephone"
				}
			}
			outJson["taskStatus"] = 1
		elif inJson["action"] == "getfourthpage":
			if inJson["serviceTypeObj"] == "lecture":
				recordKey1 = inJson["email"]
				recordKey2 = inJson["timeStamp"]
				myObj = {
					"firstName":inJson["fname"]
					,"lastName":inJson["lname"]
					,"email":inJson["email"]
					,"telephone":inJson["telephone"]
					,"contactPreference":inJson["pcontact"]
					,"zipcode":inJson["zipcode"]
					,"serviceType":inJson["serviceTypeObj"]
					,"serviceDuration":inJson["serviceDurationObj"]
					,"serviceDay":inJson["serviceDayObj"]
					,"lectureTopic":inJson["textarea1"]
					,"count":"count"
				}
           
			elif inJson["serviceTypeObj"] == "teach":
				recordKey1 = inJson["email"]
				recordKey2 = inJson["timeStamp"]
				myObj = {
					"firstName":inJson["fname"]
					,"lastName":inJson["lname"]
					,"email":inJson["email"]
					,"telephone":inJson["telephone"]
					,"contactPreference":inJson["pcontact"]
					,"zipcode":inJson["zipcode"]
					,"serviceType":inJson["serviceTypeObj"]
					,"serviceDay":inJson["serviceDayObj"]
					,"studentAgeGroup":inJson["studentAgeGroupObj"]
					,"count":"count"
				}

			elif inJson["serviceTypeObj"] == "help":
				recordKey1 = inJson["email"]
				recordKey2 = inJson["timeStamp"]
				myObj = {
					"firstName":inJson["fname"]
					,"lastName":inJson["lname"]
					,"email":inJson["email"]
					,"telephone":inJson["telephone"]
					,"contactPreference":inJson["pcontact"]
					,"zipcode":inJson["zipcode"]
					,"serviceType":inJson["serviceTypeObj"]
					,"serviceDay":inJson["serviceDayObj"]
					,"whichService":inJson["whichServiceObj"]
					,"count":"count"
				}

			elif inJson["serviceTypeObj"] == "drive":
				recordKey1 = inJson["email"]
				recordKey2 = inJson["timeStamp"]
				myObj = {
					"firstName":inJson["fname"]
					,"lastName":inJson["lname"]
					,"email":inJson["email"]
					,"telephone":inJson["telephone"]
					,"contactPreference":inJson["pcontact"]
					,"zipcode":inJson["zipcode"]
					,"serviceType":inJson["serviceTypeObj"]
					,"serviceDay":inJson["serviceDayObj"]
					,"availableSit":inJson["availableSitObj"]
					,"count":"count"
				}
			#saveSurveyNew(myObj, recordKey1, recordKey2)
			Main_save_data_into_church_data(myObj, recordKey1, recordKey2)
			outJson["taskStatus"] = 1

	elif inJson["pageid"] == "stat":
		
		#joinTables()
		jsonDb = {}
		jsonFile = "/volunteerdb/newdatabase.json"
		jsonText1 = open(jsonFile).read()   
		jsonDb = json.loads(jsonText1) # String to Oject (deserialization)
		
		index = 0
		outJson = {}  

		joinTables()
		""" 
		for email in jsonDb:
			for ts in jsonDb[email]:
               
				d = jsonDb[email][ts]["serviceDay"]
				t = jsonDb[email][ts]["serviceType"]
				fname = jsonDb[email][ts]["firstName"]
				lname = jsonDb[email][ts]["lastName"]
				count = jsonDb[email][ts]["count"]
				name = jsonDb[email][ts]["firstName"]+' '+jsonDb[email][ts]["lastName"]
				if d not in outJson:
					outJson[d] = {}
				if t not in outJson[d]:
					outJson[d][t] = {}
                   
				if count not in outJson[d][t]:
                   
					outJson[d][t][count] = 0
				if count in outJson[d][t]:

					outJson[d][t][count] += 1
					outJson[d][t][fname] = lname
				if name not in outJson:
					outJson["namelist"] = [name]
					index += 1
				else:
					outJson[namelist][index] = name
		"""
               
		outJson["taskStatus"] = 1
		outJson["errorMsg"] = "somthing went wrong";
   
           
	#We print out some content type infor   
	print "Content-Type: text/html"
	print
	print """"""
   

	#We print out the html output string
	print json.dumps(outJson, indent=4)




if __name__ == '__main__':
    main()
