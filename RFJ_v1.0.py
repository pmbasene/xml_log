# coding: utf8
import os
import csv
from pprint import pprint

"""
General purpose
===============
Ce script contient deux programmes:
- Le premier(Purpose 1) a ete implemente dans le but de supprimer les doublons (replication de lignes) de la table job-file-stage (JFS) deja cree que Christpher m'a signale (en attendant que le 
NB: Integrer ce scrpit dans celui du script_job_file_stage_Plus.py afin de d'optimiser le workflow. Ce processus a\' deux etapes n'est plus une solution perenne.

- Le second(Purpose 2), permet d'etablir la relation en (RFJ) d'ou le nom du script. L'idee c'est que, pour chaque file donn\'e, lister les jobs qui l'utlisent soit en input, soit en output.

NB: ces deux scripts executent en entree le fichier-output nomm\'e 'script_job_file_stage_Plus.py' . 
Pour executer le script  du purpose 1, il faut dabord le decommente et en commenter parallelelement celui du Purpose2, et vise-versa


Next Purpose 
-----------
Creer une fonction pour chaque script ou si besoin une classe.

"""
# ########################################
# """
# Purpose 1:
# --------
# Suppressions des doublons de table 'cf variable path'. 

# Note pour moi :
# --- 
# voir pourquoi ce fichier ci dessous, a 'CORPSPAR_NOM_FIC_CATEL' apres l'extension:
# /export/home/exp/applications/doc/onide/datastage/source/TMP_FF_PENEF_EXTRANA_ONIDE_20190702150043.csvCORPSPAR_NOM_FIC_CATEL
# """
# class SupprimerDoublonsLignesCSV():
#     """Cette classe comporte deux principales fonctions et une fonction intermediaire. 
#     Les fonctions principales sont essentiellement compos\'ee d'une phase de lecture avec suppressions de doublons, il s'agit ici de la fonction <removeCsvLines()> 
#     et d'une phase d'ecriture <writeNewCSV()> qui ...
#     La fonction <removeCsvLines()> est execut\'e en premier. Elle prend en entree un fichier INPUT avec eventuellement des doublons (job-file-stage (JFS), en l'occurence) et retourne une liste de lignes sans doubons.
#     Elle genere en retour une liste de lignes sans doublons. Cette liste sera utlis\'e par la fonction writeNewCSV().

#     La fonction writeNewCSV()  un fichier qui est stock\'e dans vers le chemin precis\'e au niveau des proprietes
#     (fonction init)
#     """

#     def __init__(self):
#         self.rep = '/Users/ganasene/Downloads/projet_xml_insyco/code/resulats_projet_executable'
#         self.pathInput =os.path.join(self.rep,'jobName_fileName_truefileName_stageName_idenfiantIO_TypeIO.csv')
#         self.pathOuput =os.path.join(self.rep,'jobName_fileName_truefileName_stageName_idenfiantIO_TypeIO_clean.csv')

#     def supprimerDoublons(self, doublonsList):
#         ### supprimer doublons(list comprehension methods) 
#             # list2=[]
#             # list2= [line2 for line2 in list1 if line2 not in list2]
#         cleanList = []
#         for i in doublonsList:
#             if i not in cleanList:
#                 cleanList.append(i)
#         return cleanList
    
#     def removeCsvLines(self):

#         with open(self.pathInput, 'r') as file1:
#             reader = csv.reader(file1)
#             # next(reader)
#             list1=[line for line in reader]        
#             list1_clean = self.supprimerDoublons(list1)

#             # list2 = []
#             # for i in list1:
#             #     if i not in list2:
#             #         list2.append(i)
#         # return list2
#         nb_supprime = len(list1)- len(list1_clean)
#         print('Le nombre de lignes de depart est de {}'.format(len(list1)))
#         print('Le nombre de lignes apres suppression  est de {}\n Soit {} lignes supprimees '.format( len(list1_clean) , nb_supprime ))
        
#         return list1_clean

#     ## Ecriture

#     def writeNewCSV(self, list1_clean):

#         with open(self.pathOuput, 'w') as file2:
#             csv_writer = csv.writer(file2)
#             for line2 in list1_clean:
#                 csv_writer.writerow(line2)

 
# ########## Test P1    #####
# sD = SupprimerDoublonsLignesCSV.
# # print(len(list1))
# # print(len(list1_clean))

###########################################################################

"""
Purpose 2
--------
YANN REQUIREMENT :
---------------
 << j'aimerai que en priorité tu puisses nous déterminer 
les relations entre les jobs en se basant sur le nom du fichier.>>

En tete tableur ['Projet','job','file','truefile','stage','idIO','typeIO']
"""


class Rfj:

    def __init__(self):

        self.rep ='/Users/ganasene/Desktop/insyco/projet_xml_insyco/code/resulats_projet_executable'
        self.pathOffileOuput = os.path.join(rep,'RFJ_basedOnTrueFile.csv')
        self.pathOffileInput = os.path.join(rep, 'jobName_fileName_truefileName_stageName_idenfiantIO_TypeIO2.csv')

    def __str__(self):
        return self.pathOffileOuput

    def buildFilePath(self, filepath):
        """cette fonction permet separer un filename du path absolu pour le cas des 'file'"""
        extensions = ['.ds', '.txt', '.csv',' ']
        extensions2 = ['.csv\\(2)0', '.csv\(2)0', '.txt\\(2)0', '.txt\(2)0']
        fileSplitted = filepath.split('#')
        # print(fileSplitted)
        ext = fileSplitted[-1]
        if len(fileSplitted) > 3:
            lastPar = fileSplitted[-2]
            if ext in extensions:
                fic = lastPar+ext
                # print(fic)
            elif ext in extensions2:
                extf = ext.rstrip('.txt\\(2)0')
                fic = lastPar+extf
                # print(fic)
            else:
                fic = lastPar
        else:

            fic = ext.split('/')[-1]
            if r'\('in fic:
                fic = fic.rstrip('\(2)0')
                # print(fic)
            else:
                fic= ext

        return fic

    def splitPath(self, path):
        return os.path.split(path)
    
    def supprimerDoublons(self, doublonsList):
            ### supprimer doublons    (list comprehension methode)
            # list2=[]
            # list2= [line2 for line2 in list1 if line2 not in list2]
        cleanList = []
        for i in doublonsList:
            if i not in cleanList:
                cleanList.append(i)
        return cleanList
            
    def metadataValue(self, pathOffileInput, colCible='file'):
        """cette fonction permet d'extraire, nettoyer et collecter les items(file ou truefile) de la  colonne <colCible>
        Elle prend en entree le fichier input en l'occurence ici la table (JFS) et retourne une liste 
        d'items de la colonne <colCible> 
        NB: <colCible> est la colonne Centrale """
        with open(self.pathOffileInput, 'r') as file1:
            reader = csv.DictReader(file1, delimiter=';')

            # Note : print(reader)
            # Note :next(reader)   # IS FOR reader methods
            # Note :  on peut pas utiliser le curseur deux fois dans un meme context manager

            if colCible == 'truefile':
                colItems = [f[colCible] for f in reader] 

                # ### trie et supprimer des valeurs NaN
                colItems.sort()
                colItems = [l for l in colItems if l != ' ']

                # ### suppression des doublons PATH ABSOLU(path + filename) afin de ne pas avoir une replication des resultats
                colItemsFilter = list(set(colItems))
                colItemsFilter_list = [os.path.split(tf)[1] for tf in colItemsFilter]
                colItemsFilter_list = self.supprimerDoublons(colItemsFilter_list) # Supprimer les doublons filename
                # print(colItemsFilter_list)

            ###   Ajout de la colonne type IO                        # En cours d'implementation  
            # with open(pathOffileInput, 'r') as file2:
            #     reader = csv.DictReader(file2)
            #     typeIO = [f['typeIO'] for f in reader]
            #     # print(len(typeIO))
            #     # zip_tf_typeIO = zip(colItems, typeIO)

            elif colCible == 'file':
                colItems = [f[colCible] for f in reader]
                colItems.sort()
                # print(len(colItems))
                # colItems = [self.buildFilePath(l) for l in colItems]

                #split du path pour file 
                colItems2 = [] 
                for f in colItems:
                    colCible = self.buildFilePath(f)     # extraire juste le filename
                    colItems2.append(colCible)
                # print(len(colItems2))

                colItemsFilter_list = self.supprimerDoublons(colItems2)
                # print(len(colItemsFilter_list))

        return colItemsFilter_list

    def createRFJ(self, pathOffileInput, colCible='file', colAttachedToCible='job'):
        with open(pathOffileInput, 'r') as file1:
            reader = csv.DictReader(file1, delimiter= ';')
            lines = [line for line in reader]
    
            if colCible == 'truefile':
                colItemsFilter_list = self.metadataValue(pathOffileInput,colCible)   # appel de la fonction  <metadataVlue()
                rows = []
                for fileS in colItemsFilter_list:
                    for line in lines:
                        fileCibleB = self.splitPath(line[colCible])[1]
                        if fileS == fileCibleB:
                            row = [fileS, line[colAttachedToCible]]
                            rows.append(row)
                # print(len(rows))
            elif colCible == 'file':
                colItemsFilter_list = self.metadataValue(pathOffileInput,colCible)    # appel de la fonction  <metadataVlue()
                rows= []
                for fileS in colItemsFilter_list:
                    for line in lines:
                        # fileCibleB = self.splitPath(line[colCible])[1]
                        fileCibleB = line[colCible]
                        fileCibleB = self.buildFilePath(fileCibleB) # extraire just le filname
                        # print(fileCibleB)
                        if fileS == fileCibleB:
                            row = [fileS, line[colAttachedToCible]]
                            rows.append(row)
        # print(len(rows))
        rows_clean = self.supprimerDoublons(rows)   # suppression des doublons lignes

        return rows_clean

    def writeRFJ_ToCSV(self, rows):
        '''cette fonction permet d'ecriture les resulats sous format csv. 
        Elle prend en entree le dictionaire collect retourne par le fonction <createRFJ> et None'''
        path, name = os.path.split(self.pathOffileOuput)

        with open(self.pathOffileOuput, 'w') as csvfile:
            fieldnames = ['FILE','JOB' ]
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerow(fieldnames)
            writer.writerows(rows)
            print('Fichier enregistre dans {}\n--> sous le nom: {}!'.format(path, name))

    def displayResultat(self):
        #### En cours d'implimentation
        # # read
        # with open(pathOffileOuput, 'r') as csvfile:
        #     reader = csv.reader(csvfile)
        #     # print(reader)
        #     # print(dict(reader))
        #     for line in reader:
        #         print(line)
        #         # csvfile.write("%s,%s\n" % (key, value))
        pass


## affichage #####
## Pour memo les schema de la table JFS ['Projet','job','file','truefile','stage','idIO','typeIO']






###---------------- Programme Main---------------------------------------------------------------------------------------- ###


rep = "/Users/ganasene/Desktop/insyco/projet_xml_insyco/code/resulats_projet_executable"
pathOffileInput = os.path.join(rep, 'jobName_fileName_truefileName_stageName_idenfiantIO_TypeIO2.csv')
pathOffileOuput = os.path.join(rep, 'RFJ_fileCenterbis.csv')

###### initialisation de la classe 
a = Rfj()
####
colItemsFilter_list = a.metadataValue(pathOffileInput, 'truefile')
# print(colItemsFilter_list)

################## lecture
rows = a.createRFJ(pathOffileInput, 'truefile', 'job')
pprint(rows)
print(len(rows))

################# ecriture
a.writeRFJ_ToCSV(rows)


#### Pas important mais a ne pas supprimer
# # read
# with open(pathOffileOuput, 'r') as csvfile:
#     reader = csv.reader(csvfile)
#     # print(reader)
#     # print(dict(reader))
#     for line in reader:
#         print(line)

#         # csvfile.write("%s,%s\n" % (key, value))
