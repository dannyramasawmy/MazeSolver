from mazeModule import *
import matplotlib.pyplot as plt

def solveMaze(mazeGrid, start, goal, algorithm):
    """
    Solves maze.

    Input:
        maze = Maze object
        start = PriorityCoordinate
        goal = PriorityCoordinate
    """
    maze = Maze(mazeGrid)

    # check coordinates
    if maze.validCoordinate(start) == False:
        return False
    if maze.validCoordinate(goal) == False:
        return False

    # choose algorithm
    if algorithm == 'astar':
        queueType = 'priority'
    if algorithm == 'BFS':
        queueType = 'queue'
    if algorithm == 'DFS':
        queueType = 'stack'

    # set-up
    queue = Queue(queueType)
    queue.enqueue(start, 0)
    maze.updateVisited(start)

    # possible neighbors E S W N
    neighbors = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    # flags
    returnPathFlag = False

    # open figure
    plt.figure()

    # when there are items in the queue
    while queue.isEmpty == False:
        # get item from queue
        currentCoord = queue.dequeue()
        # check if its the goal
        if currentCoord == goal:
            returnPathFlag = True
            break

        # add the neighbors
        for i, j in neighbors:
            # get neighbor
            neighbor = PriorityCoordinate(currentCoord.i+i, currentCoord.j+j)
            if maze.validCoordinate(neighbor):
                # update parent
                neighbor.setParent(currentCoord)
                # calculate priority and add to queue
                priority = neighbor.stepsToGoal(goal) + neighbor.stepsHome
                queue.enqueue(neighbor, priority)
                # update visited
                maze.updateVisited(neighbor)

        # plot results
        mazeVisited = maze.getVisitedCopy(start, goal)
        # plot with numpy and update each loop
        plt.imshow(mazeVisited, cmap='viridis', vmin=0.0, vmax=1.0)
        plt.title(algorithm)
        plt.ion()
        plt.show()
        plt.pause(0.01)

    # was there a solution?
    if returnPathFlag:
        print(f'For {algorithm} the solution is: \n')
        maze.updateFinalPath(currentCoord.getPath())
        maze.printVisited()

    # get final copy
    finalMaze = maze.getVisitedCopy(start, goal)
    return finalMaze


def plotResults(plots, titles):
    """
    Plot the results for the three searching algorithms.
    """
    plt.figure()
    # plot result
    for idx, name in enumerate(titles):
        plt.subplot(1, len(titles), idx + 1)
        plt.imshow(plots[idx], cmap='viridis', vmin=0.0, vmax=1.0)
        plt.title(titles[idx])
    # show    
    plt.draw()
    plt.show()
    plt.pause(10)

    return None

def compareAlgorithms(mazeGrid, start, goal):
    """
    For the current grid, compare searching with each algorithm.
    """
    # solve the maze
    # choose algo,  'astar', 'DFS', 'BFS'
    mazeVisitedAstar = solveMaze(mazeGrid, start, goal, 'astar')
    mazeVisitedDFS = solveMaze(mazeGrid, start, goal, 'DFS')
    mazeVisitedBFS = solveMaze(mazeGrid, start, goal, 'BFS')
    # plot the results
    plotResults([mazeVisitedAstar, mazeVisitedDFS, mazeVisitedBFS], ['A*', 'DFS', 'BFS'])
    
    return None

# -------------------------------------------------
# maze 1
# -------------------------------------------------
# define the maze 0 =  ok, 1 = wall
mazeGrid = [[0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0],
            [0, 0, 1, 0, 0, 0],
            [0, 0, 1, 0, 0, 0],
            [0, 0, 1, 1, 0, 0],
            [1, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0]]

start = PriorityCoordinate(0, 5)
goal = PriorityCoordinate(5, 2)
compareAlgorithms(mazeGrid, start, goal)

# -------------------------------------------------
# maze 2
# -------------------------------------------------
mazeGrid = [[0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
            [1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0],
            [0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0],
            [0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0],
            [0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]]

start = PriorityCoordinate(0, 0)
goal = PriorityCoordinate(len(mazeGrid)-1, len(mazeGrid[0])-1)
compareAlgorithms(mazeGrid, start, goal)