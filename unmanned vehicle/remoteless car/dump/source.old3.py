import random, math
import json

from turtle import *

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
    methods = ['forward', 'backward', 'upward', 'downward', 'forward upward', 'backward upward', 'forward downward', 'backward downward']
    global_methods = ['turn_left', 'turn_right', 'tilt_left', 'tilt_right', 'tilt_left turn_right', 'tilt_right turn_left', 'tilt_left turn_left', 'tilt_right turn_right']
    track = []
    
    def __init__(self):
        self.define_methods()

        #position of body
        self.state = [0, 0, 0, 0, 0]
        self.prev_state = self.state.copy()

        self.knowledgebase = read_json("knowledgebase")        
        pass

    def define_methods(self):
        new_methods = []
        for x in self.global_methods:
            for y in self.methods:
                new_methods.append(x+" "+y)
            new_methods.append(x)
        self.methods.extend(new_methods)
        
    def reply(self, source, target):
        relation = str(self.get_relation(source, target))
##        print('knowledgebase = {}'.format(self.knowledgebase))

        if relation in self.knowledgebase:
            r = self.knowledgebase[relation]
            print('reply = {}'.format(r))
            a = [float(x) for x in relation.split()]

        else:
            r = ""
            dx = relation.split()
            match = {}
            for x in self.knowledgebase:
                test = sum([1 for xx in range(len(self.state)) if dx[xx] == x.split()[xx]])
                if test > 1:
                    match.setdefault(x, test)
            print(self.sort_dict(match)[:10])
            a = [0, 0, 0]
            
        setposition(0, 0)
        clear()
        setposition(a[1]*100, a[2]*100)
        return r

    def sort_dict(self, dic, ascending=True):
        new = []
        if len(dic) > 0:
            d = dic.copy()
            while len(d) > 0:
                v = max(zip(d.values(), d.keys()))
                new.append((v[1],v[0]))
                d.pop(v[1])
        return new
    
    def train_knowledgebase(self):
        training = {}
        for action in self.methods:
            #reset position of body [length, width, height, xy plane angle, z-xy plane angle]
            state = [0, 0, 0, 0, 0]
            prev_state = state.copy()

            t = self.process(action)
            relation = self.get_relation(prev_state, state)
            print("learned {} = from state {} to {} => {}".format(t, [format(x, ".2f") for x in self.prev_state], [format(x, ".2f") for x in self.state], relation))

            if t not in training:
                training.setdefault(relation, t)

        for x in training:
            print(x)
        write_json("knowledgebase", training)
        self.knowledgebase = training

    def tilt_right(self):
        self.state[4] += 1
        return'tilt_right'

    def tilt_left(self):
        self.state[4] -= 1
        return'tilt_left'

    def turn_left(self):
        self.state[3] -= 1
        return'turn_left'

    def turn_right(self):
        self.state[3] += 1
        return'turn_right'
    
    def upward(self):
        self.state[2] += math.cos(self.deg2rad(self.state[4]))
        xy = math.sin(self.deg2rad(self.state[4]))
        
        self.state[0] += xy*math.cos(self.deg2rad(self.state[3]))
        self.state[1] += xy*math.sin(self.deg2rad(self.state[3]))
        return 'upward'

    def downward(self):
        self.state[2] -= math.cos(self.deg2rad(self.state[4]))
        xy = math.sin(self.deg2rad(self.state[4]))
        
        self.state[0] -= xy*math.cos(self.deg2rad(self.state[3]))
        self.state[1] -= xy*math.sin(self.deg2rad(self.state[3]))
        return 'downward'

    def forward(self):
        self.state[0] += math.cos(self.deg2rad(self.state[3]))
        self.state[1] += math.sin(self.deg2rad(self.state[3]))
        return 'forward'

    def backward(self):
        self.state[0] -= math.cos(self.deg2rad(self.state[3]))
        self.state[1] += math.sin(self.deg2rad(self.state[3]))
        return 'backward'

    def status(self):
        if any([abs(self.target[i] - self.state[i]) < abs(self.target[i] - self.prev_state[i]) for i in range(3)]):
            return True

        else:
            return False

    def deg2rad(self, val):
        return val*math.pi/180

    def rad2deg(self, val):
        return val*180/math.pi
    
    def process(self, action):
        ret = ""
        actions = action.split()
        for action in actions:
            ret += " " + eval('self.'+action+'()') +" "
            ret = ret.strip()
        return ret.strip()
    
    def get_relation(self, state1= False, state2=False):
        if state1 == False:
            state1 = self.prev_state

        if state2 == False:
            state2 = self.state

        r = ""
        diff = []
        for i in range(len(self.state)):
            if state2[i] > state1[i]:
                r += ' 1 '
            elif state2[i] == state1[i]:
                r += ' 0 '
            else:
                r += ' -1 '
            diff.insert(i, state2[i]-state1[i])
            r = r.strip()

        return r.strip()
    
if __name__ == '__main__':
##    mainloop()

    genetic_algorithm = GA()

    #generate training and train
    genetic_algorithm.train_knowledgebase()
    while True:
        genetic_algorithm.reply([int(x) for x in input("Enter start position: ").split()]+[0, 0], [int(y) for y in input("Enter stop position: ").split()]+[0, 0]) #make decision
        print()
