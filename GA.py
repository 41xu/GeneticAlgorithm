import math
import random

populationNum = 500
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


def Decoding(pop, chromoLen):
    X1 = []
    X2 = []
    for i in range(len(pop)):
        temp = 0
        for j in range(0,chromoLen // 2):
            temp += pop[i][j] * pow(2, j)
        # print(temp)
        X1.append(temp)
        temp = 0
        for j in range(chromoLen // 2, chromoLen):
            temp += pop[i][j] * pow(2, j - chromoLen // 2)
        # print(temp)
        X2.append(temp)
    print("X1",X1)
    print("-----")
    print("X2",X2)
    print("-----")

    X1_ = [minX + xi * (maxX - minX) // (pow(2, chromoLen // 2) - 1) for xi in X1]
    X2_ = [minX + xi * (maxX - minX) // (pow(2, chromoLen // 2) - 1) for xi in X2]

    print("X1_",X1_)
    print("-----")
    print("X2_",X2_)
    print("-----")

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
    print("Y",Y)
    print("-----")
    maxY = max(Y)
    for i in range(len(population)):
        Y[i] = maxY - Y[i]
    print("process Y",Y)
    print("-----")

    return Y


def selection(population, Y):  # Roulette Wheel Selection
    newPopulation = []
    if sum(Y)!=0:
        probY = [y / sum(Y) for y in Y]
    else:
        return None
    print("probY",probY)
    print("----")
    c = 0
    for (index, item) in enumerate(probY):
        c += item
        r = random.random()
        if r < c:
            newPopulation.append([population[index]])
    for x in newPopulation:
        print(x)

    return newPopulation

def crossover(newPopulation):
    for i in range(len(newPopulation)-1):
        r=random.random()
        if r<crossRate:
            crossPoint1=random.randint(0,chromoLen-1)
            crossPoint2=random.randint(0,chromoLen-1)
            crossPoint3=random.randint(0,chromoLen-1)
            crossPoint4=random.randint(0,chromoLen-1)
            if crossPoint2>crossPoint1:
                temp1=newPopulation[i][crossPoint1:crossPoint2]
                temp2=newPopulation[i+1][crossPoint1:crossPoint2]
            else:
                temp1=newPopulation[i][crossPoint2:crossPoint1]
                temp2=newPopulation[i+1][crossPoint2:crossPoint1]
            if crossPoint4>crossPoint3:
                temp3=newPopulation[i][crossPoint3:crossPoint4]
                temp4=newPopulation[i+1][crossPoint3:crossPoint4]
            else:
                temp3=newPopulation[i][crossPoint4:crossPoint3]
                temp4=newPopulation[i+1][crossPoint4:crossPoint3]

            newPopulation[i]=newPopulation[i][:crossPoint1]+temp2+newPopulation[i][crossPoint2:chromoLen//2-1]+\
                             newPopulation[i][chromoLen//2:crossPoint3]+temp4+newPopulation[i][crossPoint4:]
            newPopulation[i+1]=newPopulation[i+1][:crossPoint1]+temp1+newPopulation[i+1][crossPoint2:chromoLen//2+1]+\
                               newPopulation[i+1][chromoLen//2:crossPoint3]+temp3+newPopulation[i+1][crossPoint4:]
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
    # totalPop=[]
    # X=[]
    # Y=[]
    # population = EncodingInit(populationNum, chromoLen)
    # totalPop.append(population)
    # for i in range(populationNum):

    #     X1, X2 = Decoding(totalPop[-1], chromoLen)
    #     # print(X1,X2)
    #     y = fitness1(X1, X2,totalPop[-1])
    #     X.append([X1,X2])
    #     Y.append(y)
    #     newpop = selection(totalPop[-1], y)
    #     if newpop!=None:
    #         newpop = crossover(newpop)
    #         newpop = mutation(newpop)
    #         totalPop.append(newpop)
    #         # print(len(totalPop[-1]))
    #     else:
    #         break
    # print("x1,x2:",X[-1])
    # print("y:",Y[-1])
    pop=EncodingInit(10,chromoLen)
    count=0
    temp=pop
    while count<10:
        pop=temp
        X1,X2=Decoding(pop,chromoLen)
        y=fitness1(X1,X2,pop)
        ys=selection(pop,y)
        if ys==None:
            break
        yc=crossover(ys)
        ym=mutation(yc)
        temp=ym
        count+=1
    print(temp)