from map_methods import piece_coordinates, create_map

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

    # obter o caminho (sequencia de estados) da raiz ate um no
    def get_path(self, node):
        if node[1] is None:
            return [node[0]]
        path = self.get_path(self.all_nodes[node[1]])
        path += [node[0]]

        return path

    # procurar a solucao
    def search(self, limit=None):
        while self.open_nodes:
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

            # procurar as ações possíveis a partir do Nó atualmente a ser expandido
            for a in self.problem[0][0](node[0]):                                       # for a in self.problem.domain.actions(node.state):
                # Para cada ação, determina-se o resultado, isto é, o novo nó
                newstate = self.problem[0][1](node[0], a)                               # newstate = self.problem.domain.result(node.state, a)
                # verificar se o novo nó não existe já no caminho investigado, para fazer pesquisa em profundidade sem repetição de estados
                # if not self.in_parent(node, newstate):
                # verificar se o novo nó não existe já no caminho investigado, para fazer pesquisa em profundidade sem repetição de estados
                if newstate[1] not in self.visited:
                    #newnode = SearchNode(newstate, node, node.depth + 1)
                    map = create_map(newstate[1])
                    a_coords = piece_coordinates(map, "A")

                    newnode_heuristic = 0
                    newnode_cost = self.problem[0][2](newstate, a, node[0])

                    if self.strategy == "greedy" or self.strategy == "a*":
                        newnode_heuristic = self.problem[0][3](("A", newstate[1]), (map[0] - a_coords[-1][0], 0), 4, 0)

                    #TODO: Tentar eliminar nós com heuristica demasiado elevada
                    newnode = (newstate, nodeID, node[2] + 1,node[-2] +  newnode_cost, newnode_heuristic)

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
                    
                    self.visited.add(newstate[1])

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
