import time

class Graph:
    def __init__(self, dir):
        self.dir = dir
        self.n = 0
        self.m = 0
        
        self.pstart = None
        self.edges = None
        print("Graph initalized!")
        
    def __del__(self):
        print('Destructor called, graph deleted')
        
    def read_graph(self):
        file1 = open(self.dir+ "/degreefigure2.txt", 'r')
        
        self.n = int(file1.readline())
        self.m = int(file1.readline())
        
        print("\t n={0}, m = {1}".format(self.n,self.m))
        
        degree = []
        for line in file1.readlines():
            degree.append(int(line))
        
        
        file1.close()
        
        file2 = open(self.dir+ "/figure2graph.txt", 'r')
        if self.pstart == None:
            self.pstart = [None] * (self.n+1)
        if self.edges == None:
            self.edges = [None] * (self.m)
        
        self.pstart[0] = 0;
        for i in range(self.n):
            if degree[i] > 0:
                tmp = (file2.readline()).strip("\n").split(" ")
                for j in range(degree[i]):
                    self.edges[self.pstart[i] + j] = int(tmp[j])
            
            self.pstart[i+1] = self.pstart[i] + degree[i]
        file2.close()
        
        del degree
        
        
        
    def degree_one_kernel_and_remove_max_degree(self):                  #BDOne
        
        stime = time.time()
        
        is1 = []
        for i in range(self.n):
            is1.append(1)
            
        bin_head = [-1] * self.n
        bin_next = [None] * self.n
        degree = [None] * self.n
        
        degree_ones = []
        S = []

        max_d = 0
        res = 0
        for i in range(self.n):
            degree[i] =  int(self.pstart[i+1] - self.pstart[i])
            bin_next[i] = bin_head[degree[i]]
            bin_head[degree[i]] = i

            if degree[i] == 0:
                res += 1
            elif degree[i] == 1:
                degree_ones.append(i)
            if degree[i] > max_d:
                max_d = degree[i]


        fixed = [0] * self.n
        
        kernel_size = 0
        first_time = 1
        z = 0
        while ((degree_ones) or (max_d >= 2)):                      #while not empty or max_d is >= 2
            while(degree_ones):
                u = degree_ones[-1]
                degree_ones.pop()
                if ((not is1[u]) or (degree[u] != 1)):
                    continue
                cnt = 0;
                for j in range(self.pstart[u], self.pstart[u+1]):
                    if (is1[self.edges[j]]):
                        cnt += 1
                        res += self.delete_vertex(v=self.edges[j], is1=is1, degree=degree, degree_ones=degree_ones)
                        
            if (first_time):
                first_time = 0;
                for k in range(self.n):
                    if ((is1[k]) and (degree[k] >0)):
                        kernel_size += 1
                    else:
                        fixed[k] = 1
            while not degree_ones:
                while ((max_d >= 2 ) and (bin_head[max_d] == -1)):
                    max_d -= 1
                if (max_d < 2):
                    break
                v = bin_head[max_d]
                while (v != -1):
                    tmp = bin_next[v]
                    if ((is1[v]) and (degree[v] > 0)):
                        if degree[v] < max_d:
                            bin_next[v] = bin_head[degree[v]]
                            bin_head[degree[v]] = v
                        else:
                            S.append(v)
                            res += self.delete_vertex(v=v, is1=is1, degree = degree, degree_ones = degree_ones)
                            bin_head[max_d] = tmp
                            break
                    v = tmp
                if (v==-1):
                    bin_head[max_d] = -1
                        
        for i in range(len(S)-1,0,-1):
            u = S[i]
            ok = 1
            for j in range(self.pstart[u], self.pstart[u+1]):
                if (is1[self.edges[i]]):
                    ok = 0
                    break
            if (ok):
                is1[u] = 1
                res+=1
        I = []
        for i in range(len(is1)):
            if is1[i] == 1:
                I.append(i)
        
        etime = time.time()
        
        print("\nMIS: {0}".format(I))
        print("\nDegree_one MIS: {0} (kernel |V|: {1}, inexact reduction: {2})".format(res, kernel_size, len(S)))
        print("Took {0} seconds to get MIS\n".format(etime-stime))
                
        del bin_head
        del bin_next
        del degree
    

    def delete_vertex(self, v, is1, degree, degree_ones):
        is1[v] = 0
        res = 0
        for k in range(self.pstart[v], self.pstart[v+1]):
            if(is1[int(self.edges[k])]):
                w = int(self.edges[k])
                degree[w] -= 1
                if degree[w] == 0:
                    res += 1
                elif (degree[w] == 1):
                    degree_ones.append(w)
        print("vertex {0} deleted".format(v))
        return res
        
    '''
    def degree_two_kernel_and_remove_max_degree_with_contraction(self):
        
    def degree_two_kernel_and_remove_max_degree_without_contraction(self):
        
    def degree_two_kernel_dominate_lp_and_remove_max_degree_without_contraction(self):
        
    def greedy(self):
        
    def greedy_dynamic(self):
    
    def _general_swap(self, is, fixed=None):
        
    def _check_is(self, is, count):
    
    def _compute_upperbound(self, is, fixed=None):
        
    def _get_two_neighbours(self, u, is, u1, u2):
        
    def _get_other_neighbor(self, u, is, u1):
        
    def _exist_edge(self, u1, u2, pend = None):
    
    def _edge_rewire(self, u, u1, u2, pend = None):
    
    def _find_other_endpoint(self, u, v, is):
        
    def _remove_degree_one_two(self, degree_ones, degree_twos, is, degree, adj, S):
        
    def _lp_reduction(self, ids, ids_n, is, degree):
        
    def _shrink(self, u, end, is, tri=None):
        
    def _update_triangle(self, u1, u2, pend, is, adj, tri, degree, dominate, dominated):
        
    def _dominated_check(self, u, pend, is, tri, degree):
        
    def _compute_triangle_counts(self, tri, pend, adj, is, degree, dominate, dominated):
    
    def _construct_degree_increase(self, ids):
        
    '''

    #def delete_vertex(self, v, is, degree, pend=None, degree_ones=None, degree_twos=None, tri=None, adj=None, dominate=None, dominated=None, head=None, es=None, bin_head=None, bin_next=None, bin_pre=None):

if __name__ == "__main__":
    graph = Graph("graph")
    graph.read_graph()
    graph.degree_one_kernel_and_remove_max_degree()