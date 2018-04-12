import time

class Graph:
    def __init__(self, dir, verbose):
        self.verbose = verbose
        self.dir = dir
        self.n = 0
        self.m = 0
        
        self.pstart = None
        self.edges = None
        print("Graph initalized!")
        
    def __del__(self):
        print('Destructor called, graph deleted')
        
    def read_graph(self):
        file1 = open(self.dir+ "/GrQc_deg.txt", 'r')
        
        self.n = int(file1.readline())
        self.m = int(file1.readline())
        
        print("\t n = {0}, m = {1}".format(self.n,self.m))
        
        degree = []
        for line in file1.readlines():
            degree.append(int(line))
        
        
        file1.close()
        
        file2 = open(self.dir+ "/GrQc_adj.txt", 'r')
        if self.pstart == None:
            self.pstart = [None] * (self.n+1)
        if self.edges == None:
            self.edges = [None] * (self.m)
        
        self.pstart[0] = 0
        for i in range(self.n):
            tmp = (file2.readline()).strip("\n").split(" ")
            if degree[i] > 0:
                for j in range(degree[i]):
                    if degree[i] != 0 or '0':
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
        for i in range(len(S)-1,-1,-1):
            u = S[i]
            ok = 1
            for i in range(self.pstart[u], self.pstart[u+1]):
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
        
        if self.verbose:
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


    def degree_two_kernel_and_remove_max_degree_without_contraction(self):     #LinearTime
        stime = time.time()

        tmp_edges = [None] * self.m
        for i in range(self.m):
            tmp_edges[i] = self.edges[i]

        tmp_start = [None] * (self.n+1)
        for i in range(0,self.n+1):
            tmp_start[i] = self.pstart[i]

        is1 = []
        for i in range(self.n):
            is1.append(1)

        bin_head = [-1] * self.n
        bin_next = [None] * self.n
        degree = [None] * self.n

        degree_ones = []
        degree_twos = []
        S = []
        modified_edges = []

        max_d = 0
        res = 0
        for i in range(self.n):
            degree[i] = int(self.pstart[i+1] - self.pstart[i])
            bin_next[i] = bin_head[degree[i]]
            bin_head[degree[i]] = i;

            if(degree[i] == 0):
                res += 1
            elif(degree[i] == 1):
                degree_ones.append(i)
            elif(degree[i] == 2):
                degree_twos.append(i)

            if(degree[i] > max_d):
                max_d = degree[i]

        fixed = [0] * self.n

        pend = [None] * self.n
        for i in range(self.n):
            pend[i] = self.pstart[i+1]

        kernel_size = inexact = 0
        first_time = 1
        S_size = len(S)
        kernel_edges = 0
        while(degree_ones or degree_twos or max_d >= 3):
            while(degree_ones or degree_twos):
                while(degree_ones):
                    u = degree_ones[-1]
                    degree_ones.pop()
                    if(not is1[u] or degree[u] != 1):
                        continue

                    cnt = 0
                    for j in range(self.pstart[u],pend[u]):
                        if(is1[self.edges[j]]):
                            cnt += 1
                            res += self.delete_vertex_lineartime(v=self.edges[j], pend=pend, is1=is1, degree=degree, degree_ones=degree_ones, degree_twos=degree_twos)
                    
                while(degree_twos and not degree_ones):
                    u = degree_twos[-1]
                    degree_twos.pop()
                    if(not is1[u] or degree[u] != 2):
                        continue
                    self.shrink(u, pend[u], is1)

                    u1 = self.edges[self.pstart[u]]
                    u2 = self.edges[self.pstart[u]+1]

                    pre = u
                    cnt = 1
                    while(u1 != u and degree[u1] == 2):
                        cnt += 1
                        self.shrink(u1, pend[u1], is1)
                        tmp = u1
                        if(self.edges[self.pstart[u1]] != pre):
                            u1 = self.edges[self.pstart[u1]]
                        else:
                            u1 = self.edges[self.pstart[u1]+1]
                        pre = tmp

                    if(u1 == u):
                        res += self.delete_vertex_lineartime(v=u, pend=pend, is1=is1, degree=degree, degree_ones=degree_ones, degree_twos=degree_twos)
                        continue

                    pre = u
                    while(degree[u2] == 2):
                        cnt += 1
                        self.shrink(u2, pend[u2], is1)

                        tmp = u2
                        if(self.edges[self.pstart[u2]] != pre):
                            u2 = self.edges[self.pstart[u2]]
                        else:
                            u2 = self.edges[self.pstart[u2]+1]
                        pre = tmp

                    if(u1 == u2):
                        res += self.delete_vertex_lineartime(u1, pend, is1, degree, degree_ones, degree_twos)
                        continue

                    self.shrink(u1, pend[u1], is1)
                    self.shrink(u2, pend[u2], is1)


                    if(cnt%2 == 1):
                        if(self.exist_edge(u1, u2, pend)):
                            res += self.delete_vertex_lineartime(v=u1, pend=pend, is1=is1, degree=degree, degree_ones=degree_ones, degree_twos=degree_twos)
                            res += self.delete_vertex_lineartime(v=u2, pend=pend, is1=is1, degree=degree, degree_ones=degree_ones, degree_twos=degree_twos)
                        elif(cnt > 1):
                            idx = self.pstart[pre]
                            if(self.edges[idx] == u2):
                                idx += 1
                            u = self.edges[idx]
                            self.edges[idx] = u1
                            if(not first_time):
                                modified_edges.append(((pre,u), u1))

                            u2 = pre
                            while(u != u1):
                                is1[u] = 0
                                tmp = u
                                if(self.edges[self.pstart[u]] == pre):
                                    u = self.edges[self.pstart[u]+1]
                                else:
                                    u = self.edges[self.pstart[u]]
                                S.append((tmp,u))
                                pre = tmp

                            self.edge_rewire(u1, pend, pre, u2)
                            if(not first_time):
                                modified_edges.append(((u1,pre), u2))
                    else:
                        v2 = v1 = pre
                        pre = u2
                        while(v1 != u1):
                            is1[v1] = 0
                            tmp = v1
                            if(self.edges[self.pstart[v1]] == pre):
                                v1 = self.edges[self.pstart[v1]+1]
                            else:
                                v1 = self.edges[self.pstart[v1]]
                            S.append((tmp,v1))
                            pre = tmp
                        v1 = pre
                        if(self.exist_edge(u1, u2, pend)):
                            degree[u1] -= 1
                            degree[u2] -= 1

                            if(degree[u1] == 2):
                                degree_twos.append(u1)
                            if(degree[u2] == 2):
                                degree_twos.append(u2)
                        else:
                            self.edge_rewire(u1, pend, v1, u2)
                            self.edge_rewire(u2, pend, v2, u1)
                            if(not first_time):
                                modified_edges.append(((u1,v1), u2))
                                modified_edges.append(((u2,v2), u1))

            if(first_time):
                S_size = len(S)
                first_time = 0
                for k in range(self.n):
                    if(is1[k] and degree[k] > 0):
                        kernel_size += 1
                        for j in range(self.pstart[k],pend[k]):
                            if(is1[self.edges[k]]):
                                kernel_edges += 1
                    else:
                        fixed[k] = 1

            while(not degree_ones and not degree_twos):
                while(max_d >= 3 and bin_head[max_d] == -1):
                    max_d -= 1
                if(max_d < 3):
                    break
                v = -1
                v = bin_head[max_d]
                while(v != -1):
                    tmp = bin_next[v]
                    if(is1[v] and degree[v] > 0):
                        if(degree[v] < max_d):
                            bin_next[v] = bin_head[degree[v]]
                            bin_head[degree[v]] = v
                        else:
                            S.append((v,self.n))
                            inexact += 1
                            res += self.delete_vertex_lineartime(v=v, pend=pend, is1=is1, degree=degree, degree_ones=degree_ones, degree_twos=degree_twos)
                            bin_head[max_d] = tmp
                            break
                    v = tmp
                if(v == -1):
                    bin_head[max_d] = -1

        for i in range(len(S)-1,-1,-1):
            u1 = S[i][0]        #access the first element of tuple
            u2 = S[i][1]        #access the second element of tuple
            assert(not is1[u1])

            if(u2 != self.n):
                if(not is1[u2]):
                    is1[u1] = 1
                    res += 1
                continue

            ok = 1
            for i in range(self.pstart[u1],self.pstart[u1+1]):
                if(is1[self.edges[i]]):
                    ok = 0
                    break

            if(ok):
                is1[u1] = 1
                res += 1

        etime = time.time()

        I = []
        for i in range(len(is1)):
            if is1[i] == 1:
                I.append(i)

        if self.verbose:
            print("\nMIS: {0}".format(I))
        print("\nDegree_two_path MIS: {0} (kernel (|V|,|E|): ({1},{2}), inexact reduction: {3})".format(res, kernel_size, kernel_edges, inexact))
        print("Took {0} seconds to get MIS\n".format(etime-stime))

        del bin_head
        del bin_next
        del degree_ones
        del pend


    def delete_vertex_lineartime(self, v, pend, is1, degree, degree_ones, degree_twos):
        is1[v] = 0
        res = 0
        for k in range(self.pstart[v],pend[v]):
            if(is1[self.edges[k]]):
                w = self.edges[k]
                degree[w] -= 1
                if(degree[w] == 0):
                    res += 1
                elif(degree[w] == 1):
                    degree_ones.append(w)
                elif(degree[w] == 2):
                    degree_twos.append(w)
        print("vertex {0} deleted".format(v))
        return res


    def shrink(self, u, end, is1):
        i = self.pstart[u]
        while(True):
            while(i < end and is1[self.edges[i]]):
                i += 1
            while(i < end and not is1[self.edges[end-1]]):
                end -= 1

            if(i >= end):
                break
            self.edges[i], self.edges[end-1] = self.edges[end-1], self.edges[i]     #swapping the elements


    def exist_edge(self, u, v, pend):
        if(pend[u] - self.pstart[u] < pend[v] - self.pstart[v]):
            for i in range(self.pstart[u],pend[u]):
                if(self.edges[i] == v):
                    return 1
            return 0
        for i in range(self.pstart[v],pend[v]):
            if(self.edges[i] == u):
                return 1
        return 0

    def edge_rewire(self, u, pend, v, w):
        for i in range(self.pstart[u],pend[u]):
            if(self.edges[i] == v):
                self.edges[i] = w
                return i
        print("WA in edge_rewire!")
        return 0
    '''
    def degree_two_kernel_and_remove_max_degree_with_contraction(self):
        
    
        
    def degree_two_kernel_dominate_lp_and_remove_max_degree_without_contraction(self):
        
    def greedy(self):
        
    def greedy_dynamic(self):
    
    def _general_swap(self, is, fixed=None):
        
    def _check_is(self, is, count):
    
    def _compute_upperbound(self, is, fixed=None):
        
    def _get_two_neighbours(self, u, is, u1, u2):
        
    def _get_other_neighbor(self, u, is, u1):
        
    def _self.exist_edge(self, u1, u2, pend = None):
    
    def _self.edge_rewire(self, u, u1, u2, pend = None):
    
    def _find_other_endpoint(self, u, v, is):
        
    def _remove_degree_one_two(self, degree_ones, degree_twos, is, degree, adj, S):
        
    def _lp_reduction(self, ids, ids_n, is, degree):
        
    def _self.shrink(self, u, end, is, tri=None):
        
    def _update_triangle(self, u1, u2, pend, is, adj, tri, degree, dominate, dominated):
        
    def _dominated_check(self, u, pend, is, tri, degree):
        
    def _compute_triangle_counts(self, tri, pend, adj, is, degree, dominate, dominated):
    
    def _construct_degree_increase(self, ids):
        
    '''

    #def delete_vertex(self, v, is, degree, pend=None, degree_ones=None, degree_twos=None, tri=None, adj=None, dominate=None, dominated=None, head=None, es=None, bin_head=None, bin_next=None, bin_pre=None):

if __name__ == "__main__":
    verbose = True          #set to false if too much print
    graph = Graph("graph", verbose)
    ans=True
    while ans:
        print("""
            1.BDOne
            2.Linear Time
            3.Exit
            """)
        ans =input("Choose your method:")
        if ans == "1":
            graph.read_graph()
            graph.degree_one_kernel_and_remove_max_degree()
        elif ans == "2":
            graph.read_graph()
            graph.degree_two_kernel_and_remove_max_degree_without_contraction()
        elif ans == "3":
            break
        else:
            print("\nNot a valid choice. Please try again")