import math


class Translator:
    def __init__(self,fileLoc):
        nodeList = self.readMorseFile(fileLoc)
        self.__tree = MorseBinTree(len(nodeList))
        
        for i in range(len(nodeList)):
            self.__tree.addNode(nodeList[i])
        
        #print(tree.getStartNode().getLeftChild().getLeftChild().getLeftChild().getMorse())
        #self.__tree.outputTree()
    def translateCharactersText(self,text):
        returnText = ""
        textList = text.split()

        for word in textList:
            for letter in word:
                if (self.__tree.getCharacterTranslation(letter) != None):
                    returnText += self.__tree.getCharacterTranslation(letter).toString() + " "
                else:
                    returnText += "undef "

        return returnText

    def translateMorseText(self,text):
        returnText = ""
        letterList = text.split()

        for letter in letterList:
            if (self.__tree.getMorseTranslation(letter) != None):
                returnText += self.__tree.getCharacterTranslation(letter).toString() + " "
            else:
                returnText += "undef "

        return returnText

    def readMorseFile(self, fileLoc):
        nodeList = []
        morseFile = open(fileLoc,"r")

        for line in morseFile:
            data = line.split()
            nodeList.append(TreeNode(data[0],data[1]))

        return nodeList

    def checkValidMorse(self,morse):
        if (len(morse) >= self.__tree.getTreeHeight()):
            return False
        else:
            for i in range(len(morse)):
                if (morse[i] not in [".","-"]):
                    return False



class MorseBinTree:
    def __init__(self,treeLength):
        self.__startNode = TreeNode()
        self.__treeLength = treeLength

        self.__treeHeight = 1
        while self.__treeLength > 0:
            self.__treeLength -= math.pow(2,self.__treeHeight)
            self.__treeHeight+=1

    def getTreeHeight(self):
        return self.__treeHeight

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

    def getStartNode(self):
        return self.__startNode
    
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
    

class TreeNode:
    def __init__(self,character = None, morse = None):
        self.__character = character
        self.__morse = morse
        self.__leftChild = None
        self.__rightChild = None

    def getCharacter (self):
        return self.__character

    def getMorse (self):
        return self.__morse

    def getLeftChild (self):
        return self.__leftChild

    def getRightChild (self):
        return self.__rightChild

    def setLeftChild (self, leftChild):
        self.__leftChild = leftChild

    def setRightChild (self, rightChild):
        self.__rightChild = rightChild

    def toString(self):
        if (self.__character != None and self.__morse != None):
            return self.__character + " : " + self.__morse

        else:
            return "[]"

if __name__ == "__main__":
    trans = Translator('morseCodeInput.txt')