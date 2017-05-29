import random
import operator
import time
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
procList=[]
for i in range(procNum):
    procList.append(procStruct())

########   ABOVE:create procList



def newReadyProc_staticPrior():
    global waitPoint,blockPoint
    priors = {}
    for i in range(procNum):
        if procList[i].state =='f':
            continue
        priors[i] = priors.get(i,procList[i].prior)
    sortedPriors = sorted(priors.iteritems(),key=operator.itemgetter(1),reverse=True)
    index = sortedPriors[0][0]
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
        while (procList[n].next != -1):
            n = procList[n].next
        procList[n].next = index
    return


def nextRunProc():
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


def cpuSche():
    global runPoint,finish,clockNum,blockPoint
    if runPoint == -1:
        nextRunProc()
        return
    procList[runPoint].cpuTime -= 1
    if procList[runPoint].cpuTime > 0:
        return
    if procList[runPoint].serial[0] == procList[runPoint].pos:
        finish += 1
        procList[runPoint].state = 'f'
        procList[runPoint].prior = -1
        procList[runPoint].end = clockNum
        runPoint = -1
        nextRunProc()
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
        nextRunProc()
        #print [procList[i].state for i in range(procNum)]
    return


def ioSche():
    global blockPoint,finish,clockNum,waitPoint
    #blockShow()####
    if blockPoint == -1:
        return
    procList[blockPoint].ioTime -= 1
    if procList[blockPoint].ioTime > 0:
        return
    if procList[blockPoint].serial[0] == procList[blockPoint].pos:
        finish += 1
        procList[blockPoint].state = 'f'
        finishPoint = blockPoint
        procList[blockPoint].prior = -1
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


def staticPrior():
    global clockNum,finish,waitPoint
    procClock = []
    while finish < procNum:
        newReadyProc_staticPrior()
        clockNum+=1
        cpuSche()
        ioSche()
        '''procPer = []
        for n in range(procNum):
            p = []
            if procList[n].state == '0':
                continue
            p.append(procList[n].state)
            p.append(procList[n].pid)
            p.append(procList[n].prior)
            p.append(procList[n].start)
            t = 0
            if procList[n].state == 'f':
                t = procList[n].end - procList[n].start
            else:
                t = clockNum - procList[n].start
            p.append(t)
            procPer.append(p)
        procClock.append(procPer)'''
        print waitPoint, [procList[i].state for i in range(procNum)]
    return procClock
