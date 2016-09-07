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
# TODO: Override night, if someone is in Bed earlier

_debug = 0 # 1 = true | 0 = false

# Local Variables
import datetime
from datetime import time

_todayDate = datetime.datetime.now()
if _debug: indigo.server.log("_todayDate: " + str(_todayDate.strftime('%Y-%m-%d')) , type="Nightmode")

#_todayTime = datetime.datetime.now().time().strftime('%H:%M')
_todayTime = datetime.datetime.now()

_tomorrowDate = _todayDate + datetime.timedelta(days=1)
if _debug: indigo.server.log("_tomorrowDate: " + str(_tomorrowDate.strftime('%Y-%m-%d')) , type="Nightmode")

# Define the values
_enableNightWeek = time(21,15).strftime('%H:%M')
_enableNightWE = time(21,15).strftime('%H:%M')
_disableNightWeek = time(8,00).strftime('%H:%M')
_disableNightWE = time(9,30).strftime('%H:%M')


if _debug: indigo.server.log("_todayTime: " + str(_todayTime.strftime('%H:%M')) , type="Nightmode")
if _debug: indigo.server.log("_enableNightWeek: " + str(_enableNightWeek) , type="Nightmode")
if _debug: indigo.server.log("_enableNightWE " + str(_enableNightWE) , type="Nightmode")
if _debug: indigo.server.log("_todayDate.weekday(): " + str(_todayDate.weekday()) , type="Nightmode")


if _debug:
    indigo.server.log("Debugging enabled", type="Nightmode")

if _debug:
    # Check if variable folder exist and creat it if needed
    if not ("nightmode" in indigo.variables.folders):
        indigo.variables.folder.create("nightmode");
        indigo.server.log("Variable folder 'nightmode' does not exist > create it.", type="Nightmode")

if _debug:
    if ("nightmode" in indigo.variables.folders):
        indigo.server.log("Variable folder 'nightmode' exist", type="Nightmode")


# Check if global variables exist or creat them if needed

# HolidayTomorrow
if not ("holidayTomorrow" in indigo.variables):
    indigo.variable.create("holidayTomorrow", value="false", folder="nightmode"); 
    indigo.server.log("Variable 'holidayTomorrow' does not exist > create it.", type="Nightmode")

# HolidayToday
if not ("holidayToday" in indigo.variables):
    indigo.variable.create("holidayToday", value="false", folder="nightmode"); 
    indigo.server.log("Variable 'holidayToday' does not exist > create it.", type="Nightmode")

# Night
if not ("night" in indigo.variables):
    indigo.variable.create("night", value="false", folder="nightmode"); 
    indigo.server.log("Variable 'night' does not exist > create it.", type="Nightmode")
    
holidayTomorrow = indigo.variables["holidayTomorrow"]
holidayToday = indigo.variables["holidayToday"]
night = indigo.variables["night"]
SleepingTempDelta_Simon = indigo.variables["SleepingTempDelta_Simon"]
SleepingTempDelta_Caro = indigo.variables["SleepingTempDelta_Caro"]


# Enable 'night' if tomorrow is a weekday
#if _todayTime.hour == 21 and _todayTime.minute == 15:
if _todayTime == _enableNightWeek:

	if _debug: indigo.server.log("**************************************", type="Nightmode")
	if _debug: indigo.server.log("Night: " + night.value, type="Nightmode")
	if _debug: indigo.server.log("Today: " + str(_todayTime), type="Nightmode")
	if _debug: indigo.server.log("Tomorrow: " + str(_tomorrowDate)+ "; tomorrow.weekday: " + str(_tomorrowDate.weekday()), type="Nightmode")
	if _debug: indigo.server.log("HolidayTomorrow: " + holidayTomorrow.value, type="Nightmode")
	if _debug: indigo.server.log("**************************************", type="Nightmode")

	# Tomorrow is a normal weekday
	if _tomorrowDate.weekday() in range(0,5) and holidayTomorrow.value == "false":
		indigo.variable.updateValue(night, value="true")
		indigo.server.log("Checking 'night'... Tomorrow is a weekday > enable 'night' now.", type="Nightmode")

    # Tomorrow is weekend or a holiday
	if _tomorrowDate.weekday() in range(5,7) or holidayTomorrow.value == "true":
		indigo.server.log("Checking 'night'... Tomorrow is weekend/holiday. Check again later.", type="Nightmode")


# Enable 'Night' if tomorrow is weekend or holiday
#if _todayTime.hour == 23 and _todayTime.minute == 59:
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
if _todayTime.weekday() in range(0,5) and holidayToday.value == "false":

	# Disable 'Night' 
	# if _todayTime.hour == 9 and _todayTime.minute == 00:
	if _todayTime == _disableNightWeek:
		indigo.server.log("Disable 'night' now.", type="Nightmode")
		indigo.variable.updateValue(night, value="false")

# Today is weekend or a holiday
if _todayTime.weekday() in range(5,7) or holidayToday.value == "true":
	
	# Disable 'Night' 
	#if _todayTime.hour == 10 and _todayTime.minute == 30:
	if _todayTime == _disableNightWE:
		indigo.server.log("Disable 'night' now.", type="Nightmode")
		indigo.variable.updateValue(night, value="false")
