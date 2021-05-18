import sys
import glob
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.shortcuts import ProgressBar

import tellurium as te
import roadrunner
import copy, sys, os, math, getopt, json, time, zipfile
import matplotlib.pyplot as plt
import matplotlib
import tkinter
matplotlib.use('TkAgg')

# zip file handle
zf = 0
numGenerations = 0
numPopulation = 0

def readModel (zf, generation, individual):
    fileName = "populations/generation_" + str(generation) + '/individual_' + str (individual) + '.txt'
    ant = zf.read (fileName).decode ("utf-8")
    return ant


def readSavedRun (fileName):
    global zf
    global numPopulation
    global numGenerations
    zf = zipfile.ZipFile (fileName, 'r')
    data = zf.read('summary.txt').decode("utf-8") 
    data = data.splitlines()
    numGenerations = int (data[5].split ('=')[1])
    numPopulation = int (data[6].split ('=')[1])
    print ("Number of Generations = ", numGenerations)
    print ("Size of population in each generation =", numPopulation)
  
def getBestIndivdials():
       p = []
       for i in range (numGenerations-1):
           p.append (readModel (zf, i, 0))
       return p
   
def plotFitness():
    data = zf.read('fitnessList.txt').decode("utf-8") 
    fitnesslist = json.loads (data)
    plt.figure(figsize=(8,5))
    plt.plot (fitnesslist)
    plt.show()
    
def plotAllFitness():
    if type (zf) == zipfile.ZipFile:
       zf.close()
    plt.figure(figsize=(8,5))
    for fileName in zipFileList:
        print (fileName)
        readSavedRun (fileName)
        data = zf.read('fitnessList.txt').decode("utf-8") 
        fitnesslist = json.loads (data)
        plt.plot (fitnesslist)  
        zf.close()
    plt.show()        

def getBestIndivdials():
       p = []
       for i in range (numGenerations-1):
           p.append (readModel (zf, i, 0))
       return p
       
def plotPopulationPlots (models):
    n = math.trunc (math.sqrt (len (models)))
    fig, axs = plt.subplots(n,n,figsize=(10,8))
    count = -1
    with ProgressBar() as pb:
         for i in pb(range (n)):
           for j in range (n):
              count += 1
              r = te.loada (models[count])
              m = r.simulate (0, 2, 100)
              axs[i, j].plot(m[:,0], m[:,1:])
    plt.setp(plt.gcf().get_axes(), xticks=[], yticks=[]);
    plt.show()

print ("Press x to exit")
print ("Commands: help, run, ant, list, fitness, evolution, allfitness, quit")

zipFileList = glob.glob('Model*.zip')
zipCompleter = WordCompleter(zipFileList, ignore_case=True)
   
dataRead = False   
while 1:
    user_input = prompt('>',
                        history=FileHistory('history.txt'),
                        completer=zipCompleter,
                       )
    if user_input == 'x' or user_input == "quit":
       if type (zf) == zipfile.ZipFile:
          zf.close()
       sys.exit()
    if user_input == 'help':
        print ("list                list all models")
        print ("evolution <model>   Plot grid of simulations from the best models per generation")
        print ("run <model>         Run a simulation of the best model in the loaded trial")
        print ("ant <model>         Print out the best antimony model for the loaded trial")
        print ("fitness <model>     PLot the best fitness profile for the loaded trial ")
        print ("allfitness          Plot all fitness profiles")
        print ("quit                Quit the program")
    if user_input == 'list':
        print ('\n'.join(zipFileList))
        #print (zipFileList)
    if user_input.split(' ')[0] == 'load': 
       fileName = user_input.split(' ')[1]
       readSavedRun (fileName) 
       dataRead = True
    if user_input.split(' ')[0] == 'fitness':
       fileName = user_input.split(' ')[1]
       readSavedRun (fileName) 
       dataRead = True  
       if dataRead:
          plotFitness()
       else:
          print ("Use: load filename")
    if user_input.split(' ')[0]  == 'evolution':
       fileName = user_input.split(' ')[1]
       readSavedRun (fileName) 
       dataRead = True       
       if dataRead:
           p = getBestIndivdials()
           plotPopulationPlots (p)               
       else:
           print ("Use: load filename")  
    if user_input == 'allfitness':
       plotAllFitness ()               
    if user_input.split(' ')[0]  == 'run':
       fileName = user_input.split(' ')[1]
       readSavedRun (fileName) 
       ant = readModel (zf, numGenerations-1, 0)
       r = te.loada (ant)
       #if user_input.split(' ')[2] != '':
       #    timeEnd = float (user_input.split(' ')[2])
       #else:
       timeEnd = 2
       m = r.simulate (0, timeEnd, 300)
       nFloats = r.getNumFloatingSpecies()
       plt.figure(figsize=(8,5))
       for i in range (nFloats):
           plt.plot (m[:,0], m[:,i+1])
       plt.show()
    if user_input.split(' ')[0]  == 'ant':
       fileName = user_input.split(' ')[1]
       readSavedRun (fileName) 
       dataRead = True       
       if dataRead:
          print (readModel(zf, numGenerations-1, 0))             
       else:
           print ("Use: load filename")  
       

    
       
       
    