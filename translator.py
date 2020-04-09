import math

#Main class which creates the tree instance, reads textfile containing morse inputs and translates inputs
class Translator:
    def __init__(self,fileLoc):
        nodeList = self.readMorseFile(fileLoc)
        self.__tree = MorseBinTree(len(nodeList))
        
        for i in range(len(nodeList)):
            self.__tree.addNode(nodeList[i])
    

    #Translates input english text to morse code
    def translateCharactersText(self,text):
        returnText = ""
        textList = text.split()

        for word in textList:
            for letter in word:
                if (self.__tree.getCharacterTranslation(letter) != None):
                    returnText += self.__tree.getCharacterTranslation(letter).getMorse() + " "
                else:
                    returnText += "undef "

        return returnText

    #Translates input morse code to english text (with no spaces)
    def translateMorseText(self,text):
        returnText = ""
        letterList = text.split()

        for letter in letterList:
            if (self.__tree.getMorseTranslation(letter) != None):
                returnText += self.__tree.getMorseTranslation(letter).getCharacter()
            else:
                returnText += "undef "

        return returnText

    #Reads provided morse code file and adds node to binary tree
    def readMorseFile(self, fileLoc):
        nodeList = []
        morseFile = open(fileLoc,"r")

        for line in morseFile:
            data = line.split()
            nodeList.append(TreeNode(data[0],data[1]))

        return nodeList

    #UNUSED: checks if morse will be translated using current tree
    def checkValidMorse(self,morse):
        if (len(morse) >= self.__tree.getTreeHeight()):
            return False
        else:
            for i in range(len(morse)):
                if (morse[i] not in [".","-"]):
                    return False


#Binary tree containing TreeNodes of morse code character pairs
class MorseBinTree:
    def __init__(self,treeLength):
        self.__startNode = TreeNode()
        self.__treeLength = treeLength
        self.__treeHeight = 1

        while self.__treeLength > 0:
            self.__treeLength -= math.pow(2,self.__treeHeight)
            self.__treeHeight+=1

    #Returns height of tree
    def getTreeHeight(self):
        return self.__treeHeight

    #Returns morse code translation of an ascii character, simple binary search
    def getCharacterTranslation(self,character):
        finalTreeList = [self.__startNode]
        tempList = [self.__startNode]

        for i in range(1, self.__treeHeight): 
            for y in range(len(tempList)):
                finalTreeList.append(tempList[y].getLeftChild())
                finalTreeList.append(tempList[y].getRightChild())
            tempList = finalTreeList[int(len(finalTreeList) - math.pow(2,i)):]

            for x in range(len(tempList)):
                if(tempList[x] != None):
                    if (tempList[x].getCharacter() == character.upper()):
                        return tempList[x]
        return None

    #Returns character when given morse code, performs unordered binary search by going through tree layer by layer
    def getMorseTranslation(self,morse):
        currentNode = self.__startNode
        for i in range(len(morse)):
            if (i == len(morse) - 1):
                if (morse[i] == "."):
                    return currentNode.getLeftChild()
                else:
                    return currentNode.getRightChild()
            else:
                if (morse[i] == "."):
                    currentNode = currentNode.getLeftChild()
                else:
                    currentNode = currentNode.getRightChild()
        return None

    #Outputs tree to console in order
    def outputTree(self):
        finalTreeList = [self.__startNode]
        tempList = [self.__startNode]

        print("START \n")

        for i in range(1, self.__treeHeight): 
            for y in range(len(tempList)):
                finalTreeList.append(tempList[y].getLeftChild())
                finalTreeList.append(tempList[y].getRightChild())
            tempList = finalTreeList[int(len(finalTreeList) - math.pow(2,i)):]

            for x in range(len(tempList)):
                if (tempList[x] != None):
                    print(tempList[x].toString() +  "    " , end="")

                else:
                    print ("[]    ", end = "")
            print("\n")

    #Returns start node, allowing other classes to access the tree
    def getStartNode(self):
        return self.__startNode
    
    #Function to add node to binary tree
    def addNode(self,newNode):
        morse = newNode.getMorse()
        currentNode = self.__startNode

        for i in range(len(morse)):
            if (i == len(morse) - 1):
                if morse[i] == ".":
                    if (currentNode.getRightChild() == None):
                        currentNode.setRightChild(TreeNode())

                    currentNode.setLeftChild(newNode)
                else:
                    if (currentNode.getLeftChild() == None):
                        currentNode.setLeftChild(TreeNode())
                    currentNode.setRightChild(newNode)
                

            elif (morse[i] == "."):
                if (currentNode.getLeftChild() == None):
                    currentNode.setLeftChild(TreeNode())
                if (currentNode.getRightChild() == None):
                    currentNode.setRightChild(TreeNode())
                currentNode = currentNode.getLeftChild()
            else:
                if (currentNode.getLeftChild() == None):
                    currentNode.setLeftChild(TreeNode())
                if (currentNode.getRightChild() == None):
                    currentNode.setRightChild(TreeNode())
                currentNode = currentNode.getRightChild()
    
#Class for a single node on the binary tree
class TreeNode:
    def __init__(self,character = None, morse = None):
        self.__character = character
        self.__morse = morse
        self.__leftChild = None
        self.__rightChild = None

    #Returns character of this node
    def getCharacter (self):
        return self.__character

    #Returns morse of this node
    def getMorse (self):
        return self.__morse

    #Returns left child
    def getLeftChild (self):
        return self.__leftChild

    #Returns right child
    def getRightChild (self):
        return self.__rightChild

    #Sets the left child of this node
    def setLeftChild (self, leftChild):
        self.__leftChild = leftChild

    #Sets the right child of this node
    def setRightChild (self, rightChild):
        self.__rightChild = rightChild

    #Returns the node in a string
    def toString(self):
        if (self.__character != None and self.__morse != None):
            return self.__character + " : " + self.__morse

        else:
            return "[]"

if __name__ == "__main__":
    #Creates translator object 
    trans = Translator('morseCodeInput.txt')

    print(trans.translateCharactersText("i love mais so much / i love mais 2020"))
    print(trans.translateCharactersText("mais"))

    print(trans.translateMorseText("-- .- .. ... "))
    print(trans.translateMorseText(".. .-.. --- ...- . -- .- .. ... ... --- -- ..- -.-. .... -..-. .. .-.. --- ...- . -- .- .. ... ..--- ----- ..--- -----"))