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
    def __init__(self, state, parent, depth=1, cost=0, heuristic=0, action=None):
        self.state = state
        self.parent = parent
        self.depth = depth
        self.cost = cost
        self.heuristic = heuristic
        self.action = action

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


# Arvores de pesquisa
class SearchTree:

    # construtor
    def __init__(self, problem, strategy='a*'):
        self.problem = problem
        root = SearchNode(problem.initial, None)
        self.open_nodes = [root]
        self.strategy = strategy
        self.solution = None

        self.terminals = 0
        self.non_terminals = 0
        self.highest_cost_nodes = []

    def get_operation(self, node):
        if node.parent is None:
            return []

        path = self.get_operation(node.parent)
        path += [node.action]
        return path

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
        if node.parent == None:
            return [node.state]
        path = self.get_path(node.parent)
        path += [node.state]
        return path

    # procurar a solucao
    def search(self, limit=None):
        while self.open_nodes != []:
            node = self.open_nodes.pop(0)
            # Se o nó atual é o objetivo, terminar a pesquisa
            if self.problem.goal_test(node.state):
                self.solution = node
                self.terminals = len(self.open_nodes) + 1
                return self.get_path(node)

            # Caso contrário, expandir o nó, determinar os filhos, e adicionar à fila de pesquisa (se não atingirem o limite de profundidade/forem nós repetidos)
            lnewnodes = []
            self.non_terminals += 1

            # Primeiro verificar se a profundidade da árvore não ultrapassou já o limite, no caso de pesquisa em profundidade com limite
            if limit is None or node.depth < limit:
                # procurar as ações possíveis a partir do Nó atualmente a ser expandido
                for a in self.problem.domain.actions(node.state):
                    # Para cada ação, determina-se o resultado, isto é, o novo nó
                    newstate = self.problem.domain.result(node.state, a)

                    if newstate is None:
                        continue

                    # verificar se o novo nó não existe já no caminho investigado, para fazer pesquisa em profundidade sem repetição de estados
                    if not node.in_parent(newstate):
                        newnode = SearchNode(newstate, node, node.depth + 1)                # CHANGES

                        # Determinar custo acumulado do novo nó e, se for maior ou igual do que os maiores nós até ao momento, adicionar a highest_cost_nodes
                        if self.highest_cost_nodes == [] or newnode.cost > self.highest_cost_nodes[0].cost:
                            self.highest_cost_nodes = [newnode]
                        elif newnode.cost == self.highest_cost_nodes[0].cost:
                            self.highest_cost_nodes.append(newnode)

                        lnewnodes.append(newnode)

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
            self.open_nodes.sort(key=lambda n: n.cost)
        elif self.strategy == 'greedy':
            self.open_nodes.extend(lnewnodes)
            self.open_nodes.sort(key=lambda n: n.heuristic)
        elif self.strategy == 'a*':
            self.open_nodes.extend(lnewnodes)
            self.open_nodes.sort(key=lambda n: n.heuristic + n.cost)
