
'''
car = (car_id, car_index, car_length, car_orientation)
state = (grid_str, grid_size)
node = (state, parentID, depth, cost, heuristic)
problem = (domain, initial_state)
domain = func_actions(state), func_result(state,action),
         func_cost(s,a,p), func_heuristic(s,m,l,d),
         func_satisfies(state)
'''

# Arvores de pesquisa
class SearchTree:

    # construtor
    def __init__(self, problem, strategy='breadth'):
        self.problem = problem
        root = (self.problem[1], None, 0, 0, 0)
        self.open_nodes = [0]
        self.closed_nodes = []
        self.all_nodes = [root]
        self.strategy = strategy
        self.solution = None
        self.terminals = 0
        self.non_terminals = 0
        self.visited = set()


    def get_path(self, node):
        """
        Obtains the path travelled from the root of the tree until a passed node, using a recursion strategy.

        Parameters:
        - Node: (state, parentID, depth, cost, heuristic)
        """
        if node[1] is None:
            return [node[0]]
        path = self.get_path(self.all_nodes[node[1]])
        path += [node[0]]

        return path


    def search(self):
        """
        Applies the algorithm used to search for the solution.
        """
        while self.open_nodes:
            nodeID = self.open_nodes.pop(0)
            node = self.all_nodes[nodeID]

            # In case the goal has been achieved
            if self.problem[0][4](node[0]):
                self.solution = node
                self.terminals = len(self.open_nodes) + 1
                return self.get_path(node)

            lnewnodes = []
            self.non_terminals += 1

            # Expanding a new node for each possible action returned by func_actions, in case the noded has not been
            # previously visited
            for action in self.problem[0][0](node[0]):
                newstate = self.problem[0][1](node[0], action)
                if newstate not in self.visited:
                    newnode = (newstate, nodeID, node[2] + 1, 0, 0)
                    lnewnodes.append(len(self.all_nodes))
                    self.all_nodes.append(newnode)
                    self.visited.add(newstate)

            self.add_to_open(lnewnodes)
        return None


    def add_to_open(self, lnewnodes):
        """
        Adds the new nodes expanded on a new iteration of tree_search to the list of open nodes, according to the
        search strategy employed by student.py.

        Parameters:
        - lnewnodes: List of new nodes to be appended to open_nodes.
        """
        if self.strategy == 'breadth':
            self.open_nodes.extend(lnewnodes)
        elif self.strategy == 'depth':
            self.open_nodes[:0] = lnewnodes
        elif self.strategy == 'uniform':
            self.open_nodes.extend(lnewnodes)
            # self.open_nodes.sort(key=lambda n: n.cost)
            self.open_nodes.sort(key=lambda n: self.all_nodes[n][3])
        elif self.strategy == 'greedy':
            self.open_nodes.extend(lnewnodes)
            # self.open_nodes.sort(key=lambda n: n.heuristic)
            self.open_nodes.sort(key=lambda n: self.all_nodes[n][4])
        elif self.strategy == 'a*':
            self.open_nodes.extend(lnewnodes)
            # self.open_nodes.sort(key=lambda n: n.heuristic + n.cost)
            self.open_nodes.sort(key=lambda n: self.all_nodes[n][3] + self.all_nodes[n][4])

    def in_parent(self, node, state):
        if node[1] is None:
            return False
        if self.all_nodes[node[1]][0] == state:
            return True
        return self.in_parent(self.all_nodes[node[1]], state)
