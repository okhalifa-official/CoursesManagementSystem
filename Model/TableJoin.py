import DataModel as DM

class Graph:
    def __init__(self):
        self.g = {}
        self.visited = {}
        self.build_relations()

    
    def add_edge(self, src, dst):
        if src not in self.g:
            self.g[src] = []
        if dst not in self.g:
            self.g[dst] = []
        self.g[src].append(dst)
        self.g[dst].append(src)

    def build_relations(self):
        self.add_edge(DM.Students, DM.Student_Enrollment)
        self.add_edge(DM.Students, DM.Payments)
        self.add_edge(DM.Student_Enrollment, DM.Courses)
        self.add_edge(DM.Payments, DM.Courses)
        self.add_edge(DM.Courses, DM.Doctors)
    
    def display(self):
        for node, neighbors in self.g.items():
            print(f"{node}: {neighbors}")

# g = Graph()
# g.display()
