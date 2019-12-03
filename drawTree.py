#-*-coding:utf-8-*
#!/bin/sh

import os
import sys
from optparse import OptionParser

indentSign = "\t"
treeBranch = "├"
treeBranchEnd = "└"
treeExtend = "│"
fillEmptyCharCnt = 2
treeFillEmpty = " " * fillEmptyCharCnt
space = " "
config = "example.conf"

class node :
    def __init__(self, string, indentCount):
        self.string = string
        self.indentCount = indentCount
        self.parent = None
        self.child = None
        self.sibling = None
    def addParent(self, parent) :
        self.parent = parent
    def addChild(self, child) :
        self.child = child
    def addSibling(self, sibling) :
        self.sibling = sibling

def addNode(lastNode, currentNode) :
    if currentNode.indentCount == lastNode.indentCount + 1 :
        lastNode.addChild(currentNode)
        currentNode.addParent(lastNode)
    elif currentNode.indentCount <= lastNode.indentCount :
        while True :
            if lastNode.indentCount == currentNode.indentCount :
                lastNode.addSibling(currentNode)
                currentNode.addParent(lastNode.parent)
                break
            if lastNode.parent != None:
                lastNode = lastNode.parent
            else :
                print "Config format error."
                sys.exit(-1) 

def createTree() :
    if not os.path.isfile(config):
        print "Config file not exist"
        sys.exit(-1)
    with open(config, "r") as f :
        line = f.readline().replace('\n', '')
        root = node(line, 0)
        lastNode = root
        for line in f :
            line = line.replace('\n', '')
            result = countLeadingIndent(line)
            currentNode = node(result["string"], result["indent"])
            addNode(lastNode, currentNode)
            lastNode = currentNode
    return root

def indentForward(prependStr) :
    treeBranchLen = len(treeBranch)
    treeBranchEndLen = len(treeBranchEnd)
    if prependStr[-treeBranchEndLen:] == treeBranchEnd :
        prependStr = prependStr[:-treeBranchEndLen] + space + treeFillEmpty + treeBranch
    elif prependStr[-treeBranchLen:] == treeBranch :
        prependStr = prependStr[:-treeBranchLen] + treeExtend + treeFillEmpty + treeBranch
    else :
        prependStr = treeFillEmpty + treeBranch
    return prependStr

def lastSiblingPrepend(prependStr) :
    treeBranchLen = len(treeBranch)
    if prependStr[-treeBranchLen:] == treeBranch :
        prependStr = prependStr[:-treeBranchLen] + treeBranchEnd
    else :
        print "Argument is invalid."
        sys.exit(-1)
    return prependStr

def printTree(tree, prependStr = "", output = None) :
    currentNode = tree
    if currentNode.sibling == None and currentNode.parent != None:
        prependStr = lastSiblingPrepend(prependStr)
    
    if output != None:
        output.write(prependStr + currentNode.string + "\n")
    else:
        print prependStr + currentNode.string

    if currentNode.child != None :
        printTree(currentNode.child, indentForward(prependStr), output)
    if currentNode.sibling != None :
        printTree(currentNode.sibling, prependStr, output)

def countLeadingIndent(line) :
    count = 0
    indentSignLen = len(indentSign)
    while True :
        if line[0: indentSignLen] == indentSign :
            line = line[indentSignLen : ]
            count += 1
        else :
            break
    return {"indent" : count, "string" : line}

def main () :
    global config
    global indentSign
    parser = OptionParser()
    parser.add_option("-c", "--config", dest="config", help="Path of config file.", metavar="CONFIG")
    parser.add_option("-t", type="int", dest="tabConvert", help="Indent using the blank space in config file.", metavar="SPACE_COUNT")
    parser.add_option("-o", "--output", dest="output", help="Output file path.", metavar="OUTPUT")
    (options, args) = parser.parse_args()
    
    if options.config != None:
        config = options.config
    if options.tabConvert != None:
        indentSign = space * options.tabConvert

    root = createTree()
    
    if options.output != None:
        with open(options.output, "w") as f:
            printTree(root, output=f)
    else:
        printTree(root)

if __name__ == "__main__" :
    main()