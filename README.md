## **LAB 05**


## **SUBMISSION INSTRUCTIONS**

- [x] 0.) Submit | python file using the naming convention below (replace JaneDoe with your first and last name respectively):
	* e JaneDoeS.py
	
	
## **QUESTION**

- [x] 1.) Create a folder named files then download and store input.txt in it.

- [x] 2.) Ask the user for the input file name (use exceptions to deal with a missing file).

- [x] 3.) Once the right file name is provided, create an output file named output.csv.

  - [x] a.) This file should also be stored in the files folder.

  - [x] b.) Please note, before you store output.csv in the files folder, you need to check if there already exists a file with that name in the folder. Use the os.path module (not exception handling) to check if the file already exists. If it does, ask the user if they want to overwrite it or if they would prefer creating a different output file (refer to sample output for the logic). 
		
      * Regarding the os module, the code below is enough to get you started.
    
    > ‘import os.path  
	> if os.path.isfile("Presidents. txt"):  
	> print("Presidents.txt exists")  

	* Here isfile('"Presidents.txt") returns True if the file Presidents.txt exists in the current directory.
	
  - [x] c.) If no file exists with the name output.csv, anew file with that name should be created. If the file already exists, ask the user if they want to overwrite it. If they select y for yes, you can use thew file mode to overwrite the file. If they select n for no, ask them for anew output file name. 
	
- [x] 4.) Once the output.csv file is successfully created, create a header row in it with the headers: Email, Time, and Confidence.

- [x] 5.) Go through the lines in input.txt looking for lines that begin with (please note the  colons are part of the text)

  > source@collab.sakaiproject.org  
  > From: stephen.marquard@uct.ac.za  
  > Subject: [sakai] svn commit: r39772 - content/branches/sakai_2-5-x/content-impl/impl/src/java/org/sakaiproject|  
  > x-Content-Type-Outer-Envelope: text/plain; charset=UTF-8  
  > X-Content-Type-Message-Body: text/plain; charset=UTF-8  
  > X-content-Type: text/plain; charset=UTF-8  
  > X-DSPAM-Result: Innocent  
  > X-DSPAM-Processed: Sat Jan 5 09:14:16 2008  
  > X-DSPAM-Confidence: @.8475  
  > X-DSPAM-Probability: @.e000  
	
  - [x] a.) From: - Extract the email address (e.g., stephen.marquard@uct.ac.za)

  - [x] b.) X-DSPAM-Processed: - Extract the time value (e.g., 09:14:16)

  - [x] c.) X-DSPAM-Confidence: - Extract the numeric value (e.g., 0.8475)
	
- [x] 6.) Send the results obtained in (d) to output.csv for each occurrence of the 3 items in input.txt.

- [x] 7.) The contents of your output.csv file should be identical to sample.csv when your program is done

	* (please note the last row contains the average X-DSPAM-Confidence).

- [x] 8.) Once all the data is sent to output.csv, print Data stored! to the console to let users know your program is done.

## Please note:

- [x] 9.)  Write your program asa script (i.e., include the if__name block).
	
- [x] 10.) Strip input when getting the file name (do not lower). There are some OS systems that are case sensitive with file names so make sure you don’t change the case of the file name entered (only strip file name input).

- [x] 11.) Your program should be able to work if the input and output file names were different.

- [x] 12.) Don’t forget to close any files you open.

- [x] 13.) Feel free to use functions to organize your code.
	
	
#### SAMPLE OUTPUT1

> Input file name: input.txt  
> Output file name: output.csv  
> Data stored!  

* NOTE: The assumption in this scenario is that you didn’t have output.csv in your files
folder so this is the first time it’s being created.
	
	
#### SAMPLE OUTPUT 2

> Input file name: input.txt  
> Output file name: output.csv  
> Overwrite existing file (y/n): Y  
> Data stored!  

* NOTE: The assumption in this scenario is that you already had a file named output.csv in your files folder but you are choosing to delete its previous content and send new data to it.
	
	
#### SAMPLE OUTPUT 3

> Input file name: test.txt  
> File does not exist!  
> Input file name: input  
> File does not exist!  
> Input file name:  
> ==  
> ‘main”:>  
> input.txt  
> Output file name: output.csv  
> Overwrite existing file (y/n): x  
> Enter (y/n): a  
> Enter (y/n): N  
> New output file name: output.csv  
> Overwrite existing file (y/n): n  
> New output file name: test.csv  
> Data stored!  

* NOTE: The assumption in this scenario is that you already hada file named output.csv in your files folder and are choosing to send your data to a new csv file named test.csv because you don’t want to overwrite your output.csv file.
