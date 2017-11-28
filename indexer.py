"""

This project has been created by:

                                                    ###############################################
                                                    ###   VAIBHAV AGRAWAL 2014B3A7PS0501H       ###
                                                    ###   YASH BANSAL  2014A7PS0119H    	    ###
                                                    ###   SHIVAM AGRAWAL 2014B3A7PS0940H    	###
                                                    ###   AMAN GUPTA     2014A7PS0201H          ###
                                                    ###############################################



The proposed query search engine has been employed using "Vector Space model".

Version of python used = python 3.5.2

The major data structures used in the project are:

Dictionaries / HashMaps
List
String

The code consists of two files namely porter.py and indexer.py.

"""

doc_to_int = {}
import sys
import os
reload(sys)
sys.setdefaultencoding('utf8')

import copy
import porter
import nltk
import csv
import os
import pydoc



NO_OF_DOC = 0



############################################### INDEXING MODULE #######################################################################

dic={} # Dictionary data structure holding the index data
idf={} # Dictionary data structure holding IDF of words
mag={} # |document|
doc={}
N=0 # size of corpus
def test1():
    '''
        test1() is a helper function which computes the tf-idf values of the resulting index
    '''
    global NO_OF_DOC
    N= NO_OF_DOC
    computeTF_IDF(N)

def index(l):
    '''
        index(l) accepts a parameter l which is of type list.
        It would help to put the new words in the dictionary and increase the frequency of the previously occured words in the dictionary.
        The time complexity of this function depends on the dictionary data structure.
        Average case - O(1)/insertion
        Worst case - O(length of list)/insertion
    '''
    n=len(l) # find length of document
    ID=l[0]
    doc[ID]=set([])
    for i in range(1,n):
        word=l[i] # word in document
        doc[ID].add(word)
        if(word in dic):
            if(ID in dic[word]): # l[0] stores the document ID
                dic[word][ID]+=1 # update term frequency of word in document l[0]
            else:
                dic[word][ID]=1  # insert document with ID l[0] and make term frequency of word in doc=1
        else:
            dic[word] = {ID:1} # insert word in dic and insert doc ID l[0] in posting list and freq of word in l[0]=1

    #print dic


def computeTF_IDF(N):
    '''
        computeTF_IDF(N)
        It has N as a parameter. This N is the number of documents available in corpus.
        This function helps calculating the tf-idf values of all the words in our index. This would help us later
        to figure out the most relevant documents in the corpus.
        Math library has been used to implemnt the logarithmic functions.
    '''
    import math
    for i in dic:
        n=len(dic[i]) # DF
        IDF=1+math.log(N/n,2) # IDF = log(N/df,2)
        idf[i]=IDF
        for j in dic[i]:
            dic[i][j]=(1+math.log(dic[i][j],2))*IDF # TF*IDF
            if(j in mag):
                mag[j]+=dic[i][j]*dic[i][j]
            else:
                mag[j]=dic[i][j]*dic[i][j]


############################################### END OF INDEXER ########################################################################






############################################### QUERYING MODULE #######################################################################


qdic={}
result={}
magq=0
h=[]

def getQueryTF_IDF():
    '''
        getQueryTF_IDF()
        This function also calculates the tf-idf value, but for the query string only.
        Math library has been used to implemnt the logarithmic functions.

    '''
    import math
    n=len(q)
    for i in q:
        if(i in qdic):
            qdic[i]+=1
        else:
            qdic[i]=1
    for i in qdic:
        if(i in idf):
            qdic[i]=(1+math.log(qdic[i],2))*idf[i]
    global magq
    for i in qdic:
        magq+=qdic[i]*qdic[i]



############################################### END OF QUERYING MODULE #######################################################################


def levenshtein(s1, s2):
    '''
        levenshtein(s1, s2) computes the edit distance between two strings
        The following algorithm is a derived version of Algorithms Wiki
        for further reference go to - https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance#Python
    '''
    if len(s1) < len(s2):
        return levenshtein(s2, s1)
    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1       # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]



mp={}
def auto_correct(s):
    '''
        auto_correct(s) takes an input list of string s
        This functions returns -1 if the query list is too difficult to tolerate or crosses the threshold.
        It returns the resultant correct list of strings which would be processed by query engine.
    '''
    global mp
    global Q
    mp={}
    lis=[]
    ans1={}
    ans2={}
    x=0
    temp=""
    st={}
    for t in s:
        if t in dic:
            lis.append(t)
            Q+=t+" "
            continue
        mind=10000000000
        temp=t
        for d in dic:
            x=levenshtein(t,d)
            if(x<mind):
                temp=d
                mind=x

        if(mind>len(t)/2):
            return -1
        Q+=temp+" "
        z=[]
        for d in dic:
            x=levenshtein(t,d)
            if x==mind:
                for j in dic[d]:
                    z.append(j)
                    st[j]=0
                ans1[d]=z
                z=[]
        ans2[t]=ans1
        ans1={}

    mx=0
    num=0

    for i in st:
        for j in ans2:
            flag=0
            for k in ans2[j]:
                for m in ans2[j][k]:
                    if m==i:
                        st[m]+=1
                        if mx<st[m]:
                            mx=st[m]
                            num=i
                        flag=1
                        break
                if flag==1:
                    break


    x=""
    for j in ans2:
        flag=0
        for k in ans2[j]:
            for m in ans2[j][k]:
                if m==num:
                    lis.append(k)
                    flag=1
                    break
            x=k
            if flag==1:
                break
                zzzz=0
        if flag==0:
            lis.append(x)

    for i in lis:
        flag=0
        for j in ans2:
            for k in ans2[j]:
                if i==k:
                    mp[j]=i
                    flag=1
                    break
            if flag==1:
                break
    return lis

############################################### OUTPUT MODULE #################################################################
def build_heap():
    '''
        build_heap()
        This function sorts the obtained results from the tf-idf algorithm using the well
        known "HEAP SORT" algorithm. This can be further used to print only some of most relevant documents.
        For eg. - We can show 10 results per page.
    '''
    import heapq
    import math
    for i in qdic:
        if((i in dic)==False):
            continue
        for j in dic[i]:
            if(j in result):
                result[j]+=dic[i][j]*qdic[i]
            else:
                result[j]=dic[i][j]*qdic[i]
    for i in result:
        h.append([-result[i]/(math.sqrt(magq*mag[i])),i])
    heapq.heapify(h)





def outputFirst_K_results(K):
    '''
    outputFirst_K_results(K)
    This funtion outputs the results obtained from the search engine.
    '''
    import heapq
    global Q
    length=len(h)

    print("\nShowing results for: ")
    l=Q.split()
    n=len(l)
    Q=""
    for i in range(0,n):
        Q=Q+(l[i]+" ")
    print(Q)
    print('The results are:')
    global docs_to_int
    for i in range(1,length+2):
        if(i<=length and i<=K):
            no=heapq.heappop(h)[1]
            print(str(i)+".\t--> Document ID IS :: "+str(no) + " and document name is : " + doc_to_int[int(no)])
        else:
            print("")
            return



############################################### END OF OUTPUT MODULE #################################################################






############################################### TOKENIZER MODULE #######################################################################


def fileread():
    '''
    fileread() function read all the files in the corpus and index them into the dictionary.
    This function uses the porter algorithm and is generating a list of tokens for each document using the nltk.word_tokenize() function in the "punkt" library.
    '''
    filename=[]
    global doc_to_int
    lis_of_docs = os.listdir("docs/")
    len_of_corpus=1    #actual size = 50
    #import codecs
    #f = codecs.open('C:\Python26\text.txt', 'r', 'utf-8-sig')

    for i in lis_of_docs:
        filename.append("docs/" + str(i))
        doc_to_int.update({int(len_of_corpus):str(i)})
        len_of_corpus+=1
        #filename=['1.txt','2.txt']
    lis = porter.inputs(filename)

    tokens=[]
    n=1
    #n=len(lis)
    for l in lis:
        tokens.append([n]+nltk.word_tokenize(l))
        n+=1
    #print(len(tokens))
    global NO_OF_DOC
    NO_OF_DOC= len(tokens)
    for t in tokens:
        index(t)
    print("Done indexing\n")
    fo=open('big.txt',"w")

fileread()

############################################### END OF TOKENIZER ########################################################################




############################################### QUERY PROCESSING #######################################################################

test1()


Q=""
def get_query():
    '''
        get_query()
        This is a helper function to input the requested query.
    '''
    global Q
    print "Audio input or text..????  1 for audio  and 2 for text "
    x=raw_input()
    x = int(x)
    if(x==1):
            s=audio_to_text()
    else:
        s=raw_input("Enter Query:  Ctrl+C to exit\n")
    f=open('temp_porter.txt',"w")
    f.write(s+"\n")
    f.close()

    lis=porter.inputs(['temp_porter.txt'])
    lis=lis[0]
    Q=""
    lis=auto_correct(nltk.word_tokenize(lis))

    if(lis == -1):
        return -1

    else:
        return lis

def audio_to_text():
    #!/usr/bin/env python3

    import speech_recognition as sr

    # get audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak:")
        audio = r.listen(source)

    try:
        print("You said " + r.recognize_google(audio))
        return r.recognize_google(audio)
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))

        return -1

while(True):
    h=[]
    qdic={}
    q=[]
    result={}
    magq=0
    q=get_query()

    if(q!=-1):
        getQueryTF_IDF()
        build_heap()
        outputFirst_K_results(3)
    else:
        print ("No Search Results Found\n")


############################################### END OF QUERY PROCESSING #######################################################################




############################################### END OF QUERY ENGINE #################################################################
