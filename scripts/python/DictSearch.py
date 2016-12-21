# import re
# import sys

def DictSearch(InString):
	outList = [InString]
	gesture_mapping = {"goes" : "^start...", \
					   "apple" : "^asdtausdfgjh", \
					   }

	for keyword, gesture in gesture_mapping.iteritems():

		j=0	#Index that allows the removal and insertion at specific location
		for n in range(len(outList)):
	
			#Split the List according to keyword 
			splitList = outList.pop(j).split(keyword)
		#	print(splitList)
						
			#Merge splitted list with keyword
			tempList = []
			tempList.append(splitList.pop(0))
			for subst in splitList:	
				tempList.append(keyword)
			 	tempList.append(subst)
		#	print(tempList)
			
			#Insert Splitted List into Output List
			for subst2 in tempList:
				outList.insert(j, subst2)
				j+=1

	print(outList)



def main():
	InString = "Gerald goes to the park and goes to get an apple and eat it. The weather was nice so he took off his hat and shouted, wassup?"
	DictSearch(InString)

if __name__ == "__main__":
	    
    main()


