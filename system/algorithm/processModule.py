import random
import operator
import copy
import pdb

global clockNum,waitPoint,runPoint,blockPoint,finish
clockNum = 0
waitPoint = -1
runPoint = -1
blockPoint = -1
finish = 0

class procStruct(object):
    def __init__(self):
        self.pid = random.randint(0,1000) #proc id
        self.state = '0' #wait||run||blocked||finish \
                       #'b'-block 'w'-wait 'r'-run 'f'-finish
        self.prior = random.randint(0,100) #priority
        self.start = random.randint(1,10) #create time   #######
        self.end = 0 #finish time
        self.serial = [random.randint(6,12)] #cycle data
        for i in range(self.serial[0]):
            self.serial.append(random.randint(5,15))
        self.pos = 1 #position in serial
        self.cpuTime = self.serial[1] #rest of cpu time
        self.ioTime = self.serial[2] #rest of io time
        self.next = -1

procNum = random.randint(5,10)
procFCFS = []
for i in range(procNum):
    procFCFS.append(procStruct())

procDY = copy.deepcopy(procFCFS)
procST = copy.deepcopy(procFCFS)
########   ABOVE:create procList
    


def newReadyProc_FCFS(procList):
    global clockNum,waitPoint
    for i in range(procNum):
        if procList[i].start == clockNum:
            procList[i].state = 'w'
            procList[i].next = -1
            if waitPoint == -1:
                waitPoint = i
            else:
                n = waitPoint
                while(procList[n].next!=-1):
                    n = procList[n].next
                procList[n].next = i
    return


def newReadyProc_staticPrior(procList):
    """
    detect a process with the highest prior
    """
    global waitPoint, blockPoint, clockNum
    
    priors = {}
    for i in range(procNum):
        if procList[i].state == 'f':
            continue
        priors[i] = priors.get(i,procList[i].prior)
    sortedPriors = sorted(priors.iteritems(),key=operator.itemgetter(1),reverse=True)
    index = sortedPriors[0][0]
    if procList[index].state == '0':
        procList[index].start = clockNum
    if procList[index].state == 'r' or index == waitPoint:
        return
    w = waitPoint
    while (procList[w].next != -1):
        if index == procList[w].next:
            procList[w].next = procList[procList[w].next].next
            break
        w = procList[w].next
    procList[index].state = 'w'
    if index == blockPoint:
        blockPoint = procList[blockPoint].next
    b = blockPoint
    while (procList[b].next != -1):
        if index == procList[b].next:
            procList[b].next = procList[procList[b].next].next
            break
        b = procList[b].next
    procList[index].next = -1
    if waitPoint == -1:
        waitPoint = index
    else:
        n = waitPoint
        while(procList[n].next != -1):
            n = procList[n].next
        procList[n].next = index
    return


def newReadyProc_dynamicPrior(procList):
    """
    detect a process with the highest prior
    """
    global waitPoint, blockPoint, clockNum
    
    priors = {}
    for i in range(procNum):
        if procList[i].state == 'f':
            continue
        priors[i] = priors.get(i,procList[i].prior)
    sortedPriors = sorted(priors.iteritems(),key=operator.itemgetter(1),reverse=True)
    index = sortedPriors[0][0]
    if procList[index].state == '0':
        procList[index].start = clockNum
    if procList[index].state == 'r' or index == waitPoint:
        return
    w = waitPoint
    while (procList[w].next != -1):
        if index == procList[w].next:
            procList[w].next = procList[procList[w].next].next
            break
        w = procList[w].next
    procList[index].state = 'w'
    if index == blockPoint:
        blockPoint = procList[blockPoint].next
    b = blockPoint
    while (procList[b].next != -1):
        if index == procList[b].next:
            procList[b].next = procList[procList[b].next].next
            break
        b = procList[b].next
    procList[index].next = -1
    if waitPoint == -1:
        waitPoint = index
    else:
        n = waitPoint
        while(procList[n].next != -1):
            n = procList[n].next
        procList[n].next = index
    return



def nextRunProc(procList):
    global waitPoint,runPoint
    if waitPoint == -1:
        runPoint = -1
        return
    procList[waitPoint].state = 'r'
    runPoint = waitPoint
    procList[waitPoint].cpuTime = procList[waitPoint].serial[procList[waitPoint].pos]
    waitPoint = procList[waitPoint].next
    procList[runPoint].next = -1
    return


def cpuSche(procList):
    global runPoint,finish,clockNum,blockPoint
    if runPoint == -1:
        nextRunProc(procList)
        return
    procList[runPoint].cpuTime -= 1
    if procList[runPoint].cpuTime > 0:
        return
    if procList[runPoint].serial[0] == procList[runPoint].pos:
        finish += 1
        procList[runPoint].state = 'f'
        procList[runPoint].end = clockNum
        runPoint = -1
        nextRunProc(procList)
    else: #go into the blocklist
        #print 'yes'
        procList[runPoint].pos += 1
        procList[runPoint].state = 'b'
        procList[runPoint].ioTime = procList[runPoint].serial[procList[runPoint].pos]
        n = blockPoint
        if n == -1:
            blockPoint = runPoint
        else:
            while(procList[n].next != -1):
                n = procList[n].next
            procList[n].next = runPoint
        runPoint = -1
        nextRunProc(procList)
        #print [procList[i].state for i in range(procNum)]
    return


def cpuScheDY(procList):
    global runPoint,finish,clockNum,blockPoint
    if runPoint == -1:
        nextRunProc(procList)
        return
    procList[runPoint].cpuTime -= 1
    procList[runPoint].prior -= 1
    if procList[runPoint].cpuTime > 0:
        return
    if procList[runPoint].serial[0] == procList[runPoint].pos:
        finish += 1
        procList[runPoint].state = 'f'
        procList[runPoint].end = clockNum
        runPoint = -1
        nextRunProc(procList)
    else: #go into the blocklist
        #print 'yes'
        procList[runPoint].pos += 1
        procList[runPoint].state = 'b'
        procList[runPoint].ioTime = procList[runPoint].serial[procList[runPoint].pos]
        n = blockPoint
        if n == -1:
            blockPoint = runPoint
        else:
            while(procList[n].next != -1):
                n = procList[n].next
            procList[n].next = runPoint
        runPoint = -1
        nextRunProc(procList)
        #print [procList[i].state for i in range(procNum)]
    return


def ioSche(procList):
    global blockPoint,finish,clockNum,waitPoint
    if blockPoint == -1:
        return
    procList[blockPoint].ioTime -= 1
    if procList[blockPoint].ioTime > 0:
        return
    if procList[blockPoint].serial[0] == procList[blockPoint].pos:
        finish += 1
        procList[blockPoint].state = 'f'
        procList[blockPoint].end = clockNum
        if procList[blockPoint].next == -1:
            blockPoint = -1
            return
        else:
            n = procList[blockPoint].next
            procList[blockPoint].next = -1
            blockPoint = n
            procList[blockPoint].ioTime = procList[blockPoint].serial[procList[blockPoint].pos]
            return
    else:  #go into the waitList(jiu xu)
        bk = blockPoint
        blockPoint = procList[blockPoint].next
        procList[bk].pos += 1
        procList[bk].state = 'w'
        procList[bk].next = -1
        n = waitPoint
        if n == -1:
            waitPoint = bk
            return
        else: #end of the waitList
            while(procList[n].next != -1):
                n = procList[n].next
            procList[n].next = bk
    return


c1 = 0
def FCFS():
    global clockNum, finish, waitPoint, runPoint, blockPoint, c1
    procClock = []
    while finish < procNum:
        clockNum += 1
        newReadyProc_FCFS(procFCFS)
        cpuSche(procFCFS)
        ioSche(procFCFS)
        procPer = []
        for n in range(procNum):
            p = []
            if procFCFS[n].state == '0':
                continue
            p.append(procFCFS[n].state)
            p.append(procFCFS[n].pid)
            p.append(procFCFS[n].prior)
            p.append(procFCFS[n].start)
            t = 0
            if procFCFS[n].state == 'f':
                t = procFCFS[n].end - procFCFS[n].start
            else:
                t = clockNum - procFCFS[n].start
            p.append(t)
            procPer.append(p)
        procClock.append(procPer)
        #print [ procFCFS[i].state for i in range(procNum) ]
    c1 = clockNum
    clockNum = 0
    finish = 0
    waitPoint = -1
    runPoint = -1
    blockPoint = -1
    return procClock


c2 = 0
def staticPrior():
    global clockNum, finish, waitPoint, runPoint, blockPoint, c2
    procClock = []
    while finish < procNum:
        clockNum += 1
        newReadyProc_staticPrior(procST)
        cpuSche(procST)
        ioSche(procST)
        procPer = []
        for n in range(procNum):
            p = []
            if procST[n].state == '0':
                continue
            p.append(procST[n].state)
            p.append(procST[n].pid)
            p.append(procST[n].prior)
            p.append(procST[n].start)
            t = 0
            if procST[n].state == 'f':
                t = procST[n].end - procST[n].start
            else:
                t = clockNum - procST[n].start
            p.append(t)
            procPer.append(p)
        procClock.append(procPer)
        
        
        #print [ procST[i].state for i in range(procNum) ]
    c2 = clockNum
    clockNum = 0
    finish = 0
    waitPoint = -1
    runPoint = -1
    blockPoint = -1
    return procClock

        
c3 = 0
def dynamicPrior():
    global clockNum, finish, waitPoint, c3
    procClock = []
    while finish < procNum:
        #pdb.set_trace()
        clockNum += 1
        newReadyProc_dynamicPrior(procDY)    
        cpuScheDY(procDY)
        ioSche(procDY)
        procPer = []
        for n in range(procNum):
            p = []
            if procDY[n].state == '0':
                continue
            p.append(procDY[n].state)
            p.append(procDY[n].pid)
            p.append(procDY[n].prior)
            p.append(procDY[n].start)
            t = 0
            if procDY[n].state == 'f':
                t = procDY[n].end - procDY[n].start
            else:
                t = clockNum - procDY[n].start
            p.append(t)
            procPer.append(p)
        procClock.append(procPer)
        #print [ procDY[i].state for i in range(procNum) ]
    c3 = clockNum
    clockNum = 0
    finish = 0
    waitPoint = -1
    runPoint = -1
    blockPoint = -1
    return procClock

