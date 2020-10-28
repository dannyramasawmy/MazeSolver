"""
mazeModule contains classes and test cases for A* maze algorithm.
"""
from copy import deepcopy


class PriorityCoordinate:
    """
    A coordinate, with a pointer to the parent and distance to path home.
    """

    def __init__(self, i, j):
        """ 
        Initialise coordinate.
        i = row index, 
        j = column index,
        parent = pointer to coordinate
        stepsHome = number of parents till None
        """
        self.i = i
        self.j = j
        self.parent = None
        self.stepsHome = 0

    def setParent(self, parentCoordinate):
        """
        Sets a pointer to the parents, plus increments the steps.
        """
        self.parent = parentCoordinate
        self.stepsHome = parentCoordinate.stepsHome + 1

    def stepsToGoal(self, goalCoordinate, heuristic='l2'):
        """
        Get the l1 (city-block) distance to the goal.
        """
        if heuristic == 'l1':
            distance = abs(goalCoordinate.i - self.i) + \
                abs(goalCoordinate.j - self.j)
        else: # l2
            distance = ((goalCoordinate.i - self.i)**2  +  \
                (goalCoordinate.j - self.j)**2)**(1/2)

        return distance

    def getPath(self):
        """
        Prints and returns the path home.
        """
        # initialise path
        path = [(self.i, self.j)]
        # follow path home
        tmp = self.parent
        while tmp:
            path.append((tmp.i, tmp.j))
            tmp = tmp.parent
        # print path
        #print(f'The path is: {path[::-1]}')
        return path[::-1]

    def __eq__(self, coordinate):
        """
        Equivalence operator overloaded, comapres coordinates of i and j terms.
        """
        return self.i == coordinate.i and self.j == coordinate.j

    def __str__(self):
        return f'Coord: {self.i, self.j}, Steps home: {self.stepsHome}'

    def __repr__(self):
        return self.__str__()


class Maze:
    """
    Contains maze class as 2D array.
    0 - valid position
    1 - invalid position (wall)
    """

    def __init__(self, maze):
        """
        maze : must be 2D array of 1's and 0's.
        """
        self.grid = deepcopy(maze)
        self.visited = deepcopy(maze)
        # 0 based height and width
        self.height = len(maze)
        self.width = len(maze[0])

    def validCoordinate(self, coordinate):
        """
        Check if the coordinate is valid on the grid, 
        i.e, within bounds and element[i][j] ==  0.
        """
        if 0 <= coordinate.i < self.height and 0 <= coordinate.j < self.width:
            if self.visited[coordinate.i][coordinate.j] == 0:
                return True
        return False

    def updateVisited(self, coordinate):
        """
        Update the visited map with a given coordinate.
        """
        if self.validCoordinate(coordinate) == True:
            self.visited[coordinate.i][coordinate.j] = 0.1

    def updateFinalPath(self, path):
        """
        Given a path, which is in the form of a list of (i, j) tuples,
        updated the visited map to show the final path and start and end points.
        """
        for i, j in path:
            self.visited[i][j] = 0.7
        i, j = path[0]
        self.visited[i][j] = 0.8
        i, j = path[-1]
        self.visited[i][j] = 0.85

    def formatMaze(self, maze):
        """Formats maze for printing."""
        return '\n'.join(['  '.join([str(elem) for elem in row]) for row in maze])

    def printVisited(self):
        """ Prints a 2D array for the visited map."""
        print('\n' + self.formatMaze(self.visited) + '\n')

    def __repr__(self):
        """ Prints a 2D array."""
        dimensions = f'\nA maze of height: {self.height} and width: {self.width} \n'
        mazeStr = self.formatMaze(self.grid)
        return dimensions + '\n' + mazeStr + '\n'


class Queue:
    """
    A queue, which is a (inefficient) priority queue by 
    default but can operate as a stack or normal queue.
    """

    def __init__(self, queueType='priority'):
        # use a list as the data structure (TODO: linked list better?)
        self.items = []
        # switch for different algorithms
        if queueType in ['priority', 'queue', 'stack']:
            self.queueType = queueType
        else:
            self.queueType = 'priority'

    @property
    def isEmpty(self):
        """
        True when empty, false when there are items in the queue.
        """
        return True if len(self.items) == 0 else False

    def enqueue(self, coordinate, score):
        """
        Add item, sort from largest to smallest.
        type : (default) 'priority' - astar, 'queue' - DFS, 'stack' - BFS
        """
        # TODO: insertion sort faster?
        if self.queueType == 'priority':
            self.items.append((coordinate, score))
            self.items.sort(key=lambda x: x[1], reverse=True)

        if self.queueType == 'queue':
            self.items.insert(0, (coordinate, score))

        if self.queueType == 'stack':
            self.items.append((coordinate, score))

    def dequeue(self):
        """
        Return the end of the queue.
        """
        if self.isEmpty == False:
            return self.items.pop()[0]
        else:
            return None

    def __repr__(self):
        """
        Return priority queue, reverse order.
        """
        return ' '.join([str((crd[0].i, crd[0].j)) for crd in self.items])


def test():
    try:
        # define the maze 0 =  ok, 1 = wall
        mazeGrid = [[0, 0, 0, 0, 0, 0],
                    [0, 0, 1, 0, 0, 0],
                    [0, 0, 1, 0, 0, 0],
                    [0, 0, 1, 0, 0, 0],
                    [0, 0, 1, 1, 0, 0],
                    [1, 0, 0, 1, 0, 0],
                    [0, 0, 0, 0, 0, 0]]

        maze = Maze(mazeGrid)
        # check maze printing
        print(maze)

        # define start and end points
        start = PriorityCoordinate(0, 0)
        goal = PriorityCoordinate(5, 5)
        maze.updateVisited(start)
        maze.printVisited()
        # define a few points to check updates
        step1 = PriorityCoordinate(1, 0)
        step1.setParent(start)
        maze.updateVisited(step1)
        maze.printVisited()
        # define a few points to check updates
        step2 = PriorityCoordinate(1, 1)
        step2.setParent(step1)
        maze.updateVisited(step2)
        maze.printVisited()
        # define a few points to check updates
        step3 = PriorityCoordinate(1, 2)
        step3.setParent(step2)
        step3.getPath()

        # test equivalence or coordinate
        stepTest = PriorityCoordinate(1, 0)
        assert (stepTest == step1) == True
        assert (stepTest == start) == False

        # test maze
        assert maze.validCoordinate(PriorityCoordinate(6, 6)) == False
        assert maze.validCoordinate(PriorityCoordinate(0, 0)) == False
        assert maze.validCoordinate(PriorityCoordinate(0, 5)) == True
        assert maze.validCoordinate(PriorityCoordinate(6, 0)) == True
        assert maze.validCoordinate(PriorityCoordinate(5, 0)) == False
        assert maze.validCoordinate(PriorityCoordinate(5, 3)) == False
        assert maze.validCoordinate(PriorityCoordinate(1, 1)) == False

        # check printing
        print(start, step1, step2, step3)
        print(start.stepsToGoal(goal))
        print(step1.stepsToGoal(goal))
        print(step3.stepsToGoal(goal))

        # test queue
        myQueue = Queue()
        assert myQueue.isEmpty == True
        assert myQueue.dequeue() == None
        myQueue.enqueue('a', 5)
        myQueue.enqueue('b', 3)
        myQueue.enqueue('c', 7)
        assert myQueue.dequeue() == 'b'
        assert myQueue.dequeue() == 'a'
        assert myQueue.dequeue() == 'c'
        myQueue.enqueue(PriorityCoordinate(0, 0), 5)
        myQueue.enqueue(PriorityCoordinate(5, 5), 3)
        myQueue.enqueue(PriorityCoordinate(3, 2), 7)
        print(myQueue)
        assert myQueue.dequeue() == PriorityCoordinate(5, 5)
        assert myQueue.dequeue() == PriorityCoordinate(0, 0)
        assert myQueue.dequeue() == PriorityCoordinate(3, 2)
    except:
        return False
    return True


if __name__ == '__main__':
    # check tests
    print('-'*60)
    print(' '*25 + 'Start of test.')
    print('-'*60)
    assert test() == True
    print('-'*60)
    print(' '*25 + 'End of tests.')
    print('-'*60)
