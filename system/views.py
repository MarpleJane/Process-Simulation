from django.shortcuts import render

# Create your views here.
import algorithm.processModule as process
import json
from django.http import HttpResponse

clockFCFS = process.FCFS()
clockST = process.staticPrior()
clockDY = process.dynamicPrior()

'''def data(request, i):
    rlist = [['jack', 'chinese'], ['mike', 'english'], ['bob', 'math'],
             ['frank', 'art'], ['lucy', 'music']]
    rlist2 = []
    rlist2.append({'name': rlist[int(i)][0], 'subject': rlist[int(i)][1]})
    rjson = json.dumps(rlist2)
    response = HttpResponse()
    response['Content-Type'] = 'text/javascript'
    response.write(rjson)
    return response

def update(request):
    return render(request, 'test.html')
    '''

def index(request):
    return render(request, 'os.html')


def fcfsData(request, c):
    c = int(c)
    per = []
    num = len(clockFCFS[c-1])
    if num == 0:
        pass
    else:
        for p in xrange(num):
            per.append({'state': clockFCFS[c-1][p][0], 'pid': clockFCFS[c-1][p][1],
                        'prior': clockFCFS[c-1][p][2], 'start': clockFCFS[c-1][p][3],
                        'used': clockFCFS[c-1][p][4]})
    cjson = json.dumps(per)
    response = HttpResponse()
    response['Content-Type'] = 'text/javascript'
    response.write(cjson)
    return response


def fcfsUpdate(request):
    clock = len(clockFCFS)
    num = process.procNum
    contents = {'clock': clock, 'num':num}
    return render(request, 'fcfs.html', contents)


def staticData(request, c):
    c = int(c)
    per = []
    num = len(clockST[c-1])
    if num == 0:
        pass
    else:
        for p in xrange(num):
            per.append({'state': clockST[c-1][p][0], 'pid':clockST[c-1][p][1],
                        'prior': clockST[c-1][p][2], 'start': clockST[c-1][p][3],
                        'used': clockST[c-1][p][4]})
    cjson = json.dumps(per)
    response = HttpResponse()
    response['Content-Type'] = 'text/javascript'
    response.write(cjson)
    return response


def staticUpdate(request):
    clock = len(clockST)
    num = process.procNum
    contents = {'clock': clock, 'num': num}
    return render(request, 'staticPrior.html', contents)


def dynamicData(request, c):
    c = int(c)
    per = []
    num = len(clockDY[c-1])
    if num == 0:
        pass
    else:
        for p in xrange(num):
            per.append({'state': clockDY[c-1][p][0], 'pid':clockDY[c-1][p][1],
                        'prior': clockDY[c-1][p][2], 'start': clockDY[c-1][p][3],
                        'used': clockDY[c-1][p][4]})
    cjson = json.dumps(per)
    response = HttpResponse()
    response['Content-Type'] = 'text/javascript'
    response.write(cjson)
    return response


def dynamicUpdate(request):
    clock = len(clockDY)
    num = process.procNum
    contents = {'clock': clock, 'num': num}
    return render(request, 'dynamicPrior.html', contents)


def analysis(request):
    fcfsClock = len(clockFCFS)
    dyClock = len(clockDY)
    stClock = len(clockST)
    num = process.procNum
    contents = {'fcfsClock': fcfsClock, 'dyClock': dyClock, 'stClock': stClock,
                'num': num}
    return render(request, 'analysis.html', contents)
