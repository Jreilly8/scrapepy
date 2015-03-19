#!/usr/bin/env python
import sys
import re
import requests
import csv

'''
Scraper for otherwise irritating information necessary for our seasonal sales

Note that this script requires python 2.x and the requests module, neither
guarenteed to be on the server.

This script creates a csv with the necessary information to generate the sale
page html. It is mostly a regular expression based scraper. 
Neither this script nor genhtml.php actually modifies the internal x-cart
pricing.
The regex & matches will have to be updated for your use
'''

''' Initialize csv objects '''
# change these filenames as appropriate
ifile = "list.csv"
ofile = "output.csv"
csvi = open(ifile, 'r')
csvo = open(ofile, 'w')
reader = csv.reader(csvi, delimiter=',', quotechar='"')
writer = csv.writer(csvo, delimiter=',', quotechar='"')

''' Compiled regular expressions '''
# internal display name, taken from url. used for output csv and html comments for readability
# the URL
the_url = "http://url.com/path/to/cart"
re_name = re.compile(r"the_url(.*)\.html", re.IGNORECASE | re.MULTILINE)

# actual product id
re_productid = re.compile(r'name="productid" value="(\d+?)"', re.IGNORECASE | re.MULTILINE)

# actual product price
#re_price = re.compile(r'id="product_price">(\d+?)<', re.IGNORECASE | re.MULTILINE)

# thumbnail image url
re_img = re.compile(r'<div id="timp-art">\s*<img src=".(.+?)" alt="" />', re.IGNORECASE | re.MULTILINE)

# variant and option id for DVD, if available. Relies on proper SKU to find
re_dvd = re.compile(r"variants\[\d+\] = \[\[(.*?),.*?,.*?,.*?,.*?,'(.*?-VF-.*?)'.*?;(?:\s|\r\n)*variants\[.*?\]\[.*?\]\[(\d+?)\] = (\d+?);", re.IGNORECASE | re.MULTILINE)

# variant and option id for DTO, if available. Relies on proper SKU to find
re_dto = re.compile(r"variants\[\d+\] = \[\[(.*?),.*?,.*?,.*?,.*?,'(.*?-EF-.*?)'.*?;(?:\s|\r\n)*variants\[.*?\]\[.*?\]\[(\d+?)\] = (\d+?);", re.IGNORECASE | re.MULTILINE)

# variant and option id for HD DTO, if available. Relies on proper SKU to find
#re_hddto = re.compile(r"variants\[\d+\] = \[\[(.*?),.*?,.*?,.*?,.*?,'(.*?HD-EF-.*?)'.*?;(?:\s|\r\n)*variants\[.*?\]\[.*?\]\[(\d+?)\] = (\d+?);", re.IGNORECASE | re.MULTILINE)


''' Main loop '''
for row in reader:
	(title, avail, url, sale_section, price) = row

	# grab the entire html document from cart
	r = requests.get(url)
	text = r.text

	# get sluggy name of movie from URI
	name = re_name.search(url).group(1)

	# scrape product id
	productid = re_productid.search(text).group(1)

	# scrape product id

	#price = re_price.search(text).group(1)

	# scrape image url
	img = 'the_url%s' % (re_img.search(text).group(1))

	# scrape dvd-specific variant and option ids
	match = re_dvd.search(text)
	if match:
		dvdsku = match.group(2)
		dvdvar1 = match.group(3)
		dvdvar2 = match.group(4)
	else:
		dvdsku = "NONE"
		dvdvar1 = "NONE"
		dvdvar2 = "NONE"

	# scrape dto-specific variant and option ids
	match = re_dto.search(text)
	if match:
		dtosku = match.group(2)
		dtovar1 = match.group(3)
		dtovar2 = match.group(4)
	else:
		dtosku = "NONE"
		dtovar1 = "NONE"
		dtovar2 = "NONE"
	# scrape HDdto-specific variant and option ids
	#match = re_hddto.search(text)
	#if match:
		#hddtosku = match.group(2)
		#hddtovar1 = match.group(3)
		#hddtovar2 = match.group(4)
	#else:
		#hddtosku = "NONE"
		#hddtovar1 = "NONE"
		#hddtovar2 = "NONE"

	# write this row to file
	outrow = [name, avail,  price, productid, url, img, dvdvar1, dvdvar2, dtovar1, dtovar2, sale_section]
	print outrow
	writer.writerow(outrow)

# main loop done, close files
csvi.close()
csvo.close()
