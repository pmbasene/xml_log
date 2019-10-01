#!/anaconda3/bin/python
# coding: utf-8

from lxml import etree
import xml.etree.ElementTree as ET
import os
import numpy as np
import pandas as pd
# from XML_HANDLE import *
# ou
from XML_HANDLE import Xml_logfile

""" 
Pour la documentation sur le package lxml consulter: 
- https://docs.python.org/3.4/library/xml.etree.elementtree.html#module-xml.etree.ElementTree

- Ce que je dois faire :
   - extraire les valeurs des cles(jobname, filename, directory) qui sont en format string ou variable depuis les fichiers XML.
   - recuperer leurs valeurs exactes en utilisant les jobnames des fichiers xml pour trouver leurs fichiers excecutables corespndantes.

- Demarche:
    1. Extraire tous les jobs d'un ou les fichier(s) xml du repertoire logFullDS  /ok
        a. le resultat de cette operation va retourner une listes de tous les jobs trouve dans un fichier XML donnee.
            note : l'objectif c'est de le faire avec tous les fichiers xml
    2. Aller chercher dans les jobs correspondants dans les fichiers executables (les logs).
        a. lire un par un tous les fichiers executables (log) qui sont le dossier logfullDS (faire une booucle for dans lequel with open sera appele)
        b. ensuite toujours dans cette meme boucle for, parcourir la liste collectionJobFromXML et pour chaque element i (qui est en fait le nom du job recuperer dans le fichier xml) de cette liste tester si il est bien presence un des fichier log.
            Si oui afficher le filename de ce fichier

"""
# DOC-FTSACprod.xml

class ParseElementXML():
    """cette classe prend en entree le nom du fichier XML a parser et pretourne une colletction (format liste)nommé collectionJobFromXML des jobs dun fichier XML
    Note: le fichier XML doit etre dans le meme dossier que le fichier py """

    def document(self, fileXML="SUPprd.xml"):
        basePath = os.path.dirname(__file__)
        fullPath = os.path.join(basePath, fileXML)
        # ---------------------------------------------------------------------,
        # try:
        #     basePath = os.path.dirname(__file__)
        #     fullPath = os.path.join(basePath, fileXML)
        #     print(fullPath)
        #     return fullPath
        # except OSError:
        #     return "verifier bien le path du fichier. Il doit etre dans le dossier"
        # print(fullPath)
        return fullPath

    def getRoot(self, fullPath):
        tree = etree.parse(fullPath)
        root = tree.getroot()
        print(root.tag, root.attrib)
        print(f"Infos - nombre de  child pour {root.tag}:", len(root))
        print("_________-------_____----Header------___----___----___----___ ")
        return root

    def removeDuplicates(self, listDoublons):  # not use
        '''cette methode permet de supprimer les doublons dans une liste. 
            Elle prend en entree une liste d'elements et retourne ensuite la meme liste dans laquelle tous elements dupliques sont supprimes'''
        liste = []
        for i in listDoublons:
            if i not in liste:
                liste.append(i)
        return liste

        
class ParseLog():

    def changeDir(self):
        path_to_logfullDS = '/Users/ganasene/Downloads/folder/logsfullDS'
        r = os.chdir(path_to_logfullDS)
        return r

    def blockEventID(self, string):
        '''ici on va prendre le separator_word Event iD
        sep_word=Event 
        !!! Dans les listes qui seront generees il en y aura certaines qui sont vide. 
        Donc il faut en prendre compte lors de suppression des occurences de la liste bloc_jb'''
        bloc_jb = string.split('Event ')     # Note : prendre juste Event plus espace pour que ca marche
        # del bloc_jb[2]                          # permet d'enlever la deuxieme occurence qui comporte que les parametre de conf du datastage
       
        del bloc_jb[0]       # enleve la permiere occ qui est vide
        bloc_jb = bloc_jb[:]
        
        return bloc_jb



# ===================MAIN1===================================================

p = ParseElementXML()

collectionJobFromXML = []

fullPath = p.document()

root = p.getRoot(fullPath)

# a decommenter.....
for job in root:
    # print(job.tag, job.attrib)
    # print(f"infos - nombre de child pour {job.tag}:", len(job))
    # print("\t\t->"+str(job.attrib.get('Identifier')))
    collectionJobFromXML.append(job.attrib.get('Identifier'))
    
print(len(collectionJobFromXML))
collectionJobFromXML = list(set(collectionJobFromXML))
collectionJobFromXML = p.removeDuplicates(collectionJobFromXML)
collectionJobFromXML.remove(None)
print(len(collectionJobFromXML))
# print(collectionJobFromXML)

######## ======================== ======================

# some resultat:
# # Jx_FEUILLET_01_CHG_CPTRENDU    job a trouver

# /Users/ganasene/Downloads/folder/logsfullDS/SUPprdJx_FEUILLET_01_CHG_CPTRENDUlog.txt
q = ParseLog()

path_to_logfullDS = q.changeDir()           # changement de repertoire 
tuple_job_logfile =[]
compt =0
for jobFromXML in collectionJobFromXML:
    compt+=1
    # print(f"job {compt}/{len(collectionJobFromXML)} ({jobFromXML})")

    for logfile in os.listdir(path_to_logfullDS):
        with open(logfile, encoding='utf8') as f:
            f = f.read()
   
            if jobFromXML in f:
                print(f"job {compt}/{len(collectionJobFromXML)} {jobFromXML} -->{logfile}")
                job_logfile = (jobFromXML, logfile)
                tuple_job_logfile.append(job_logfile)
                # bloc = q.blockEventID(f)
                # blockTextPar =  bloc[0]
                # print(blockTextPar)        
            else:
                # print(f"Jx_FEUILLET_01_CHG_CPTRENDU is not in {logfile}")
                pass

### resultat
# print(tuple_job_logfile)

# ===================MAIN2===================================================
# ### traitement 2 

# # initiation des listes suivants en vue de creeer un dataframe
# jobName = []
# stagName = []
# stageType = []
# recordType = []
# fileName = []
# datasetValue =[]
# #initialisation du tuple file_job
# tuple_file_Job = []

# #compteur
# num_job = []  # nombre de job pour un fic XML donnee
# num_stage = []  # nombre de job pour un fic XML donnee

# # DOC-FTSACprod.xml
# # SUPprd.xml

# # basePath = os.path.dirname(__file__)
# # fullPath = os.path.join(basePath, "SUPprd.xml")
# # print(fullPath)

# b = Xml_logfile()
# fullPath = b.document()
# print(fullPath)

# # Instanciation du module etree
# ## methode parse
# tree = etree.parse(fullPath)
# root = tree.getroot()
# # print(root.tag, root.attrib)
# # print(f"Infos - nombre de  child pour {root.tag}:", len(root))
# # print(" ")



# for job in root:
#     # print(job.tag, job.attrib)
#     # print(f"infos - nombre de child pour  {job.tag}:", len(job))
#     jobN = job.attrib.get('Identifier')
#     num_job.append(jobN)
#     # print("\t\t1>"+str(job.attrib.get('Identifier')))
#     # print('')
#     for record in job:
#         attribute = record.attrib.get('Type')
#         if attribute == 'CustomStage':
#             # print("\t"+record.tag, record.attrib)
#             # print(f"\tinfos - nombre de child pour {record.tag}:", len(record))
#             # print("\t\t---->"+ attribute)

#             for PropertyOrcollection in record:
#                 attribute_Name = PropertyOrcollection.attrib.get('Name')
#                 if attribute_Name == 'Name':
#                     TextPropertyOrcollection = str(PropertyOrcollection.text)

#                     # print(f'{jobN} ->{TextPropertyOrcollection}')
#                     # print("\t\t\t2>"+TextPropertyOrcollection)
#                     jobName.append(jobN)
#                     stagName.append(TextPropertyOrcollection)

#                 elif attribute_Name == 'StageType':
#                     TextPropertyOrcollection = str(PropertyOrcollection.text)
#                     # print("\t\t\t3>"+TextPropertyOrcollection)
#                     # jobName.append(jobN)
#                     stageType.append(TextPropertyOrcollection)

#         elif attribute == 'CustomOutput':
#             # print("\t"+record.tag, record.attrib)
#             # print(f"\tinfos - nombre de child pour {record.tag}:", len(record))
#             # print("\t\t---->"+ attribute)
#             for PropertyOrcollection in record:
#                 if PropertyOrcollection.tag == 'Collection' and PropertyOrcollection.attrib.get("Name") == 'Properties':
#                     # print("\t\t\t"+PropertyOrcollection.tag, PropertyOrcollection.attrib)
#                     attribute_Name = PropertyOrcollection.attrib.get('Name')

#                     for subrecord in PropertyOrcollection:

#                         for prop in subrecord:

#                             if prop.attrib.get('Name') == 'Name':
#                                 Textprop = str(prop.text)
#                                 if Textprop == r"file\(20)":
#                                     pass
#                                     # print("\t\t\t\t>"+Textprop)                             
#                                 # elif Textprop == "dataset":
#                                 #     print("\t\t\t\t>"+Textprop)
#                                 #     # pass
#                                 else:
#                                     pass
#                             else:
#                                 Textprop = str(prop.text)
#                                 if r')file' in Textprop:
#                                     # print(f'{jobN} ->{Textprop}')
#                                     tup = (jobN, Textprop)
#                                     tuple_file_Job.append(tup)
#                                     # print("\t\t\t\t4>"+Textprop)
#                                     fileName.append(Textprop)
#                                     recordType.append('CustomOutput')                            # ajout de lattribut Custominput dams la colonne recordType


#                                 else:
#                                     # fileName.append("NaN")
#                                     pass

#         elif attribute == 'CustomInput':
#             # print("\t"+record.tag, record.attrib)
#             # print(f"\tinfos - nombre de child pour {record.tag}:", len(record))
#             # print("\t\t---->"+ attribute)
#             # recordType.append(attribute)

#             for PropertyOrcollection in record:
#                 if PropertyOrcollection.tag == 'Collection' and PropertyOrcollection.attrib.get("Name") == 'Properties':
#                     # print("\t\t\t"+PropertyOrcollection.tag, PropertyOrcollection.attrib)
#                     attribute_Name = PropertyOrcollection.attrib.get('Name')

#                     for subrecord in PropertyOrcollection:

#                         for prop in subrecord:

#                             if prop.attrib.get('Name') == 'Name':
#                                 Textprop = str(prop.text)
#                                 if Textprop == "dataset":
#                                     pass
#                                     # print("\t\t\t\t>"+Textprop)
#                                 else:
#                                     pass
#                             else:     # ie name = value ou autres 
#                                 Textprop = str(prop.text)
#                                 if r".ds" in Textprop:
#                                     # print(f'{jobN} ->{Textprop}')
#                                     # print("\t\t\t\t4>"+Textprop)
#                                     datasetValue.append(Textprop)
#                                     recordType.append('CustomOutput')                           # ajout de lattribut Custominput dams la colonne recordType
                                    

#                                 else:
#                                     # fileName.append("NaN")
#                                     pass
#                 else:
#                     pass


# # pas commode de gerer les length, l'astuce trouve est de manipuler les colonnes sous un format dataframe

# print("|----Informations sur les elements extraits de ce fichier XML---|")
# print("1./Nombre de jobs dans ce fichier:", len(num_job))
# print("2.Nombre de stage dans ce fichier:", len(stagName))
# print("3./Nombre de stageType dans ce fichier:", len(stageType))
# print("4./Nombre de fileName de ce fichier:", len(fileName))
# print("4./Nombre de recordType de ce fichier:", len(recordType))
# print("4./Nombre de datasetValue de ce fichier:", len(datasetValue))
# print('\n')

# print("|---- check colonnes pour creation tableau ---|")

# print(len(jobName))
# # print(jobName)

# print(len(stagName))
# # print(stagName)

# print(len(stageType))
# # print(stageType)

# print(len(fileName))
# # print(fileName)

# print(len(recordType))
# # print(recordType)

# print(len(datasetValue))
# # print(datasetValue)

# # print('\n')
# # print(len(tuple_file_Job))
# # print(tuple_file_Job)


# ###=====================main3===================================
# #  ++++++++++++++++++++++Dataframe++++++++++++++++++++++++++++
# file = []
# data = {
#     "jobName": jobName,
#     "stagName": stagName,
#     "stageType": stageType,
#     "recordType": np.nan,
#     'datasetValue': np.nan,
#     'fileName': np.nan,

# }

# df = pd.DataFrame(data)
# print(df)

# # gestion cle-valeur
# idx = []
# tuple_idx_job = []
# tuple_idx_file = []
# tuple_idx_logfile = []
# for key, job in enumerate(df.jobName):
#     for i in range(len(tuple_file_Job)):
#         if job == tuple_file_Job[i][0]:
#             idx_job = (key, job)
#             idx_file = (key, tuple_file_Job[i][1])
#             # print(idx_job)
#             tuple_idx_job.append(idx_job)
#             tuple_idx_file.append(idx_file)
#             idx.append(key)
#             file.append(tuple_file_Job[i][1])
    
#         # else:
#         #     pass
#         #     # file.append('NaN')

#     # for j in range(len(tuple_job_logfile)):
#     #     if job == tuple_job_logfile[j][0]:
#     #         idx_logfile = (key, logfile)
#     #         tuple_idx_logfile.append(idx_logfile)


# # print(tuple_idx_logfile)


# # affection des data de files-excates à la 4 eme colonne
# for j in range(len(tuple_idx_job)):
#     # i == index , j== job, et fl = file
#     ix = tuple_idx_job[j][0]             # index des valeurs file
#     jb = tuple_idx_job[j][1]
#     fl = tuple_idx_file[j][1]  # file extrait du tuple
#     # print(ix)            #
#     # print(jb)
#     # print(fl)
#     df.loc[tuple_idx_job[j][0], 'fileName'] = fl



# print(df)
# # df.to_csv('/Users/ganasene/Desktop/outputxml.csv')



