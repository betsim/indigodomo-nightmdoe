# -*- coding: utf-8 -*-

#-----------------------------------------------------------------------------#
# Enable 'Night'-mode depending on weekday and holiday
#
# Autor: Simon Betschmann
# Version: 1.3
# Date: 7.09.2016
#
# .weekday(): Monday=0 .. Sunday=6   | range(5,7) = 5 and 6
#-----------------------------------------------------------------------------#


# TODO: Exception if Caro has Nachtdienst

# Debuging (1 = true | 0 = false)
_debug = 0
if _debug: indigo.server.log("Debugging enabled", type="Nightmode")
    
# Local Variables
import datetime
from datetime import time

# Define the values
_NachtdienstCaro = 0
_enableNightWeek = time(18,39).strftime('%H:%M')
_enableNightWE = time(21,15).strftime('%H:%M')
_disableNightWeek = time(18,41).strftime('%H:%M')
_disableNightWE = time(9,30).strftime('%H:%M')

_todayDate = datetime.datetime.now()
_todayTime = datetime.datetime.now().strftime('%H:%M')
_tomorrowDate = _todayDate + datetime.timedelta(days=1)

if _debug: indigo.server.log("" , type="Nightmode")
if _debug: indigo.server.log("**************************************" , type="Nightmode")
if _debug: indigo.server.log("Today: " + str(_todayDate.strftime('%Y-%m-%d')) , type="Nightmode")
if _debug: indigo.server.log("Tomorrow: " + str(_tomorrowDate.strftime('%Y-%m-%d')) + " (weekday: " + str(_tomorrowDate.weekday()) + ")", type="Nightmode")
if _debug: indigo.server.log("Actual time: " + str(_todayTime) , type="Nightmode")
if _debug: indigo.server.log("Enable 'nightmode' on a weekday at: " + str(_enableNightWeek) , type="Nightmode")
if _debug: indigo.server.log("Enable 'nightmode' on weekends at " + str(_enableNightWE) , type="Nightmode")
if _debug: indigo.server.log("Actual weekday: " + str(_todayDate.weekday()) , type="Nightmode")

# Check if variable folder exist and creat it if needed
if not ("nightmode" in indigo.variables.folders):
    indigo.variables.folder.create("nightmode");
    indigo.server.log("Variable folder 'nightmode' does not exist > created it.", type="Nightmode")

if ("nightmode" in indigo.variables.folders):
    if _debug: indigo.server.log("Variable folder 'nightmode' already exists... nothing to do.", type="Nightmode")


# Check if global variables exist or creat them if needed
# HolidayTomorrow
if not ("holidayTomorrow" in indigo.variables):
    indigo.variable.create("holidayTomorrow", value="false", folder="nightmode"); 
    indigo.server.log("Variable 'holidayTomorrow' does not exist > created it.", type="Nightmode")

# HolidayToday
if not ("holidayToday" in indigo.variables):
    indigo.variable.create("holidayToday", value="false", folder="nightmode"); 
    indigo.server.log("Variable 'holidayToday' does not exist > created it.", type="Nightmode")

# Night
if not ("night" in indigo.variables):
    indigo.variable.create("night", value="false", folder="nightmode"); 
    indigo.server.log("Variable 'night' does not exist > created it.", type="Nightmode")

# Global variables
holidayTomorrow = indigo.variables["holidayTomorrow"]
holidayToday = indigo.variables["holidayToday"]
night = indigo.variables["night"]
SleepingTempDelta_Simon = indigo.variables["SleepingTempDelta_Simon"]
SleepingTempDelta_Caro = indigo.variables["SleepingTempDelta_Caro"]


# Enable 'night' if tomorrow is a weekday
if _todayTime == _enableNightWeek:

	if _debug: indigo.server.log("Nightmode: " + night.value, type="Nightmode")
	if _debug: indigo.server.log("HolidayTomorrow: " + holidayTomorrow.value, type="Nightmode")

	# Tomorrow is a normal weekday
	if _tomorrowDate.weekday() in range(0,5) and holidayTomorrow.value == "false":
		indigo.variable.updateValue(night, value="true")
		indigo.server.log("Checking 'night'... Tomorrow is a weekday > enable 'night' now.", type="Nightmode")

    # Tomorrow is weekend or a holiday
	if _tomorrowDate.weekday() in range(5,7) or holidayTomorrow.value == "true":
		indigo.server.log("Checking 'night'... Tomorrow is weekend/holiday. Check again later.", type="Nightmode")


# Enable 'Night' if tomorrow is weekend or holiday
if _todayTime == _enableNightWE:

	if _debug: indigo.server.log("**************************************", type="Nightmode")
	if _debug: indigo.server.log("night: " + night.value, type="Nightmode")
	if _debug: indigo.server.log("today: " + str(_todayTime), type="Nightmode")
	if _debug: indigo.server.log("tomorrow: " + str(_tomorrowDate)+ "; tomorrow.weekday: " + str(_tomorrowDate.weekday()), type="Nightmode")
	if _debug: indigo.server.log("holidayTomorrow: " + holidayTomorrow.value, type="Nightmode")
	if _debug: indigo.server.log("**************************************", type="Nightmode")

	# Tomorrow is weekend or a holiday
	if _tomorrowDate.weekday() in range(5,7) or holidayTomorrow.value == "true":
		indigo.server.log("Checking 'night'... Tomorrow is weekend/holiday > enable 'night' now.", type="Nightmode")
		indigo.variable.updateValue(night, value="true")

# Today is a normal weekday
if _todayDate.weekday() in range(0,5) and holidayToday.value == "false":

	# Disable 'Night' 
	if _todayTime == _disableNightWeek:
		indigo.server.log("Disable 'night' now.", type="Nightmode")
		indigo.variable.updateValue(night, value="false")

# Today is weekend or a holiday
if _todayDate.weekday() in range(5,7) or holidayToday.value == "true":
	
	# Disable 'Night' 
	if _todayTime == _disableNightWE:
		indigo.server.log("Disable 'night' now.", type="Nightmode")
		indigo.variable.updateValue(night, value="false")

if _debug: indigo.server.log("**************************************", type="Nightmode")
if _debug: indigo.server.log("" , type="Nightmode")