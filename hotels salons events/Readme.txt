Total 3 types of files are there:
1. totalPages.py   -----   creates a dictionary of total pages of each object(hotels, salons etc.) and saves that dictionary using json into a txt file.
2. zootout_restaurants.py, zootout_salons.py, zootout_hotels.py   ------   extracts attributes(url, address etc.) and their values and saves them into txt files.
3. postProcess.py  -----   processes txt files from 2nd step and saves data in another txt file

Note:-
These files should be compiled in order.


Things to be taken care of:
1. totalPages.py -
	a. The code written by the author only extracts cities of India. It can be modified using either of the two ways-
		(i). Line 15. Instead of "citybox india" it can be changed according to the country's code provided in the website.
		(ii). Before line 30 i.e. before "for city in cities:" cities dictionary can be hardcoded with city names.
	b. Enter the path of text file according to you. Line 90.

2. zootout_restaurants.py, zootout_salons.py, zootout_hotels.py - 
	a. Enter the path of text file according to you.

3. postProcess.py -
	a. Enter the path of text file according to you.
	b. Enter the attribute names in the search array at line 15.


For further querries write me at: himanshukharkwal765@gmail.com