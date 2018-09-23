import random
import json

def write_json(name, dictionary):
    content = json.dumps(dictionary)
    file = open(name+'.json', 'w')
    file.write(content)
    file.close()

def read_json(name):
    file = open(name+'.json', 'r')
    content = file.read()
    file.close()
    return json.loads(content)

class GA:
    methods = ['forward', 'backward']
    track = []
    
    def __init__(self):
        self.knowledgebase = read_json("knowledgebase")        
        pass

    def reply(self, source, target):
        relation = str(self.get_relation(source, target))
        print('knowledgebase = {}'.format(self.knowledgebase))
        r = self.knowledgebase[relation]
        print('reply = {}'.format(r))
        return r
    
    def learn(self):
        classes = self.get_classes()

        cl = {}
        for n in range(len(classes)):
            cl.setdefault(classes[n], [])
            for d in self.track:
                if d[0] == classes[n]:
                    cl[classes[n]].append((d[1], d[2]))
        #print("\n",cl)
        cl_m = {x:0 for x in cl}
        for x in cl:
            m = 1000
            for y in cl[x]:
                if y[-1] < m:
                    m = y[-1]
            cl_m[x] = m

        cl = {x:[y[0] for y in cl[x] if y[-1] == cl_m[x]] for x in cl}

        #print("\n", cl)
        cl_m = {x:0 for x in cl}
        for x in cl:
            m = 1000
            for y in cl[x]:
                if len(y) < m:
                    m = len(y)
            cl_m[x] = m

        cl_f = {x:[] for x in cl}
        for x in cl:
            for y in cl[x]:
                if len(y) == cl_m[x]:
                    if y not in cl_f[x]:
                        cl_f[x].append(y)
        #print("\n",cl_f)
        write_json("knowledgebase", cl_f)
        self.knowledgebase = cl_f
        
    def get_classes(self):
        li = list(set([x[0] for x in self.track]))
        return li
    
    def generate_training_data(self, length=10, state_start=-10, state_stop=10, target_start=-10, target_stop=10):
        self.training_data = []
        for x in range(length):
            val = (random.randint(state_start, state_stop), random.randint(target_start, target_stop))
            self.training_data.append(val)
        print("\n",'tarining data = {}'.format(self.training_data))
    
    def train(self, n_iterations=10):
        self.generate_training_data()
        for x in self.training_data:
            for i in range(n_iterations):
                self.evolve(x[0], x[-1])
            
    def evolve(self, state=0, target=10):
        self.state = state
        self.prev_state = self.state
        self.target = target
        
        self.relation = self.get_relation()
##        print('\nstate = {}, target = {}, relation = {}'.format(self.state, self.target, self.relation))

        track = ''
        self.ri = random.randint(0, len(self.methods)-1)
        counter = 0
        while self.state != self.target:
            counter += 1
            self.prev_state = self.state
            t = self.process()
            if not track.endswith(t):
                track += t

            if self.status() == False:
                self.ri = random.randint(0, len(self.methods)-1)
        
##        print("\n",'for relation {} track = {} in {} action times\n'.format(self.relation, track, counter))
        self.track.append((self.relation, track, counter))

    def forward(self):
        self.state += 1
        return '{forward}'

    def backward(self):
        self.state -= 1
        return '{backward}'

    def status(self):
##        print(self.state, self.target, self.prev_state)
        if abs(self.target - self.state) < abs(self.target - self.prev_state):
            return True

        else:
            return False

    def process(self):
        return eval('self.'+self.methods[self.ri]+'()')

    def get_relation(self, state=False, target=False):
        if state == False:
            state = self.state

        if target == False:
            target = self.target
            
        if target > state:
            return '1'
        elif target == state:
            return '-1'
        else:
            return '0'

if __name__ == '__main__':
    genetic_algorithm = GA()
##
##    #generate training and train
##    genetic_algorithm.train()
##
##    #learn from training
##    genetic_algorithm.learn()
    while True:
        genetic_algorithm.reply(input("Enter start position: "), input("Enter stop position: ")) #make decision
        print()
