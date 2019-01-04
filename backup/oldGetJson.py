#!/usr/bin/env python
import os, sys
import cgi
import json


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
	if inJson["pageid"] == "home":
		if inJson["action"] == "getfirstpage":
			outJson = {
				"injson":inJson
				,"servicetype":{
				"lecture":"Give a lecture after church"
				,"teach":"Teach a class(young youth starting from 6-14 and older)"
				,"help":"Help on holiday\'s(such as helping with setting up food, cleaning or directing people to free parking spaces)"
				,"drive":"Volunteer to drive people who have no means of transportaion"
				}
			}
			outJson["taskStatus"] = 1
		elif inJson["action"] == "getsecondpage":
			if inJson["servicetype"] == "lecture":
				outJson = {
					"injson":inJson
					,"time":{ # change the name servicedurationobj
						"1/2hour":"half hour"
						,"1hour":"one hour"
						,"1&1/2hour":"one and half hour"
						,"2hour":"two hours"
					}
					,"whichSunday":{ # servicedayobj
                      				"first":"jan 1st 2018"
                        			,"eighth":"jan 8th 2018"
                        			,"seventeenth":"jan 17 2018"
                      				,"twentyforth":"jan 24 2018"
                    			}
           
               		 	}
                		outJson["taskStatus"] = 1

           
			elif inJson["servicetype"] == "teach":
				outJson = {
					"injson":inJson
					,"ageGroup":{
						"3-5oldclass":"3-5 years old class(10:30am-11:00am)"
						,"6-9oldclass":"6-9 years old class(10:30am-11:00am)"
						,"10-14oldclass":"10-14 years old class(10:20-11:40)"
						,"14&abv":"14 and above years old class(10:20-11:40)"
					}
					,"whichSunday":{
						"first":"jan 1st 2018"
						,"eighth":"jan 8th 2018"
						,"seventheenth":"jan 17 2018"
						,"twentyforth":"jan 24 2018"
					}
				}
				outJson["taskStatus"] = 1
               
			elif inJson["servicetype"] == "help":
				outJson = {
					"injson":inJson
					,"serviceDate":{
						"medhaneAlem":"Medhane Alem holiday"
						,"easter":"Easter Holiday"
						,"christmas":"Christmas"
					}
					,"whichService":{
						"Setting Up":"Setting up ahead of time"
						,"findParking":"helping people find parking spots"
						,"cleaning":"Cleaning up"
					}
				}
				outJson["taskStatus"] = 1
           
           
			elif inJson["servicetype"] == "drive":
				outJson = {
					"injson":inJson
					,"whichSunday":{
						"first":"jan 1st 2018"
						,"eighth":"jan 8th 2018"
						,"seventheenth":"jan 17 2018"
						,"twentyforth":"jan 24 2018"
					}
					,"numberOfPeople":{
						"one":"One available sit"
						,"two":"Two available sits"
						,"three":"Three available sits"
						,"four":"Four avilable sits"
					}
				}
				outJson["taskStatus"] = 1
			elif inJson["servicetype"] == "":
				outJson["errorMsg"] = "service type not selected";
		elif inJson["action"] == "getthirdpage":
			outJson = {
				"injson":inJson
				,"format":["name","type","placeholder"]   
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
			outJson = {
				"injson":"inJson"
			}
			outJson["taskStatus"] = 1

	elif inJson["pageid"] == "stat":
		outJson = {

		}
		outJson["errorMsg"] = "statitics curently under constraction";
   
           
	

	#We print out the html output string
	print json.dumps(outJson, indent=4)



if __name__ == '__main__':
    main()
