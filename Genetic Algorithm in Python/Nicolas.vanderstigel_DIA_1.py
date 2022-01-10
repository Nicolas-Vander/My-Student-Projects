import random
import math
import numpy as np
import time
start_time = time.time()
class classTriplet : #Pour que cela soit plus pratique j'ai décidé d'utiliser une classe Triplet pour pouvoir manipuler plus facilement mes dictionnaires et mes listes
    def __init__(self, a, b, c):
        self.a=a
        self.b=b
        self.c=c
        self.cout=self.Cout() 
        
    def Affichage(self):
        print("a =",self.a,"b =",self.b,"c =",self.c)

    def __str__(self):
        return f"({self.a}, {self.b}, {self.c})"
    
    def Cout(self): #On charge le fichier excel donné
        cout = 0
        file = np.loadtxt('temperature_sample.csv', delimiter = ';', skiprows=1) #Ici j'ai choisis le fichier sample de base, mais on peut à tout moment le modifier ici
        for i in range(len([row[0] for row in file])): #on navigue dans la matrice en fonction du nombre de lignes dans celle-ci 
            a = self.a
            b = self.b
            c = self.c   
            somme = 0
            for n in range(c+1):
                somme += (a**n) * math.cos((b**n)* (math.pi) * file[i][0])#calcul de la fonction pour notre triplet                
            cout += abs(somme - file[i][1]) #on compare cette fonction avec les valeurs données
        return cout

def GenererIndividu(): #creation des triplets a,b,c
    a = round(random.uniform(0,1),4)
    b = random.randint(1,20)
    c = random.randint(1,20)
    triplet = classTriplet(a, b, c)
    return triplet

def GenererNIndividu(n): #On genere n individus au debut 
    compteur = 0
    while(compteur<n):
        listTriplet.append(GenererIndividu())
        compteur+=1
        
def NCroisement(n): #On croise les triplets entre 2 triplets pour en former 2 nouveaux 
    compteur = 0
    while(compteur<n):    
        triplet1 = random.randint(0, len(listTriplet) - 1)#On genere une position aleatoire pour recuperer le triplet 
        triplet2 = random.randint(0, len(listTriplet) - 1)
        nouveauTriplet1 = classTriplet(listTriplet[triplet1].a,listTriplet[triplet2].b, listTriplet[triplet2].c)
        nouveauTriplet2 = classTriplet(listTriplet[triplet2].a,listTriplet[triplet1].b, listTriplet[triplet2].c)
        listTriplet.append(nouveauTriplet1)
        listTriplet.append(nouveauTriplet2)
        compteur+=1    

def Mutation(positionTriplet): #on va faire muter une valeur dans un triplet aleatoire
    varriableTriplet = random.randint(0,2)
    a = listTriplet[positionTriplet].a
    b = listTriplet[positionTriplet].b #On modifie aleatoirement une des variables de notre triplet 
    c = listTriplet[positionTriplet].c
    if varriableTriplet == 0:
        a = round(random.uniform(0,1),4)
    if varriableTriplet == 1:
        b = random.randint(1,20)
    else:
        c = random.randint(1,20)
    triplet = classTriplet(a, b, c)
    del listTriplet[positionTriplet]
    return triplet

def NMutation(): #On effectue la mutation N fois
    compteur = 0
    while(compteur<10):
        positionAleatoire = random.randint(20, len(listTriplet) - 1)
        listTriplet.append(Mutation(positionAleatoire))
        compteur+=1
        
# %% Main
listTriplet = []
listParent = []
a = 0 # variable compteur
GenererNIndividu(100)#on genere n individus
listTriplet.sort(key=lambda x: x.cout)
listParent = listTriplet[:20].copy()
listTriplet = list(listParent)
listParent = []
while(a<7): #On effectue des croisements et des mutations sur 20 générations sur nos 20 meilleurs triplets 
    NCroisement(40)
    NMutation()
    listTriplet.sort(key=lambda x: x.cout)
    listParent = listTriplet[:20].copy()
    listTriplet = list(listParent)
    a+=1
# On affiche le meilleur résultat après 20 itérations
print("Mon triplet est:")
print(listTriplet[0].Affichage())
print("Avec un Cout de:",listTriplet[0].cout)
print("--- %s seconds ---" % (time.time() - start_time))
