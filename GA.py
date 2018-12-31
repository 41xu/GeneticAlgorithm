import math
import random

populationNum = 50000
chromoLen = 21 * 2  # 2D X in f1, therefore the chromosome len will be 21*2, 1-21: x1, 22-42: x2
maxX = 100
minX = -100
crossRate=0.7
mutationRate=0.01


def f1(x1, x2):
    return x1 * x1 + x2 * x2


def EncodingInit(populationNum, chromoLen):
    population = []
    for i in range(populationNum):
        temp = []
        for j in range(chromoLen):
            temp.append(random.randint(0, 1))
        population.append(temp)
    return population


def Decoding(population, chromoLen):
    X1 = []
    X2 = []
    for i in range(len(population)):
        temp = 0
        for j in range(0,chromoLen // 2):
            temp += population[i][j] * math.pow(2, j)
        X1.append(temp)
        temp = 0
        for j in range(chromoLen // 2, chromoLen):
            temp += population[i][j] * math.pow(2, j - chromoLen // 2)
        X2.append(temp)

    X1_ = [minX + xi * (maxX - minX) / (pow(2, chromoLen // 2) - 1) for xi in X1]
    X2_ = [minX + xi * (maxX - minX) / (pow(2, chromoLen // 2) - 1) for xi in X2]

    return X1_, X2_


def fitness1(X1, X2,population):
    # cal Y
    # Y is the actual value of function f1, smaller is better
    # while we calculate the fitness, the larger will be chose
    # the larger one should has the higher probability to be chose
    # therefore, we do some little trick on Y
    # we use (max of Y) - Y[i] to represent the fitness of Y[i]
    # So, the larger, the better

    Y = []
    for i in range(len(population)):
        Y.append(f1(X1[i], X2[i]))
    maxY = max(Y)
    for i in range(len(population)):
        Y[i] = maxY - Y[i]

    return Y


def selection(population, Y):  # Roulette Wheel Selection
    newPopulation = []
    if sum(Y)!=0:
        probY = [y / sum(Y) for y in Y]
    else:
        return None
    c = 0
    for (index, item) in enumerate(probY):
        c += item
        r = random.random()
        if r < c:
            newPopulation.append(population[index])
    return newPopulation

def crossover(newPopulation):
    for i in range(len(newPopulation)-1):
        r=random.random()
        if r<crossRate:
            point=random.randint(0,len(newPopulation[0])-1)
            temp1=[]
            temp2=[]
            temp1.extend(newPopulation[i][:point])
            temp1.extend(newPopulation[i+1][point:])
            temp2.extend(newPopulation[i+1][:point])
            temp2.extend(newPopulation[i][point:])
            newPopulation[i]=temp1
            newPopulation[i+1]=temp2
    return newPopulation

def mutation(newPopulation):
    for i in range(len(newPopulation)):
        r=random.random()
        if r<mutationRate:
            position=random.randint(0,chromoLen//2-1)
            if newPopulation[i][position]==1:
                newPopulation[i][position]=0
            else:
                newPopulation[i][position]=1
    return newPopulation

if __name__ == '__main__':
    totalPop=[]
    X=[]
    Y=[]
    population = EncodingInit(populationNum, chromoLen)
    totalPop.append(population)
    for i in range(populationNum):
        X1, X2 = Decoding(totalPop[-1], chromoLen)
        # print(X1,X2)
        y = fitness1(X1, X2,totalPop[-1])
        X.append([X1,X2])
        Y.append(y)
        newpop = selection(totalPop[-1], y)
        if newpop!=None:
            newpop = crossover(newpop)
            newpop = mutation(newpop)
            totalPop.append(newpop)
            # print(len(totalPop[-1]))
        else:
            break
    print("x1,x2:",X[-1])
    print("y:",Y[-1])





