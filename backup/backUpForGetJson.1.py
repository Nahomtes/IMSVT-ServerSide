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
	
	# making connection with MySQL server
	db_name = "church_DB"
	db_userid = "churchdbadmin"
	db_password = "pass123"
	db_host = "127.0.0.1" ## localhost
	dbh = MySQLdb.connect(host=db_host, user=db_userid, passwd = db_password, db = db_name)

	# inistialing email and time stamp from inJson
	
	serviceType = inJson["serviceType"]
	#print "service Type %s" % serviceType
	
	
	
	#
	if (serviceType == "lecture"):
		service_type_table_name = "lecture_service_table"
		service_type_id = lecture_table(dbh, inJson, email, time_stamp, service_type_table_name)

	elif (serviceType == "teach"):
		service_type_table_name = "teach_service_table"
		service_type_id = teach_table(dbh, inJson, email, time_stamp, service_type_table_name)
		
	elif (serviceType == "help"):
		service_type_table_name = "help_service_table"
		service_type_id = help_table(dbh, inJson, email, time_stamp, service_type_table_name)

	else: #(serviceType == "drive"):
		service_type_table_name = "drive_service_table"
		service_type_id = drive_table(dbh, inJson, email, time_stamp, service_type_table_name)
		
	individual_information_id = individual_information_table(dbh, inJson, email, time_stamp)



	sql = "INSERT INTO [%s] (%s, %s, %s) VALUE ('%s','%d','%d')" %("church_data_table", "service_type_table_name", "service_type_id","individual_information_id", service_type_table_name, service_type_id, individual_information_id)

	cur = dbh.cursor()
	cur.execute(sql)

	return 5
############################################
def lecture_table(dbh, inJson, email, time_stamp, service_type_table_name):

	 
	lecture_duration = inJson["serviceDuration"]
	service_date = inJson["serviceDay"]
	description = inJson["lectureTopic"]
	
	
	sql = "INSERT INTO [%s] (%s, %s, %s) VALUE ('%s','%s','%s')" %(service_type_table_name, "lecture_duration", "service_date","description",lecture_duration, service_date, description)

	cur = dbh.cursor()
	cur.execute(sql)

	return

#########################################
def teach_Table(dbh, inJson, email, time_stamp, service_type_table_name):
	
	
	student_age_group = inJson["studentAgeGroup"]
	service_date= inJson["serviceDay"]
	
	
	sql = "INSERT INTO [%s] (%s, %s) VALUE ('%s','%s')" %(service_type_table_name, "student_age_group", "service_date",student_age_group, service_date)

	cur = dbh.cursor()
	cur.execute(sql)	
	
	return 

#################################################
def help_table(dbh, inJson, email, time_stamp, service_type_table_name):
	
	holiday_name = inJson["serviceDay"]
	holiday_service= inJson["whichService"]
	
	
	sql = "INSERT INTO [%s] (%s, %s) VALUE ('%s','%s')" %(service_type_table_name, "holiday_name", "holiday_service",holiday_name, holiday_service)

	cur = dbh.cursor()
	cur.execute(sql)

	return

##################################################
def drive_table(dbh, inJson, email, time_stamp, service_type_table_name):
	
	available_seats = inJson["availableSit"]
	service_date= inJson["serviceDay"]
	
	# Make data to be inserted into the drive table only if the information that is in inJson like service_type_table_name, available_seats, service_date is different there should not be more than one row that is same as other row datas 
	
	sql = "SELECT %s FROM %s WHERE %s=%s AND %s=%s" %("drive_service_id", service_type_table_name, "available_seats", available_seats, "service_date", service_date)

	cur = dbh.cursor()
	cur.execute(sql)
	data = cur.fetchall()
	drive_service_id = 0
	if not data: # if has nothing in it 
	
		sql = "INSERT INTO [%s] (%s, %s) VALUE ('%s','%s')" %(service_type_table_name, "available_seats", "service_date", available_seats, service_date)

		cur = dbh.cursor()
		cur.execute(sql)

		sql2 = "SELECT %s FROM %s WHERE %s=%s AND %s=%s " %("drive_service_id", service_type_table_name, "available_seats", available_seats, "service_date", service_date)
		curr = dbh.cursor()
		curr.execute(sql2)
		drive_service_id = curr.fetchone() # this will return the id in this format (points,) = curr.fetchone()
		drive_service_id = drive_service_id[0]
		
		
	else:
		
		drive_service_id = data[0]
		
		# do nothing the data that you were about to enter already exist, it would be waste of memory to store two row of same data
	
	#sql2 = "SELECT %s FROM %s WHERE %s=%s AND %s=%s " %("drive_service_id", service_type_table_name, "available_seats", available_seats, "service_date", service_date)
	#curr = dbh.cursor()
	#curr.execute(sql2)
	#drive_service_id = curr.fetchone() # this will return the id in this format (points,) = curr.fetchone()
	#drive_service_id = drive_service_id[0]

	return drive_service_id
	#return

####################################################
def individual_information_table(dbh, inJson, email, time_stamp):
	table_name = "individual_information_table"
	first_name = inJson["firstName"]
	last_name= inJson["lastName"]
	telephone = inJson["telephone"]
	prefered_contact = inJson["contactPreference"] 
	zip_code = inJson["zipcode"]
	
	sql = "INSERT INTO [%s] (%s, %s, %s, %s, %s, %s, %s) VALUE ('%s', '%s', '%s', '%s', '%s', '%s', '%s')" %(table_name, "first_name", "last_name","telephone","email","prefered_contact","zip_code","time_stamp",first_name, last_name, telephone, email, prefered_contact, zip_code, time_stamp)

	cur = dbh.cursor()
	cur.execute(sql)
	return

##################################################
def saveSurveyNew(myObj, recordKey1, recordKey2):

	jsonFile = "/home/nahom/volunteerdb/newdatabase.json"
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
			saveSurveyNew(myObj, recordKey1, recordKey2)
			print "fffffffffffffff %d" % Main_save_data_into_church_data(myObj, recordKey1, recordKey2)
			outJson["taskStatus"] = 1
           
	elif inJson["pageid"] == "stat":
		jsonDb = {}
		jsonFile = "/home/nahom/volunteerdb/newdatabase.json"
		jsonText1 = open(jsonFile).read()   
		jsonDb = json.loads(jsonText1) # String to Oject (deserialization)
       
		index = 0
		outJson = {}   
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
