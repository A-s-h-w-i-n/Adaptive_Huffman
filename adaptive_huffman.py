"""
Created on Sun Jun 16 2019

@author: Ashwin
"""

#This script is capable of encoding and decoding input data using the Adaptive 
#Huffman technique. The user needs to have the following 
#information to complete the process:
#    1) List of symbols in sorted manner
#    2) Input data
#The input input data has to be a 1 dimensional data structure, or a string 
#Uncomment print statements to see working of respective function

import math

COUNT = 0
symbolDict = {}  #Stores details of all the symbols. Can be used to traverse the binary tree

#Saves symbol information and position in binary tree             
class Node: 
    def __init__(self, label = None, freq = None, parent = None, left = None, right = None):
        self.label = label
        self.freq = freq
        self.parent = parent
        self.left = left
        self.right = right

#Prints contents of user defined class Node    
def printNode(N):
    if(N==None):
        print("None\n")
    else:
        print("%s:%d\n"%(N.label,N.freq))  

#Symbol list parameters:
#No of symbols = m
#m = 2^e + r ; 0<=r<=2^e
def getSymListParameters(symbols):
    l = len(symbols)
    e = 0
    while(math.pow(2,e) < l):
        e += 1
    e -= 1
    r = int(l - math.pow(2,e))
    return [r,e]  

#Swap child nodes if frequency of left child is larger than right child
def swapLRChild(ele):
    parent = ele.parent
    if(parent.left.freq > parent.right.freq):
        parent.left,parent.right = parent.right,parent.left  

#Binary representation of integer n using 'bits' no.of bits
def int2bin(n,bits):
    a = str(bin(n))
    b = a[2:]    
    while(len(b) < bits):
        b = '0' + b        
    return b

#Get fixed code for element while encoding. 
#No of symbols = m
#m = 2^e + r ; 0<=r<=2^e    
def getFixedCode(k,r,e):
    if k >= 1 and k <= 2*r:
        return int2bin(k-1,e+1)
    else:
        return int2bin(k-r-1, e)    

#Get binary code for element by traversing the binary tree
def getBinCode(ele):
    code = ''
    parent = ele.parent
    while(ele.parent != None):
        if(parent.left == ele):
            code += '0'            
        else:
            code += '1'            
        ele = parent
        parent = ele.parent
    return code[::-1]

#Update frequency and position of all nodes for the incoming symbols
def updateTree(current):
    current.freq += 1
#    print('Updating tree... ',end='')
    while(current.parent != None):
        current.parent.freq += 1
        swapLRChild(current)        
        current = current.parent
#    print('Complete')
    
#Adaptive Huffman tree update and encoding process
def adaptiveHuffmanEnc(inp,symList):
    global COUNT
    global symbolDict
    COUNT = 0           
    NYT = Node('NYT',0,None,None,None)    
    codedOP = ""
#    symList = generateSymbolList(symbols)
    
    symParam = getSymListParameters(symList)
    r = symParam[0]
    e = symParam[1]
    
    for i in inp:
        updateFlag = 0
        if i not in symbolDict: 
            nytCode = getBinCode(NYT)
            fixedCode = getFixedCode(symList.index(i)+1,r,e)
            COUNT += 1
            symbolDict[i] = Node(i,0,None,None,None)
            
            if(NYT.parent == None):
                root = Node(('N'+str(COUNT)),1,None,NYT,symbolDict[i])
                NYT.parent = symbolDict[i].parent = root            
            else:
                nytParent = NYT.parent
                newNode = Node(('N'+str(COUNT)),0,nytParent,NYT,symbolDict[i])
                NYT.parent = symbolDict[i].parent = nytParent.left = newNode 
                
#            print('New symbol added. ',end='')                                  
            updateFlag = 1
            
        current = symbolDict[i] 
        updateTree(current)
        
        if(updateFlag == 1):
            codedOP = codedOP + nytCode + fixedCode
        else:
            codedOP += getBinCode(symbolDict[i])                            
    
    return codedOP
        
#Adaptive Huffman tree update and decoding process   
def adaptiveHuffmanDeco(inp,symList):
    global COUNT    
    COUNT = 0
    NYT = Node('NYT',0,None,None,None)
    root = NYT
    decodedMsg = ""
    
    symParam = getSymListParameters(symList)
    r = symParam[0]
    e = symParam[1]
    
    while(inp != ''):
        nytCode = getBinCode(NYT) 
                     
        if(inp.startswith(nytCode)):
#            print('Adding new symbol... ',end='')
            nytBits = len(nytCode)
            inp = inp[nytBits:]
            eBits = inp[0:e]
            eInt = int(eBits,2)
            
            if(eInt < r):
                index = int(inp[0:e+1],2) + 1
                inp = inp[e+1:]
            else:
                index = eInt + r + 1
                inp = inp[e:]
                
            sym = symList[index-1]
            COUNT += 1
            current = Node(sym,0,None,None,None)
            newNode = Node('N'+str(COUNT),0,None,NYT,current)
            
            if(COUNT==1):
                root = newNode
                
            current.parent = newNode
            
            if (NYT.parent == None):
                NYT.parent = newNode
            else:
                nytparent = NYT.parent
                NYT.parent = nytparent.left = newNode 
                newNode.parent = nytparent  
                                      
        else:
            current = root
            n = 0       
            
            for i in inp:  
                if(current.right == None or current.left == None):
                    break
                if(i=='0'):
                    current = current.left
#                    print("Go left -> ",end="")
                else:
                    current = current.right
#                    print("Go right -> ",end="")
                    
                n += 1       
                
            inp = inp[n:]    
            sym = current.label   
            
        updateTree(current)   
        decodedMsg += sym  
#        print(inp)
        
    return decodedMsg

#Compare memory use before and after compression
def encodingMetrics(inp,symbols,codedText):
    n = math.ceil(math.log(len(symbols),2))
    print("\n\nNo. of bits before compression: %d"%(n*len(inp)))      
    print("No. of bits after compression: %d"%(len(codedText)))    
    print("Compression Ratio: %.4f\n\n"%((n*len(inp))/len(codedText)))
    
#Driver function    
def main():
#    inp = "The quick brown fox, jumps\nover the lazy dog?!"
    inp = 'aardvark'
    print('Input: %s'%(inp))
    symbols = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz ,.?!\n'
    codedText = adaptiveHuffmanEnc(inp,symbols)
#    print("\nCoded O/P: ",end='')
#    print(code)
    
    encodingMetrics(inp,symbols,codedText)
    
    decoded = adaptiveHuffmanDeco(codedText,symbols) 
    print('\nDecoded O/P: %s'%(decoded))
        
main()    