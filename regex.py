# -*- coding: utf-8 -*-

import os, sys, re 

#search root dir
inputDir = " -path to- /manual"
#inputDir = " -path to test- "

#html page with a "%output%"  text node in the body 
tempDir = " -path to template- "
tempName = "TEMPLATE.html"
 
outDir = " -path to output- "
outName = "out.html"


#regex
#patternStr = r"(?:^|\s)(?:\*){2,2}([\w|\s|\/]+)(?:\*)"
patternStr = r"(?:^|\s)(?:\*){1,1}([\w|\s|\/]+)(?:\*)"
#repStr = r" :guilabel:`\1`"

def switchSR(filePath, filename, matchOut):
	fmatch = search(filePath, filename, matchOut)
	#fmatch = replace(filePath, filename, matchOut)
	return fmatch

def search(filePath, filename, matchOut):
	fl = open(filePath+'/'+ filename, 'r', encoding="utf-8")
	fContent = fl.read()
	
	pattern = re.compile(patternStr, re.MULTILINE)
	
	fmatch = re.findall(patternStr, fContent)

	#remove duplicates in file scope
	fmatch = checkSinguOuter(fmatch, fmatch, True)
	#remove duplicates in global scope
	#out of order: quasi-multi dim. list
	#fmatch = checkSinguOuter(matchOut, fmatch, False)
		
	fl.close()
	if len(fmatch) > 0:
		fmatch.append(str(len(fmatch))+" | "+filePath+'/'+ filename)
		matchOut.append(fmatch)
	return matchOut

def replace(filePath, filename, matchOut):
	if "repStr" in globals():
		fl = open(filePath+'/'+ filename, 'r+', encoding="utf-8")
		fContent = fl.read()
		
		#pattern = re.compile(patternStr, re.MULTILINE)
		#replc = re.compile(repStr, re.MULTILINE)
		
		outTuple = re.subn(patternStr, repStr, fContent)

		if outTuple[1] > 0:
			fl.seek(0)
			fl.write(outTuple[0])
			fl.truncate()
			matchOut.append([str(outTuple[1])+" | "+filePath+'/'+ filename])
		fl.close()
	else:
		print("regex script: no replace string")
	return matchOut

#check if match string is duplicate 
def checkSinguOuter(matchOut, fmatch, self):
	s = False
	a = 0
	while a < len(fmatch): 
		if self:
			bn = checkSinguInner(matchOut, fmatch[a], a)
		else:
			bn = checkSinguInner(matchOut, fmatch[a], -1)
		if bn:
			fmatch.pop(a)
		else:
			a = a + 1
	return fmatch
	
	
def checkSinguInner(matchOut, fmatch, o):
	i = 0
	while i < len(matchOut):
		if i != o and matchOut[i] == fmatch:
			return True
		else:
			i = i + 1
	return False

#html file ouput
def writeOut(matchOut, inputDir):
	tempFile = open(tempDir + '/' + tempName, encoding="utf-8-sig")
	tempCont = tempFile.read()
	table = "<table><th>" + patternStr + "</th><tbody>" 
	for ent in matchOut:
		table += "<tr><td>" + str(ent) + "<td><tr>"
	
	table += "</tbody></table>"
	htmloutText = re.sub('%output%', table, tempCont)
	htmloutput = open(outDir+ '/'+ outName,'w')
	htmloutput.write(htmloutText)
	htmloutput.close()
	tempFile.close()

def walkDir(inputDir):
	matchOut = []
	for dirpath, dnames, fnames in os.walk(inputDir):
		for fl in fnames:
			if fl.endswith(".rst"):
				matchOut = switchSR(dirpath, fl, matchOut)
	
	return matchOut

writeOut(walkDir(inputDir), inputDir)
