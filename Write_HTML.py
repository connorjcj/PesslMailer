#import codecs

#EMFile = codecs.open('Service Alert Email.html', 'r')

#content = EMFile.read()

#EMFile.close()

html = """

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
 <head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
  <title>Carrfields Pessl Alert</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
</head>
</html>
<body style="margin: 0; padding: 0;">
<table border="0" cellpadding="0" cellspacing="0" width="100%" style="padding: 25px 0 0px 0;">
 <table align="center" border="0" cellpadding="." cellspacing="0" width=620 style="border: 1px solid #cccccc; padding: 5px 0 0px 0;">
  <tr>
   <td style="padding: 10px 0 10px 0;">
    <table align="center" border="0" cellpadding="0" cellspacing="0" width=600 style="border-collapse: collapse;">
 	 <tr>
  	 <td>
   	  <table align="center" border="0" cellpadding="0" cellspacing="0" width="100%">
 		<tr>
  		<td width=55% style="padding: 0px 0px 0px 10px; color: #000000; font-family: Open Sans, sans-serif; font-size: 33px;"">
   		 <b><i>Service Alert</i></b>
  		</td>
  		<td align="right" width=30% style="padding: 0px 5px 0px 0;">
   		 <img src="http://www.carrfields.co.nz/wp-content/uploads/2015/11/CARRFIELDS-LOGO.png" alt="Carrfields" width="100%">
  		</td>
		<td align="center" style="padding: 0px 0px 0px 5px;">
		 <img src="http://www.pesslinstruments.com/wp-content/uploads/2016/01/logoPIweb-1-e1481460010230-300x137.png" alt="Pessl" width="100%">
  		</td>
		<td style="padding: 0px 0 0px 0;">
  		</td>
 		</tr>
	  </table>
  	 </td>
 	 </tr>
	 <table align="center" border="0" cellpadding="0" cellspacing="0" width=600 style="border-collapse: collapse;">
 	 <tr>
  	 <td align="center" style="padding: 35px 0 15px 10px; color: #000000; font-family: Open Sans, sans-serif; font-size: 18px;"">
	  <svg height="3" width="600">
  		<line x1="50" y1="0" x2="550" y2="0" style="stroke:#A7D500;stroke-width:3" />
	  </svg>
"""

html2 = """
	  <svg height="3" width="600">
  		<line x1="50" y1="3" x2="550" y2="3" style="stroke:#A7D500;stroke-width:3" />
	  </svg>
  	 </td>
 	 </tr>
	 </table>
	 <table align="center" border="0" cellpadding="0" cellspacing="0" width="600" style="border-collapse: collapse;">
 	 <tr>
  	 <td align="center" style="padding: 15px 0 15px 0;">
	 <table border="0" cellpadding="0" cellspacing="0" width="100%">
 		<tr>
  		<td style="padding: 5px 0px 5px 0px;">
   			<table align="center" border="0" cellpadding="0" cellspacing="0" width=290 style="border-collapse: collapse;">
 	 		<tr>
  	 		<td align="center" style="padding: 0px 0 0px 0;">
				<table align="left" border="0" cellpadding="0" cellspacing="0" width=50 style="border-collapse: collapse;">
					<tr>
  	 				<td align="center" style="padding: 4px 0px 4px 0px;">
						<img src="https://static.dpaw.wa.gov.au/static/libs/ionicons/1.2.2/src/icon-wifi.svg"  width="38" height="38"/>
					</tr>
					</td>
					<tr>
  	 				<td align="center" style="padding: 4px 0px 4px 0px;">
						<img src="https://static.dpaw.wa.gov.au/static/libs/ionicons/1.2.2/src/icon-battery-charging.svg"  width="38" height="38"/>
					</tr>
					</td>
					<tr>
  	 				<td align="center" style="padding: 3px 0px 3px 0px;">
						<img src="https://static.dpaw.wa.gov.au/static/libs/ionicons/1.2.2/src/icon-ios7-sunny.svg"  width="40" height="40"/>
					</tr>
					</td>
					<tr>
  	 				<td align="center" style="padding: 3px 0px 3px 0px;">
						<img src="https://static.dpaw.wa.gov.au/static/libs/ionicons/1.2.2/src/icon-ios7-rainy.svg"  width="40" height="40"/>
					</tr>
					</td>
					<tr>
  	 				<td align="center" style="padding: 3px 0px 3px 0px;">
						<img src="https://static.dpaw.wa.gov.au/static/libs/ionicons/1.2.2/src/icon-leaf.svg"  width="40" height="40"/>
					</tr>
					</td>
					<tr>
  	 				<td align="center" style="padding: 8px 0px 8px 0px;">
						<img src="https://static.dpaw.wa.gov.au/static/libs/ionicons/1.2.2/src/icon-information-circled.svg"  width="35" height="35"/>
					</tr>
					</td>
					<tr>
  	 				<td align="center" style="padding: 5px 0px 5px 0px;">
						<img src="https://static.dpaw.wa.gov.au/static/libs/ionicons/1.2.2/src/icon-ios7-location.svg"  width="40" height="36"/>
					</tr>
					</td>
				<tr>
				<table align="right" border="0" cellpadding="0" cellspacing="0" width=230 height=47 style="border-collapse: collapse;">
					<td align="left" style="padding: 5px 0 5px 0px; color: #000000; font-family: Open Sans, sans-serif; font-size: 12px;">
						<b>Connection</b>"""
                       
html3 =					"""</td>
				</table>
				<table align="right" border="0" cellpadding="0" cellspacing="0" width=230 height=47 style="border-collapse: collapse;">
					<td align="left" style="padding: 5px 0 5px 0px; color: #000000; font-family: Open Sans, sans-serif; font-size: 12px;">
						<b>Battery</b>"""
                       
html4 =					"""</td>
				</table>
				<table align="right" border="0" cellpadding="0" cellspacing="0" width=230 height=47 style="border-collapse: collapse;">
					<td align="left" style="padding: 5px 0 5px 0px; color: #000000; font-family: Open Sans, sans-serif; font-size: 12px;">
						<b>Solar panel</b>"""

html5 =					"""</td>
				</table>
				<table align="right" border="0" cellpadding="0" cellspacing="0" width=230 height=47 style="border-collapse: collapse;">
					<td align="left" style="padding: 5px 0 5px 0px; color: #000000; font-family: Open Sans, sans-serif; font-size: 12px;">
						<b>Rain Bucket</b>"""

html6 =					"""</td>
				</table>
				<table align="right" border="0" cellpadding="0" cellspacing="0" width=230 height=47 style="border-collapse: collapse;">
					<td align="left" style="padding: 5px 0 5px 0px; color: #000000; font-family: Open Sans, sans-serif; font-size: 12px;">
						<b>Leaf Wetness</b>"""

html7 =					"""</td>
				</table>
				<table align="right" border="0" cellpadding="0" cellspacing="0" width=230 height=47 style="border-collapse: collapse;">
					<td align="left" style="padding: 5px 0 5px 0px; color: #000000; font-family: Open Sans, sans-serif; font-size: 12px;">
						<b>Temperature</b>"""

html8 =					"""</td>
				</table>
				<table align="right" border="0" cellpadding="0" cellspacing="0" width=230 height=47 style="border-collapse: collapse;">
					<td align="left" style="padding: 5px 0 5px 0px; color: #000000; font-family: Open Sans, sans-serif; font-size: 12px;">
						<b>GPS Location</b>"""

html9 =					"""</td>
				</table>
					</tr>
				</table>	
  	 		</td>
  	 		</td>
 	 		</tr>
			</table>
		   </td>
  		<td style="padding: 5px 0px 5px 0px;">
   			<table align="center" border="0" cellpadding="0" cellspacing="0" width=290 style="border-collapse: collapse;">
 	 		<tr>
  	 		<td align="center" style="padding: 10px 0 0px 0;">
				<img src="https://maps.googleapis.com/maps/api/staticmap?center="""
                
html10 =                "&zoom=13&size=300x300&maptype=hybrid&markers=size:small%7color:red%7C"
                
html11 =                """"&key=\"AIzaSyD5Kpu5_-a0jEGrembulV-LN3udaF4jlws\">"
    	 	</tr>
			<tr>
  	 		<td align="center" style="padding: 3px 0 0px 0;font-family: Open Sans, sans-serif; font-size: 12px;">
				<a href="https://maps.google.com?saddr=Current+Location&daddr="""
                
html12 =                """" style="color: #009A17;"><font color="#009A17">Get Directions</font></a>
 	 		</tr>
			</table>
  		</td>
  		</td>
 		</tr>
  	 </td>
 	 </tr>
	 </table>
	 </td>
	 </tr>	 
	</table>
   </td>
  </tr>
 </table>
</body>



""" 

StationID = "01204E68"
StationDes = "River Road Pump Shed"
gps_lat = "-43.975514"
gps_lon = "171.785150"

def send_email(sensor_trigger):
    '''sensor_trigger format: {'Connection': False, 'Battery': False, 'Solar': False, 'Rain': False,
    'Leaf Wetness': False, 'Temp': False, 'GPS': False}'''

    if (sensor_trigger['Connection'] == True):
        sensor_c = "<font color=\"red\"> - Has not communicated in last 24 hours.</font>"
    else:
        sensor_c = " - No issues detected."

    if (sensor_trigger['Battery'] == True):
        sensor_b = "<font color=\"red\"> - Voltage has remained below 6050mV for last 24hrs.</font>"
    else:
        sensor_b = " - No issues detected."

    if (sensor_trigger['Solar'] == True):
        sensor_s = "<font color=\"red\"> - Output is consistently 15% less than rel solar radiation.</font>"
    else:
        sensor_s = " - No issues detected."

    if (sensor_trigger['Rain'] == True):
        sensor_r = "<font color=\"red\"> - Blockage suspected.</font>"
    else:
        sensor_r = " - No issues detected."

    if (sensor_trigger['Leaf Wetness'] == True):
        sensor_l = "<font color=\"red\"> - Behaviour does not match rain bucket records in last 24hrs.</font>"
    else:
        sensor_l = " - No issues detected."

    if (sensor_trigger['Temp'] == True):
        sensor_t = "<font color=\"red\"> - Average not within expected range.</font>"
    else:
        sensor_t = " - No issues detected."

    if (sensor_trigger['GPS'] == True):
        sensor_g = "<font color=\"red\"> - Location has moved.</font>"
    else:
        sensor_g = " - No issues detected."

    # Not yet used
    if (sensor_trigger['Wind'] == True):
        sensor_w = "<font color=\"red\"> - Wind sensor obstructed/disconnected.</font>"
    else:
        sensor_w = " - No issues detected."


    html_final = html + "\t   Daniel Lovett - %s - %s" % (StationID,StationDes) + html2 + sensor_c + html3 + sensor_b \
                 + html4 + sensor_s + html5 + sensor_r + html6 + sensor_l + html7 + sensor_t + html8 + sensor_g + html9 \
                 + gps_lat + "," + gps_lon + html10 + gps_lat + "," + gps_lon + html11 + gps_lat + "," + gps_lon + html12
    #print(html3)

    EMFile = open('Service Alert EmailTest.html', 'w')

    EMFile.write(html_final)

    EMFile.close()

    return html_final
