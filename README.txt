
						    ###############################################
                                                    ###   VAIBHAV AGRAWAL 2014B3A7PS0501H       ###
                                                    ###   YASH BANSAL  2014A7PS0119H    	###
                                                    ###   SHIVAM AGRAWAL 2014B3A7PS0940H    	###
                                                    ###   AMAN GUPTA     2014A7PS0201H          ###
                                                    ###############################################
    

Files included in the package

-  CORPUS Files [docs folder]
-  porter.py
-  indexer.py

Requirements

- required python 3.0 or later
- nltk 
- linux , windows or mac OS



-----------------------------
PROCEDURE TO COMPILE AND RUN
-----------------------------

	1 ) ensure that you have nltk already downloaded on your system
		To do that run python Console or IDLE and type :
		
		import nltk
		nltk.download('punkt')
		
		This will download the require library packages
	
    2 ) Open indexer.py from the package
		Make sure that all the data-files and porter.py must be in the same folder as of indexer.py
		Run the program using F5 Key.
		
    3 ) User would be prompted to enter the queries one by one. When a query is entered , all 
		relevant documents are printed in the order of decreasing tf-idf value. This model is implemented
		on Rank Retrieval Vector Space Model.
	
------------------
EXAMPLE
------------------

Done indexing

Enter Query:  Ctrl+C to exit
sherlock

Showing results for:
sherlock
The results are:
1.      --> Document ID IS :: 4 and document name is : Lady Frances Carfax.txt
2.      --> Document ID IS :: 1 and document name is : Black Peter.txt
3.      --> Document ID IS :: 3 and document name is : His Last Bow.txt
4.      --> Document ID IS :: 2 and document name is : Charles Augustus Milverton.txt

Enter Query:  Ctrl+C to exit

Package Dependencies


		|-------------------------|             |------------|
                |     indexer.py          |------------>|  porter.py |
                |-------------------------|             |------------|

				
-----------------------
Word Frequency Analysis 
-----------------------

These were the steps to the process:
    1 ) run word-count on each essay
    2 ) record the frequency for each word in a dictionary data structure
    3 ) anaylze by comparing tf-idf values 




		