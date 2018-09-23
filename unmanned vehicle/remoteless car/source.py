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
    methods = ['forward', 'backward']#, 'upward', 'downward', 'forward upward', 'backward upward', 'forward downward', 'backward downward']
    global_methods = ['turn_left', 'turn_right']#, 'tilt_left', 'tilt_right', 'tilt_left turn_right', 'tilt_right turn_left', 'tilt_left turn_left', 'tilt_right turn_right']
    track = []
    test = 0
    
    def __init__(self):
        self.define_methods()

        #position of body
        self.state = [0, 0, 0, 90, 0]
        self.prev_state = self.state.copy()

        self.knowledgebase = read_json("knowledgebase")
        write_json("position", {"x":0, "y":0, "tetha_xy":0})
        write_json("target", {"x":0, "y":0, "z":0})
        pass

    def define_methods(self):
        new_methods = []
        for x in self.global_methods:
            for y in self.methods:
                new_methods.append(x+" "+y)
            new_methods.append(x)
        self.methods.extend(new_methods)

    def tranform(self, state, target, tetha_x, tetha_y):
        hxy = math.hypot(state[0], state[1])
        hxyz = math.hypot(state[2], hxy)

        hxy = hxy*math.cos(self.deg2rad(tetha_x))
        hxyz = hxyz*math.sin(self.deg2rad(tetha_y))
        
        state_tetha_x, state_tetha_y = self.get_tetha(target)
##        print(hxy, hxyz, state_tetha_x)
        state[0] = hxy*math.cos(self.deg2rad(state_tetha_x))
        state[1] = hxy*math.sin(self.deg2rad(state_tetha_x))
        state[2] = hxyz*math.sin(self.deg2rad(state_tetha_y))

        return state

    def score_action(self, state, virtual_state_transform, target):
        score = []
        if not all([float(virtual_state_transform[i]) == float(format(state[i], ".4f")) for i in range(len(state))]):
            diff=[virtual_state_transform[i] - target[i] for i in range(len(self.state))]
            
            dtx, dty = self.get_tetha(self.diff(virtual_state_transform, target))

            diff[3] = dtx
            diff[4] = dty

            vst_tx, vst_ty = self.get_tetha(virtual_state_transform)
            vst = [0, 0, 0, vst_tx + virtual_state_transform[3], vst_ty + virtual_state_transform[4]]

            stx, sty = self.get_tetha(state)
            st = [0, 0, 0, stx + state[3], sty + state[4]]

            for i in range(len(self.state)):
                if i > 2:
                    
                    if abs(vst[i] - diff[i]) <= abs(st[i] - diff[i]):
                        if abs(target[i]-st[i]) != 0:
                            score.append(abs(target[i]-st[i])**-1)
                        
                else:
                    if float(format(diff[i], ".4f")) <= 0 and float(format(diff[i], ".4f")) >= -1*target[i]:
                        score.append(virtual_state_transform[i])
                
            return float(format(sum(score), ".4f"))

        else:
            return 0

    def eq(self, state1, state2):
        b = True
        for i in range(3):#len(self.state)):
            if state1[i] - state2[i] >= 0.9:
                b = False
            else:
                state2[i] = state1[i]

        if b:
            return False
        else:
            return True

    def diff(self, source, target):
        s = sum([1 for i in range(3) if target[i] > source[i]])
        if s >= 2:
            state2 = target
            state1 = source
        else:
            state2 = source
            state1 = target
        diff=[state1[i] - state2[i] for i in range(len(self.state))]

        return diff
    
    def reply(self, source, target):
        prev_source = 0
        relation = self.get_relation(source, target)
        print("source = {}, target={}".format(source, target))
        while self.eq(target, source) and source != prev_source:
            prev_source = source.copy()

            tx, ty = self.get_tetha(source)
            t = tx + source[3]
        
            if self.test: print("from = {} to {} val={}".format(source, target, t))
            
            #generate training and train
            self.train_knowledgebase()
            if self.test: print("len = {}".format(len(self.knowledgebase)))
            
            relation = self.get_relation(source, target)+" "+" ".join([str(x) for x in source[3:]])

            dtx, dty = self.get_tetha(self.diff(source, target))
            if self.test: print("relation = {}, angle away x={}, y={}".format(relation, dtx, dty))

            if relation in self.knowledgebase and 1==2:
                r = self.knowledgebase[relation]
                possible_action = r
                if self.test: print("in base")

            else:
                self.state = source.copy()
                state = source.copy()
                li = []
                dx = {}
                state_diagonal = sum([x**2 for x in target[:3]])**0.5
                for xx in self.knowledgebase:
                    xx_split = xx.split()
                    if float(xx_split[5]) == source[3] and float(xx_split[6]) == source[4]:
                        try_process = self.process(self.knowledgebase[xx], source)
                        virtual_state = try_process[1]
                        virtual_state = self.format_state(virtual_state)
                        
                        state_tetha_x, state_tetha_y = self.get_tetha(target)
                        virtual_state_tetha_x, virtual_state_tetha_y = self.get_tetha(virtual_state)

                        tetha_x = abs(state_tetha_x - virtual_state_tetha_x)
                        tetha_y = abs(state_tetha_y - virtual_state_tetha_y)

                        virtual_state_transform = self.tranform(virtual_state.copy(), target.copy(), tetha_x, tetha_y)
                        virtual_state_transform = self.format_state(virtual_state_transform)

                        score = self.score_action(state, virtual_state_transform, target)
                        if 1==1:# and "forward" == self.knowledgebase[xx]:
                            dx.setdefault(len(li), score)
                            x = (self.knowledgebase[xx], state_tetha_x, virtual_state_tetha_x, tetha_x, state_tetha_y, virtual_state_tetha_y, tetha_y, virtual_state, virtual_state_transform, score)
                            li.append(x)
                            if self.test:
                                print("[{}] stx={}, vstx={}, tx={}, vs={}, vst={}, d={}".format(x[0],
                                                                                                       format(x[1], ".0f"), format(x[2], ".0f"), format(x[3], ".0f"),
                                                                                                       [format(xx, ".4f") for xx in x[7][:4]],
                                                                                                       [format(xx, ".4f") for xx in x[8][:4]],
                                                                                                       x[9]))
                pd = self.sort_dict(dx)
                li = [li[x[0]] for x in pd if x[-1] == pd[0][-1]]

                pa_states = {}
                possible_actions = {}
                for x in li:
                    possible_actions.setdefault(x[0], len(x[0].split()))
                    pa_states.setdefault(x[0], x[7])
                    if self.test:
                        print("[{}] stx={}, vstx={}, tx={}, vs={}, vst={}, d={}".format(x[0],
                                                                                               format(x[1], ".0f"), format(x[2], ".0f"), format(x[3], ".0f"),
                                                                                               [format(xx, ".4f") for xx in x[7][:4]],
                                                                                               [format(xx, ".4f") for xx in x[8][:4]],
                                                                                               x[9]))
                pd = self.sort_dict(possible_actions)
                pd.reverse()
                
                if len(pd) >0:
                    possible_action = pd[0][0]
                else:
                    possible_action = ''

            print("reply = {}".format(possible_action))
            self.state = self.process(possible_action, source)[1].copy()
            source = self.state.copy()

            tx, ty = self.get_tetha(source)
            write_json("position", {"x":self.state[0], "y":self.state[1], "tetha_xy":tx})
            if self.test:
                print(self.state, "\n")
##                input()
        return 

    def get_tetha(self, state):
        hxy = math.hypot(state[0], state[1])
        hxyz = math.hypot(state[2], hxy)

##        print(hxy, hxyz, state)
        if state[1] == 0:
            tetha_x = 0
            
        elif state[0] == 0:
            tetha_x = 90
            
        else:
            tetha_x = abs(self.rad2deg(math.atan(state[1]/state[0])))


        if state[0] < 0 and state[1] > 0:
            tetha_x = 180 - tetha_x

        if state[0] <= 0 and state[1] < 0:
            tetha_x += 180

        if state[0] > 0 and state[1] < 0:
            tetha_x = 360 - tetha_x


        if state[2] == 0:
            tetha_y = 0
            
        elif hxy == 0:
            tetha_y = 90
            
        else:
            tetha_y = abs(self.rad2deg(math.atan(state[2]/hxy)))


        if hxy < 0 and state[2] > 0:
            tetha_y = 180 - tetha_y

        if hxy <= 0 and state[2] < 0:
            tetha_y += 180

        if hxy > 0 and state[2] < 0:
            tetha_y = 360 - tetha_y

        return tetha_x, tetha_y
    
    def sort_dict(self, dic, ascending=True):
        new = []
        if len(dic) > 0:
            d = dic.copy()
            while len(d) > 0:
                v = max(zip(d.values(), d.keys()))
                new.append((v[1],v[0]))
                d.pop(v[1])
        return new

    def format_state(self, state):
        for i in range(len(state)):
            state[i] = float(format(state[i], ".4f"))
        return state.copy()
    
    def train_knowledgebase(self):
        training = {}
        for action in self.methods:
            #reset position of body [length, width, height, xy plane angle, z-xy plane angle]
            state = self.state.copy()
            prev_state = state.copy()

            t, state = self.process(action, state)
            state = self.format_state(state)
            relation = self.get_relation(prev_state, state)
            
##            print("learned {} = from state {} to {} => {}".format(t, [format(x, ".4f") for x in prev_state[:4]], [format(x, ".4f") for x in state[:4]], relation.split()[:3]))

            val = relation+" "+" ".join([str(x) for x in prev_state[3:]])
            if t not in training:
                training.setdefault(val, t)
            else:
                if len(training[t].split()) > len(val.split()):
                    training[t] = val
                    
        self.knowledgebase.update(training.copy())
        write_json("knowledgebase", self.knowledgebase)

    def inc_tetha(self, val, op=1, inc=False):
        if inc == False:
            inc = 1

        if op == 1:
            new_val = inc + val

        else:
            new_val = val - inc
            
        if new_val >= -60 and new_val <= 60:
            val = new_val

        return val
    
    def tilt_right(self, state=False):
        if state == False:
            state = self.state

        state[4] -= 1
        return'tilt_right', state

    def tilt_left(self, state=False):
        if state == False:
            state = self.state
        state[4] += 1
        return'tilt_left', state

    def turn_left(self, state=False):
        if state == False:
            state = self.state

        state[3] = self.inc_tetha(state[3])
        return'turn_left', state

    def turn_right(self, state=False):
        if state == False:
            state = self.state

        state[3] = self.inc_tetha(state[3], -1)
        return'turn_right', state
    
    def upward(self, state=False):
        if state == False:
            state = self.state
        state[2] += 1*math.cos(self.deg2rad(state[4]))
        xy = math.sin(self.deg2rad(state[4]))
        
        state[0] += 1*xy*math.cos(self.deg2rad(state[3]))
        state[1] += 1*xy*math.sin(self.deg2rad(state[3]))
        return 'upward', state

    def downward(self, state=False):
        if state == False:
            state = self.state
        
        state[2] = -1*math.cos(self.deg2rad(state[4]))
        xy = math.sin(self.deg2rad(state[4]))
        
        state[0] = -1*xy*math.cos(self.deg2rad(state[3]))
        state[1] = -1*xy*math.sin(self.deg2rad(state[3]))
        return 'downward', state

    def forward(self, state=False):
        if state == False:
            state = self.state
        tx, ty = self.get_tetha(state)
        t = tx + state[3]
        
        state[0] += 1*math.cos(self.deg2rad(t))
        state[1] += 1*math.sin(self.deg2rad(t))
        return 'forward', state

    def backward(self, state=False):
        if state == False:
            state = self.state
        tx, ty = self.get_tetha(state)
        t = tx + state[3]
        
        state[0] += -1*math.cos(self.deg2rad(t))
        state[1] += -1*math.sin(self.deg2rad(t))
        return 'backward', state

    def status(self):
        if any([abs(self.target[i] - self.state[i]) < abs(self.target[i] - self.prev_state[i]) for i in range(3)]):
            return True

        else:
            return False

    def deg2rad(self, val):
        return val*math.pi/180

    def rad2deg(self, val):
        return val*180/math.pi
    
    def process(self, action, state=False):
        if state == False:
            state = self.state
        ret = ""
        actions = action.split()
        for action in actions:
            r = eval('self.'+action+'(['+", ".join([str(x) for x in state])+'])')
            ret += " "+r[0]+" "
            state = r[1].copy()
            ret = ret.strip()
        return ret.strip(), state
    
    def get_relation(self, state1= False, state2=False):
        for state in [state1, state2]:
            if len(state) != len(self.state):
                x, y = self.get_tetha(state)
                state.append(x)
                state.append(y)
                
        if state1 == False:
            state1 = self.prev_state

        if state2 == False:
            state2 = self.state

        r = ""
        diff = []
        
        for i in range(len(state1)):
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
    genetic_algorithm = GA()
    prev_target = 0
    genetic_algorithm.state = [0, 0, 0, 0, 0]
    while True:
        target = read_json("target")
        if target != prev_target:
            genetic_algorithm.reply([0, 0, 0, 0, 0], [target["x"], target["y"], target["z"]]) #make decision
            print("Done\n")
        prev_target = target
