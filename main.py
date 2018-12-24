# CMPT310 - Assignment1
# Author: Sen Lin - sla248@sfu.ca - 301250505
import math


test_map = []


class Node:
    def __init__(self, elevation, row, column):
        self.elevation = elevation
        self.row = row
        self.column = column
        self.parent = None

    def __eq__(self, other):
        return self.row == other.row and self.column == other.column and other is not None


# by definition, the starting
def setEmptyMatrix():
    return [[math.inf for column in range(len(test_map[0]))] for row in range(len(test_map))]


def createNode(row, column):
    if row < 0 or row >= len(test_map) or column < 0 or column >= len(test_map[0]):
        return None
    return Node(test_map[row][column], row, column)

#helper - getter for scores
def getScore(scores, node):
    return scores[node.row][node.column]


def setScore(scores, node, value):
    scores[node.row][node.column] = value


# get current node.  fScore = None -> BFS
def getCurrentNode(nodes, fScores=None, end=None):
    currentNode = None
    if fScores is not None:
        smallestFScore = None
        for node in nodes:
            currentFScore = getScore(fScores, node)
            if currentNode is None or currentFScore < smallestFScore:
                smallestFScore = currentFScore
                currentNode = node
    else:
        for node in nodes:
            if currentNode is None or getHeuristic(currentNode, end) > getHeuristic(node, end):
                currentNode = node
    return currentNode


def getPath(node):
    path = []
    temp = node
    while temp is not None:
        path.append(temp)
        temp = temp.parent
    return path[::-1]


def getParent(node):
    return node.parent


def getNeighbours(parent):
    neighbours = [createNode(parent.row - 1, parent.column),
        createNode(parent.row + 1, parent.column),
        createNode(parent.row, parent.column - 1),
        createNode(parent.row, parent.column + 1)]
    return [neighbour for neighbour in neighbours if neighbour is not None]


# heuristic function
def getHeuristic(current, end):
    return abs(current.row - end.row) + abs(current.column - end.column)


def readFile():
    with open("Asst1.data(4).txt") as f:
        lines = f.read().splitlines()
    size = int(lines[0])
    pointsStr = lines[1]
    mapRows = lines[2:]
    initMap(mapRows)
    if size != len(test_map) or size != len(test_map[0]):
        print("Size and map size does not match")
        return
    return getStartEndNodes(pointsStr)


# initialize search map
def initMap(rows):
    for row in rows:
        arr = []
        rowStr = removeArrChar(row)
        valuesStr = rowStr.split()
        for value in valuesStr:
            arr.append(int(value))
        test_map.append(arr)


# display final result in traditional (x, y) format, aka (column, row)
def writePath(nodes, start, end, mode, fScores=None, gScores=None):
    if nodes is None:
        return
    print("The path found from {0} to {1} is".format(getCoordinateStr(start), getCoordinateStr(end)))
    if mode == "aStar":
        writeAStarNodeInfo(nodes, fScores, gScores, end)
    else:
        writeBFSNodeInfo(nodes, end)


# helper - remove extra characters for array
def removeArrChar(arrStr):
    return arrStr.replace("[", "").replace("]", "")


# helper - get elevation difference
def getElevDifference(node, aNode):
    return abs(node.elevation - aNode.elevation)


# helper - get coordinate as string
def getCoordinateStr(node):
    return "({0}, {1})".format(node.column, node.row)


# helper - write each node info for A*
def writeAStarNodeInfo(nodes, fScores, gScores, end):
    for node in nodes:
        print("Node(x, y): ", getCoordinateStr(node), getScoreInfo(node, fScores, gScores, end))


# helper - for A* to get score info for each node
def getScoreInfo(node, fScores, gScores, end):
    fScoreStr = "FScore is: {0}, ".format(fScores[node.row][node.column])
    gScoreStr = "GScore is: {0}, ".format(gScores[node.row][node.column])
    hScoreStr = "HScore is: {0}".format(getHeuristic(node, end))
    return fScoreStr + gScoreStr + hScoreStr


# helper - write each node info for Best First Search
def writeBFSNodeInfo(nodes, end):
    for node in nodes:
        print("Node(x, y): ", getCoordinateStr(node), "HScore is: ", getHeuristic(node, end))


# helper - get start and end node
def getStartEndNodes(pointsStr):
    points = removeArrChar(pointsStr)
    pointsArr = points.split()
    nodes = []
    for item in pointsArr:
        temp = item.split(",")
        nodes.append(createNode(int(temp[1]), int(temp[0])))

    start = nodes[0]
    end = nodes[1]
    return start, end


# best first search
def BFS(start, end):
    if start is not None and end is not None:
        closedNodes = []
        openNodes = [start]
        count = 0
        while len(openNodes) != 0:
            currentNode = getCurrentNode(openNodes, None, end)
            neighbours = getNeighbours(currentNode)
            
            for neighbour in neighbours:
                if neighbour not in openNodes and neighbour not in closedNodes:
                    if 1 + getElevDifference(neighbour, currentNode) < 4:
                        openNodes.append(neighbour)
                        neighbour.parent = currentNode

            openNodes.remove(currentNode)
            closedNodes.append(currentNode)
            count += 1

            if currentNode == end:
                print("Best First Search has found the path")
                print("There are {0} nodes expended".format(len(openNodes) + len(closedNodes)))
                print("The number of iterations is: ", count)
                return getPath(currentNode)

        print("No path found between", getCoordinateStr(start), "and", getCoordinateStr(end), "(BFS)")
        return None
    print("Start point or end point is out of map. Please check your input. Bye!")
    return None


# A* search
def aStar(start, end):
    if start is not None and end is not None:
        closedNodes = []
        openNodes = [start]
        # initialize fScore and gScores
        fScores = setEmptyMatrix()
        gScores = setEmptyMatrix()
        # initialize fScore and gScore of start
        setScore(fScores, start, 0)
        setScore(gScores, start, 0)
        count = 0
        while len(openNodes) != 0:
            currentNode = getCurrentNode(openNodes, fScores)
            if currentNode == end:
                print("A* Search has found the path")
                print("There are {0} nodes expended".format(len(openNodes) + len(closedNodes)))
                print("The number of iterations is: ", count)
                return fScores, gScores, getPath(currentNode)

            neighbours = getNeighbours(currentNode)
            for neighbour in neighbours:
                # handle neighbours
                if neighbour in closedNodes or getElevDifference(neighbour, currentNode) >= 4:
                    continue
                else:
                    if neighbour not in openNodes:
                        gScore = 1 + getElevDifference(neighbour, currentNode) + getScore(gScores, currentNode)
                        openNodes.append(neighbour)
                        # set parent and scores for newly joined nodes
                        setScore(gScores, neighbour, gScore)
                        setScore(fScores, neighbour, gScore + getHeuristic(neighbour, end))
                        neighbour.parent = currentNode
                    else:
                        gScore = getScore(gScores, neighbour)
                        newGScore = 1 + getElevDifference(neighbour, currentNode) + getScore(gScores, currentNode)
                        if newGScore < gScore:
                            # update parent
                            neighbour.parent = currentNode
                            # update gScore and fScore
                            setScore(gScores, neighbour, newGScore)
                            setScore(fScores, neighbour, newGScore + getHeuristic(neighbour, end))

            openNodes.remove(currentNode)
            closedNodes.append(currentNode)
            count += 1
        print("No path found between", getCoordinateStr(start), "and", getCoordinateStr(end), "(A*)")
        return None, None, None
    print("Start point or end point is out of map. Please check your input. Bye!")
    return None, None, None


def init():
    # initialize start and end node
    startNode, endNode = readFile()

    # print research for A* search
    fScores, gScores, path = aStar(startNode, endNode)
    writePath(path, startNode, endNode, "aStar", fScores, gScores)

    print("-------------------------------------------------------------")

    # print result for BFS search
    writePath(BFS(startNode, endNode), startNode, endNode, "BFS")


init()
