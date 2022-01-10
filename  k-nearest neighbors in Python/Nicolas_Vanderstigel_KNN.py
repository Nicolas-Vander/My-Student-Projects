# -*- coding: utf-8 -*-
import random
import time 

class KNN : #Je crée une classe Fleur afin de lui donner comme attribut toutes les valeurs qui lui sont attribuées 
    def __init__(self, coord_1, coord_2, coord_3, coord_4, coord_5, coord_6, classe):
        self.coord_1=float(coord_1)
        self.coord_2=float(coord_2)
        self.coord_3=float(coord_3)
        self.coord_4=float(coord_4)
        self.coord_5=float(coord_5)
        self.coord_6=float(coord_6)
        self.classe = str(classe) 
        
    def Affichage(self): #Cette fonction permet d'afficher toutes les données d'une fleur  
        print("coord_1 =",self.coord_1 ,"\ncoord_2 =",self.coord_2,
              "\ncoord_3 =",self.coord_3, "\ncoord_4 =", 
              self.coord_4, "\ncoord_5 =",self.coord_5,
              "\ncoord_6 =",self.coord_6 ,"\nClasse :", self.classe)

#On crée notre liste des différentes classes possibles
allLabels = ['classA','classB','classC','classD','classE']
dim=len(allLabels)        
#on train avec data, on teste avec pretest et on evalue avec finaltest

#traitement du fichier comprenant toutes les données des fleurs
def Extraire_Data(data):
    with open(data, 'r') as file:
        lines = file.readlines()
        listeDeKNN=[]
        for line in lines[:len(lines)-1]:#On navigue dns les lignes de notre fichier de données
            valeur = line.split(",")#On sépare les lignes en fonction des virgules
            fleur = KNN(valeur[0],valeur[1],valeur[2],valeur[3],valeur[4],valeur[5],valeur[6][:6])#on donne a notre fleur les bonnes coordonnées
            listeDeKNN.append(fleur) #On remplit la liste avec toutes nos différentes fleurs 
    return listeDeKNN
#fin du remplissage de la liste des données

#traitement du fichier comprenant toutes les données des fleurs sauf qu'on ne connait pas leur classe
def Extraire_Data_inconnu(data):
    with open(data, 'r') as file:
        lines = file.readlines()
        listeDeKNN=[]
        for line in lines[:len(lines)-1]:#On navigue dns les lignes de notre fichier de données
            valeur = line.split(",")#On sépare les lignes en fonction des virgules
            fleur = KNN(valeur[0],valeur[1],valeur[2],valeur[3],valeur[4],valeur[5],"")#on donne a notre fleur les bonnes coordonnées
            listeDeKNN.append(fleur) #On remplit la liste avec toutes nos différentes fleurs 
    return listeDeKNN
#fin du remplissage de la liste des données avec à chaque fois l'attribut classe vide

#permet d'enregistrer sur fichier tous les labels trouvés
def Enregistrer_Labels(nameFile,labels):
    myFile = open(nameFile,"w")
    for label in labels:
        myFile.write(label+"\n")
    myFile.close()


#permet d'afficher ma liste de data au cas ou j'en aurai besoin
def Afficher_Data(listeDeKNN):
    for i in range (len(listeDeKNN)):
        listeDeKNN[i].Affichage()

def Check_txt(nameFile,nbLines):
    fd =open(nameFile,'r')
    lines = fd.readlines()
    count=0
    for label in lines:
    	if label.strip() in allLabels:
    		count+=1
    	else:
    		if count<nbLines:
    			print("Wrong label line:"+str(count+1))
    			break
    if count<nbLines:
    	print("Labels Check : fail!")
    else:
    	print("Labels Check : Successfull!")



#Méthode qui calcule la distance euclidienne entre les 6 coordonnées de 2 fleurs
#data= une fleur du dataset (data.csv)
#inconnu= la fleur inconnue dont on cherche le type
def Distance_Euclidienne(data,inconnu):
    return ((data.coord_1-inconnu.coord_1)**2+(data.coord_2-inconnu.coord_2)**2+
            (data.coord_3-inconnu.coord_3)**2+(data.coord_4-inconnu.coord_4)**2
            +(data.coord_5-inconnu.coord_5)**2+(data.coord_6-inconnu.coord_6)**2)**0.5

#Méthode qui retourne l'index de la liste où se trouve la plus grande valeur.
#On a besoin de cette fonction à la fin de la méthode apprentissage où, après 
#avoir compté les occurences de chaque type de fleur dans les k sélectionnées,
#on veut savoir quel type a le plus d'occurences. Mais comme on a deux listes
#différentes, une liste qui répertorie les types et une autre les occurences,
#on doit retourner l'index du max de la liste d'occurence pour la liste des types.
def Max(liste):
    index=0
    Max=liste[0]
    for i in range (len(liste)):
        if(liste[i]>Max):
            Max=liste[i]
            index=i
    return index

#Cette fonction permet de sortir deux nouveaux dataset a partir d'un dataset pris en parametre
#Elle permet de tester notre k avec les deux fichiers data et preTest en les divisant en 2 dataset chacun
def melanger_dataset(data):
    random.shuffle(data)
    taille_dataset_test=int(0.8*len(data))
    data_set_connu=[]
    data_set_inconnu=[]
    for i in range(taille_dataset_test):
        data_set_connu.append(data[i])
    for i in range(taille_dataset_test, len(data)):
        data_set_inconnu.append(data[i])
    return data_set_connu, data_set_inconnu
        
        
def Trouver_Classe(data,inconnu,k):
    distances_classees=[]
    for i in range (len(data)):
        distance_label=[]
        distance=Distance_Euclidienne(data[i], inconnu)
        distance_label.append(distance)
        distance_label.append(data[i].classe)   
        n=len(distances_classees)
        if(n==0):
            distances_classees.append(distance_label)
            n+=1
        
        for i in range (n):
            if (distance < distances_classees[i][0]):
                distances_classees.insert(i,distance_label)
                break
            elif(i==n-1):
                distances_classees.append(distance_label)
    compteur=[0 for i in range(dim)]   
    for j in range (k):
        for index in range(dim):
            if(distances_classees[j][1]==allLabels[index]):
                #Au lieu d'incrémenter avec 1 à chaque fois que l'on trouve la même classe
                #on nuance/pondère cette valeur en ajoutant un poids en fonction de la position de 
                #l'élément dans la liste des distances classées.
                #C'est à dire que le premier élément de la liste aura un poids 
                #plus important et incrémentera le compteur correspondant 
                #à sa classe de manière significative
                compteur[index]+=k-j   
    #Maintenant, on cherche le type ayant été compté le plus de fois
    label=allLabels[Max(compteur)]
    return label

#ici on va simuler qu'on ne connait pas les classes de tout le fichier preTest.csv 
#on va chercher ces classes a partir du fichier data.csv pour ensuite les comparer aux vraies 
#classes et obtenir un pourcentage de précision

#On repete l'operation pour k allant de 3 a 12 afin de determiner le meilleur k
def Choisir_k():
    t0=time.time()
    print("\nOn cherche notre meilleur k:\n")
    dataset_a_verifier=Extraire_Data("preTest.csv");
    dataset_connu=Extraire_Data("data.csv");    
    maxi=0
    meilleur_k=0
    for k in range (3,19):
        labels=[]
        count=0
        for i in range (len(dataset_a_verifier)):
            labels.append(Trouver_Classe(dataset_connu, dataset_a_verifier[i],k))
            if(labels[i]==dataset_a_verifier[i].classe):
                count+=1
        precision=count/len(dataset_a_verifier)*100
        round(precision,2)
        print(round(precision,2),"% de précision avec k=",k,".\n")
        if(precision>maxi):
            meilleur_k=k
            maxi=precision
    t1=time.time()
    duree=t1-t0
    minutes=int(duree//60)
    secondes=round(duree%60)
    print("Le k le plus précis est", meilleur_k)
    print("\n(temps d'exécution pour trouver le meilleur k:",minutes,"min",secondes,"s)\n")
    return meilleur_k    

def test_k(k):
    t0=time.time()
    #On va prendre 20% de notre dataset data.csv et simuler qu'on cherche la classe de ces 20%
    #à l'aide des 80% que l'on connait. On teste cela avec notre meilleur k trouvé au dessus.
    
    print("\nOn teste notre meilleur k pour vérifier qu'il est cohérent:\n")
    dataset=Extraire_Data("data.csv");    
    dataset_connu, dataset_a_verifier= melanger_dataset(dataset)
    labels=[]
    count=0
    for i in range (len(dataset_a_verifier)):
        labels.append(Trouver_Classe(dataset_connu, dataset_a_verifier[i],k))
        if(labels[i]==dataset_a_verifier[i].classe):
            count+=1
    precision=count/len(dataset_a_verifier)*100
    round(precision,2)
    print(round(precision,2),"% de précision avec k=",k,"avec le dataset data.csv\n")
    
    #Ici on prend 20% de notre dataset preTest.csv et on simule qu'on cherche la classe de ces 20%
    #à l'aide des 80% que l'on connait. On teste cela avec notre meilleur k trouvé au dessus.
    dataset=Extraire_Data("preTest.csv");    
    dataset_connu, dataset_a_verifier= melanger_dataset(dataset)
    labels=[]
    count=0
    for i in range (len(dataset_a_verifier)):
        labels.append(Trouver_Classe(dataset_connu, dataset_a_verifier[i],k))
        if(labels[i]==dataset_a_verifier[i].classe):
            count+=1
    precision=count/len(dataset_a_verifier)*100
    round(precision,2)
    print(round(precision,2),"% de précision avec k=",k,"avec le dataset preTest.csv\n")
    t1=time.time()
    duree=t1-t0
    minutes=int(duree//60)
    secondes=round(duree%60)
    print("(temps d'exécution pour vérifier notre meilleur k avec les deux dataset:",minutes,"min",secondes,"s)\n")

def Estim_label(data_connu, data_inconnu, k):
    print("\nOn détermine les classes de notre dataset inconnu:\n")
    t0=time.time()
    dataset_inconnu=Extraire_Data_inconnu(data_inconnu)
    dataset_connu=Extraire_Data(data_connu)   
    nbrLignes=len(dataset_inconnu)
    labels=[]
    for i in range (nbrLignes):
        labels.append(Trouver_Classe(dataset_connu, dataset_inconnu[i],k))
    t1=time.time()
    duree=t1-t0
    minutes=int(duree//60)
    secondes=round(duree%60)
    print("(temps d'exécution pour déterminer les classes du dataset inconnu" ,minutes,"min",secondes,"s)\n")
    #permet de compter le nombre d'occurences total de chaque classe pour comparer mes résultats et verifier leur cohérence
    '''
    print("classA:", labels.count("classA"), "classB:", labels.count("classB"),
          "classC:", labels.count("classC"), "classD:", labels.count("classD"),
          "classE:", labels.count("classE"))
    '''
    nameFile="Labels_VANDERSTIGEL.txt"
    Enregistrer_Labels(nameFile,labels)
    Check_txt(nameFile, nbrLignes)

t=time.time()
k = Choisir_k()
test_k(k)
Estim_label("preTest.csv", "finalTest.csv", k)
t1=time.time()
duree=t1-t
minutes=int(duree//60)
secondes=round(duree%60)
print("(temps d'exécution total:" ,minutes,"min",secondes,"s)\n")
    