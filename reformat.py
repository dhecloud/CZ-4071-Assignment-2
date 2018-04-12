def read_txt(name):
    with open(name, 'r') as f:
        lines = f.readlines()
        
    pop=[]
    for i in range(len(lines)):
        if lines[i][0] == '#':
            pop.append(i)
        lines[i] = lines[i].replace("\n","")
    for i in pop[::-1]:
        lines.pop(i)
    for i in range(len(lines)):
        lines[i] = lines[i].split("\t")
    return lines

def get_neighbours(edges):
    max =0
    for edge in edges:
        for maxtmp in edge:
            if int(maxtmp)>max:
                max=int(maxtmp)
    neighbours = [[None]] * (max+1)
    for i in range(len(edges)):
        neighbours[int(edges[i][0])] = neighbours[int(edges[i][0])] + [(int(edges[i][1]))]
    for i in range(len(neighbours)):
        if len(neighbours[i]) > 1:
            neighbours[i].pop(0)
    return neighbours
    
def write_adj_txt(name, neighbours):
    txt = ""
    for vertex in neighbours:
        for neighbour in vertex:
            if neighbour != None:
                txt += str(neighbour)
            if neighbour != vertex[len(vertex)-1]:
                txt += " "
        txt += "\n"
    with open("graph/" + name, "w") as f:
        f.write(txt)

def write_deg_txt(name, neighbours):
    txt = str(len(neighbours)) + "\n"
    for vertex in neighbours:
        if vertex[0] != None:
            txt += str(len(vertex)) 
        else:
            txt += "0"
        if vertex != neighbours[len(neighbours)-1]:
            txt += "\n"
    with open("graph/" + name, "w") as f:
        f.write(txt)

TXT_NAME = 'GrQc.txt'
edges = read_txt(TXT_NAME)
neighbours = get_neighbours(edges)
write_adj_txt(TXT_NAME.replace(".txt","_adj.txt"), neighbours)
write_deg_txt(TXT_NAME.replace(".txt","_deg.txt"), neighbours)