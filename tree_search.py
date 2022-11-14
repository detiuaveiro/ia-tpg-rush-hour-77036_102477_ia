# Module: tree_search
# 
# This module provides a set o classes for automated
# problem solving through tree search:
#    SearchDomain  - problem domains
#    SearchProblem - concrete problems to be solved
#    SearchNode    - search tree nodes
#    SearchTree    - search tree with the necessary methods for searhing
#
#  (c) Luis Seabra Lopes
#  Introducao a Inteligencia Artificial, 2012-2019,
#  Inteligência Artificial, 2014-2019

from abc import ABC, abstractmethod
from map_methods import piece_coordinates, create_map

'''
NOTA: Usando tuplos em vez das classes SearchDomain e SearchProblem, tem-se:

domain = (func_actions(s),func_result(s,a),func_cost(s,a),func_heuristic(s,goal),func_satisfies(s))
problem = (domain, initial_state)
node = (state, parent, depth, cost, heuristic)
'''

'''
# Dominios de pesquisa
# Permitem calcular as accoes possiveis em cada estado, etc
class SearchDomain(ABC):

    # construtor
    @abstractmethod
    def __init__(self):
        pass

    # lista de accoes possiveis num estado
    @abstractmethod
    def actions(self, state):
        pass

    # resultado de uma accao num estado, ou seja, o estado seguinte
    @abstractmethod
    def result(self, state, action):
        pass

    # custo de uma accao num estado
    @abstractmethod
    def cost(self, state, action):
        pass

    # custo estimado de chegar de um estado a outro
    @abstractmethod
    def heuristic(self, state, goal):
        pass

    # test if the given "goal" is satisfied in "state"
    @abstractmethod
    def satisfies(self, state):
        pass


# Problemas concretos a resolver
# dentro de um determinado dominio
class SearchProblem:
    def __init__(self, domain, initial):
        self.domain = domain
        self.initial = initial

    def goal_test(self, state):
        return self.domain.satisfies(state)


# Nos de uma arvore de pesquisa
class SearchNode:
    def __init__(self, state, parent, depth=1, cost=0, heuristic=0):
        self.state = state
        self.parent = parent
        self.depth = depth
        self.cost = cost
        self.heuristic = heuristic

    # Função utilizada para verificar se um novo nó na pesquisa faz parte do estado do nó atual, isto é, se já fez parte do caminho
    # de pesquisa atual (sendo portanto um dos seus parentes)
    def in_parent(self, state):
        if self.parent is None:
            return False
        if self.parent.state == state:
            return True
        return self.parent.in_parent(state)

    def __str__(self):
        return "no(" + str(self.state) + "," + str(self.parent) + ")"

    def __repr__(self):
        return str(self)
'''

# Arvores de pesquisa
class SearchTree:

    # construtor
    def __init__(self, problem, strategy='breadth'):
        self.problem = problem
        ## root = SearchNode(problem.initial, None)
        root = (self.problem[1], None, 0, 0, 0)
        self.open_nodes = [0]
        self.closed_nodes = []
        self.all_nodes = [root]
        self.strategy = strategy
        self.solution = None
        self.terminals = 0
        self.non_terminals = 0
        '''
        self.highest_cost_nodes = []
        '''

    '''
    def get_operation(self, node):
        if node.parent is None:
            return []

        path = self.get_operation(node.parent)
        path += [node.action]
        return path
    '''
    @property
    def length(self):
        return self.solution.depth

    @property
    def avg_branching(self):
        return (self.terminals + self.non_terminals - 1) / self.non_terminals

    @property
    def cost(self):
        return self.solution.cost

    # obter o caminho (sequencia de estados) da raiz ate um no
    def get_path(self, node):
        '''
        if node.parent == None:
            return [node.state]
        path = self.get_path(node.parent)
        path += [node.state]
        return path
        '''
        if node[1] is None:
            return [node[0]]
        path = self.get_path(self.all_nodes[node[1]])
        path += [node[0]]

        return path

    # procurar a solucao
    def search(self, limit=None):
        while self.open_nodes != []:
            nodeID = self.open_nodes.pop(0)
            node = self.all_nodes[nodeID]
            self.closed_nodes.append(nodeID)
            # Se o nó atual é o objetivo, terminar a pesquisa
            if self.problem[0][-1](node[0]):                                             # if self.problem.goal_test(node[0]):
                self.solution = node
                self.terminals = len(self.open_nodes) + 1
                return self.get_path(node)

            # Caso contrário, expandir o nó, determinar os filhos, e adicionar à fila de pesquisa (se não atingirem o limite de profundidade/forem nós repetidos)
            lnewnodes = []
            self.non_terminals += 1

            '''
            # Primeiro verificar se a profundidade da árvore não ultrapassou já o limite, no caso de pesquisa em profundidade com limite
            if limit is None or node.depth < limit:
            '''

            # procurar as ações possíveis a partir do Nó atualmente a ser expandido
            for a in self.problem[0][0](node[0]):                                       # for a in self.problem.domain.actions(node.state):
                # Para cada ação, determina-se o resultado, isto é, o novo nó
                newstate = self.problem[0][1](node[0], a)                               # newstate = self.problem.domain.result(node.state, a)
                # verificar se o novo nó não existe já no caminho investigado, para fazer pesquisa em profundidade sem repetição de estados
                # if not self.in_parent(node, newstate):
                # verificar se o novo nó não existe já no caminho investigado, para fazer pesquisa em profundidade sem repetição de estados
                if newstate not in self.get_path(node):
                    #newnode = SearchNode(newstate, node, node.depth + 1)
                    map = create_map(newstate[1])
                    a_coords = piece_coordinates(map, "A")
                    newnode = (newstate, nodeID, node[2] + 1, node[-2] + self.problem[0][2](newstate, a, node[0]),
                               self.problem[0][3](("A", newstate[1]),
                               (map[0] - a_coords[-1][0],0),
                                4, 0))

                    '''
                    # Determinar custo acumulado do novo nó e, se for maior ou igual do que os maiores nós até ao momento, adicionar a highest_cost_nodes
                    if self.highest_cost_nodes == [] or newnode.cost > self.highest_cost_nodes[0].cost:
                        self.highest_cost_nodes = [newnode]
                    elif newnode.cost == self.highest_cost_nodes[0].cost:
                        self.highest_cost_nodes.append(newnode)
                    '''


                    if newstate[1] in [self.all_nodes[id][0][1] for id in self.open_nodes] or newstate[1] in [
                        self.all_nodes[id][0][1] for id in self.closed_nodes]:
                        # Novo estado já está presente num nó do conjunto (ABERTOS U FECHADOS)
                        state_id = [self.all_nodes.index(node) for node in self.all_nodes if node[0][1] == newstate[1]][0]

                        if newnode[3] < self.all_nodes[state_id][3]:
                            # Caso o novo nó tenha melhor custo do que o nó anterior corresponde a este estado
                            self.all_nodes[state_id] = newnode
                    else:
                        # Novo estado não está presente em nenhum nó do conjunto (ABERTOS U FECHADOS)
                        lnewnodes.append(len(self.all_nodes))
                        self.all_nodes.append(newnode)


            self.add_to_open(lnewnodes)

        return None

    # juntar novos nos a lista de nos abertos de acordo com a estrategia
    def add_to_open(self, lnewnodes):
        if self.strategy == 'breadth':
            self.open_nodes.extend(lnewnodes)
        elif self.strategy == 'depth':
            self.open_nodes[:0] = lnewnodes
        elif self.strategy == 'uniform':
            self.open_nodes.extend(lnewnodes)
            # self.open_nodes.sort(key=lambda n: n.cost)
            self.open_nodes.sort(key=lambda n: n[2])
        elif self.strategy == 'greedy':
            self.open_nodes.extend(lnewnodes)
            # self.open_nodes.sort(key=lambda n: n.heuristic)
            self.open_nodes.sort(key=lambda n: n[3])
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