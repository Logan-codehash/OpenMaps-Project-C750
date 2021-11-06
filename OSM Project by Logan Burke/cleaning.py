import re
import unicodedata

#checking for correct format
phone_num =re.compile(r'[4,9][0-9]{2}-[0-9]{3}-[0-9]{4}$')
post_code =re.compile(r'[7][0-9]{4}$')

#for correcting typos and standardization 
mapping_addr = { "St" : "Street",
			"St." : "Street",
			"Ave" : "Avenue",
			"Rd" : "Road",
			"Road" : "Road",
			"road" : "Road",
			"cross" : "Cross", 
			"ROad" : "Road", 
			"ROAD" : "Road",
			"Dr" : "Drive",
			"Blvd" : "Boulevard",
			"Ct" : "Court",
			"Ln" : "Lane",
			"Hwy" : "Highway",
			"Cir" : "Circle",
			"Pky" : "Parkway",
			"Trl" : "Trail",
			"Pl" : "Place",
			"Sq" : "Square",
			"Cv" : "Cove",
			"Trce" : "Terrace",
			}
mapping_city = { "longview" : "Longview",
				 "long view" : "Longview",
				 "Long view" : "Longview",
				 "Long View" : "Longview",
				 "lakeport" : "Lakeport",
				 "hallsville" : "Hallsville",
				 "kilgore" : "Kilgore",
				 "WhiteOak" : "White Oak",
				 "whiteoak" : "White Oak",
				 "white oak" : "White Oak",
				 "diana" : "Diana",
				 "gilmer" : "Gilmer",
			}
direction_addr = {"N" : "North",
			"S" : "South",
			"E" : "East",
			"W" : "West",
			"N." : "North",
			"S." : "South",
			"E." : "East",
			"W." : "West"
			}
misc_street_names = {"H G Mosley Parkway" : "H.G. Mosley Parkway",
			"P T Parkway" : "P.T. Parkway"
			}
street_num ={"1st" : "First",
			"2nd" : "Second",
			"3rd" : "Third",
			"4th" : "Forth",
			"5st" : "Fifth",
			"6th" : "Sixth",
			"7th" : "Seventh",
			"8th" : "Eighth",
			"9th" : "Ninth",
			"10th" : "Tenth",
			"11th" : "Eleventh",
			"12th" : "Twelfth",
			"13th" : "Thirteenth",
			"14th" : "Fourteenth",
			"15th" : "Fifteenth"
			}

#function for updating the names of streets
def update_addr_name(name):
	newname = ""
	#correct street name using misc_street_names dict
	if name in misc_street_names:
		for key,val in misc_street_names.iteritems():
			name = name.replace(key,val)
	if name.split()[0] in direction_addr:
		for key,val in direction_addr.iteritems():
			name = name.replace(key,val)
	#corrects 1st to First and such
	name_list = name.split()
	for items in name_list:
		if items in street_num:
			for key,val in street_num.iteritems():
				name = name.replace(key,val)
	last_word = name.split()[-1]
	if last_word in mapping_addr:
		#get the words except the last one
		for n in range(len(name.split())-1):
			newname += name.split()[n]
			newname += ' '
		newname += mapping_addr[last_word]
		return newname
	else:
		return name

#function for updating city name
def update_city_name(name):
	new_name = ""
	if name in mapping_city: 
		new_name = mapping_city[name]
		return repr(new_name)
	else:
		return repr(name)

#function for correcting postcodes
def update_postcode(postcode):
	if postcode.split()[0] == 'TX':
		return postcode.split()[1]
	elif len(postcode) == 5:
		clean_code = re.findall(r'(\d{5})', postcode)
		if clean_code:
			return clean_code[0]
		else:
			return ("invalid")
	#makes sure postcode is correct format
	elif len(postcode) == 10:
		clean_code = re.findall(r'^(\d{5})-(\d{4})$', postcode)[0]
		if clean_code:
			return clean_code[0]
		else:
			return ("invalid")
	else:
		return ("invalid")

#fixes speed limit mph error
def speedlimit(mph):
	if 'mph' in mph:
		return mph
	else:
		return (mph+' mph')

#function for correcting phone numbers
def update_phone(phonenum):
	if phone_num.match(phonenum):
		return phonenum
	else:
		new_num = ''
		count = 0
		for i in range(len(phonenum)):
		#structures the phone number correctly
			if (phonenum[i] in ['4','9']) and count == 0:
				new_num += "("
				new_num += phonenum[i]
				count += 1
			elif (count > 0) and (count <= 12):
				if phonenum[i].isalnum():
					new_num += phonenum[i]
					count += 1
					if count == 3:
						new_num += ") "
					if count == 6:
						if new_num[6].isdigit():
							new_num += "-"
	if len(new_num) > 9 and len(new_num) <= 14:
		return new_num	  
	else:
		return ('Invalid phone number')