#this file will include the search algorithm (A*) and heuristic function
import networkx as nx
import osmnx as ox
import map
#Search 
#A* Algorithm

class searchNode:
    def __init__(self, node, path=[], traveled=0):
        self.digraphNode = node
        self.path = path
        self.traveled = traveled

    def getChildren(self, g):
        return g.neighbors(self.digraphNode)
        #return a list of nodes children

class searchAgent:
    visited = []                                                                #visited will be list of digraph nodes
    obstacles = []
    graph = False
    goalDistance = False
    solution = False
    deadEnd = False
    
    #heuristic variables 
    nodesVisted = 0
    nodesExpanded = 0

    def __init__(self,userDistance,start,userIncline=0):                        #start is (lat,long)
        self.graph = map.createDiGraph(start)
        self.goalDistance = userDistance

        latlong = ox.geocoder.geocode(start) 
        closestNode = ox.get_nearest_nodes(self.graph, latlong[0], latlong[1], return_dist=False)
        firstNode = searchNode(closestNode)

        frontier = [[firstNode, self.goalDistance]]                             #astarScore of first node is the goalDistance
        success = self.loopFrontier(userIncline,frontier)                  #initialize frontier as the closest node
        if success == True:
            print("An inline route has been found")
            return self.solution
        else: 
            return False

    def loopFrontier(self,userIncline,frontier):
        print(frontier)
        count = 0                                                               #cut off for searching
        while len(frontier) != 0 or self.solution == False or count >= 100:
            if frontier[0][0].traveled >= self.goalDistance:
                self.solution = frontier[0][1]
            else:
                frontier = self.populateFrontier(userIncline, frontier)
                count += 1
        
        if self.solution != False:
            return True
        elif len(frontier) == 0:
            self.deadEnd = True
            return False
        else: 
            return False
    
    def astarScore(self, parentNode, childNode, dist, userIncline):
        print(parentNode)
        print(childNode)
        return (userIncline - self.calculateIncline(parentNode, childNode)) + (self.goalDistance-dist)
        #calculate astar score based on incline and distance


    def calculateIncline(self, parent, child):
        print(parent)
        print(child)
        return nx.get_node_attributes(self.graph, 'elevation')[parent] - nx.get_node_attributes(self.graph, 'elevation')[child]
    
    def distanceToChild(self, parent, child):
        edge = self.graph.get_edge_data(parent,child)
        #print(nx.get_edge_attributes(self.graph, 'length')[parent,child,0])
        return nx.get_edge_attributes(self.graph, 'length')[parent,child,0]
        #calculate distance to child node

    def populateFrontier(self,userIncline,frontier):
        parent = frontier[0][0]
        parentScore = frontier[0][1]
        children = parent.getChildren(self.graph)
        self.nodesExpanded += 1                                                 #parent node has been expanded
        for child in children:
            edge_distance = self.distanceToChild(parent.digraphNode, child)
            childScore = self.astarScore(parent.digraphNode, child, (parent.traveled+edge_distance), userIncline)
            if childScore < parentScore and child not in self.visited:
                child = searchNode(child, path=parent.path + [child], traveled=parent.traveled + edge_distance)
                frontier.append([child, childScore])
                self.visited.append(child.digraphNode)                          #store nodes in visited
        return frontier[1:]
