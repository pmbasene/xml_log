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
from clean_file import CleanFolder

""" 
- inclure le scrip clean file.py en en-tete afin de nottoyer le dossier 
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
        print(fullPath)
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
    
    # def splitValues(self, string):
    #     # os.string
    #     pass

    def recupererCleOuValeurInString(self, string, sep=" "):
        '''cette fonction prend en entree une chaine de caractere <str>  
        et un separateur(= ou , ou ; ou : etc) et retourne la cle et la valeur de la chaine splitee'''
        key, val = string.split(sep)
        Key = key.strip()
        Val = val.strip()
        return Key, Val

# fonction plus elaborer que celle ci dessus
    def recuperer_PAR_dir(self, string):
        """ cette fonction prend en entree une la valeur du file du xML (format string) et retourne une liste d'elements filtree(format list).
        Le role de cette fonction est d'abord de spliter une chaine de caractere avec comme separator # pris en entree, ensuite filter tous les items non desirables 
        tel items vide , underscore , etc, et retourne que les variable repertoires du logfile  """
        PAR_list = []                            # RESULTAT A RECUPERER COMME RETURN DE LA FONCTION
        # LIST DES CARACTERES EXCLUS COMME PREMIER ITEM DE LA LISTE
        caract_exclu = ['', '_']

        result = string.split("\\")
        for res in result:
            if 'PAR' in res:
                res = res.split("#")
                # print(res)
                del res[0]
                for r in res:
                    if r not in caract_exclu and 'DS_' not in r:
                        PAR_list.append(r)
                    if 'DS_' in r:
                        r, r_ext = os.path.splitext(r)
                        PAR_list.append(r)
                        PAR_list.append(r_ext)
                # print(res)
                # print(PAR_list)
        return PAR_list


    # def buildFullPath(self, PAR_list, realFilePath):
    #     # global realFilePathFull
    #     extensions = ['.ds', '.ext', 'csv']
    #     extension = PAR_list[-1]
    #     if extension in extensions:
    #         # Full = realFilePath+extension
    #         return realFilePath+extension          
    #     else:
    #         return realFilePath+extension

    def buildFullPath(self, PAR_list, realFilePath):
        # global realFilePathFull
        extensions = ['.ds', '.ext', 'csv']
        extension = PAR_list[-1]
        DSfile = PAR_list[-2]
        if extension in extensions:
            if 'PAR' not in DSfile:
                # realFilePathFull = realFilePath+DSfile+extension
                return realFilePath+DSfile+extension
            else:
                # realFilePathFull = realFilePath+extension
                return realFilePath+extension
        elif extension not in extensions:
            return realFilePath+extension

    # def funcname(self, **args):
    #     if len(args) == 1:
    #         realFilePath = os.path.join(args[0])
    #         return realFilePath
    #     elif len(args) == 2:
    #         realFilePath = os.path.join(args[0], args[1])
    #         print(realFilePath)
    #         return realFilePath

    #     elif len(args) == 3:
    #         realFilePath = os.path.join(args[0], args[1], args[2])
    #         print(realFilePath)
    #         return realFilePath

    #     elif len(args) == 4:
    #         realFilePath = os.path.join(args[0], args[1], args[2], args[3])
    #         print(realFilePath)
    #         return realFilePath

    #     elif len(args) == 5:
    #         realFilePath = os.path.join(args[0], args[1], args[2], args[3], args[4])
    #         print(realFilePath)
    #         return realFilePath




class ParseLog():

    def changeDir(self):
        path_to_logfullDS = '/Users/ganasene/Downloads/folder/logsfullDS'
        r = os.chdir(path_to_logfullDS)
        return r

    # def blockEventID(self,string):
    #     '''ici on va prendre le separator_word Event iD
    #     sep_word=Event 
    #     !!! Dans les listes qui seront generees il en y aura certaines qui sont vide. 
    #     Donc il faut en prendre compte lors de suppression des occurences de la liste bloc_jb'''
    #     bloc_jb = string.split(
    #         'Event ')     # Note : prendre juste Event plus espace pour que ca marche
    #     # del bloc_jb[2]                          # permet d'enlever la deuxieme occurence qui comporte que les parametre de conf du datastage
    #     # enleve la permiere occ qui est vide
    #     del bloc_jb[0]
    #     bloc_jb = bloc_jb[:]
    #     return bloc_jb
    

    def blockEventID(self , string):
        ''' cette fonction prend en entree une string et retourne une liste.
        ici on va prendre comme separator_word le -Event iD-, donc sep_word=Event !!! 
            -Dans les listes qui seront generees il en y aura certaines qui seront vides. Donc il faut en prendre compte lors de suppression 
            des occurences inutiles(msgid -00126 par exples) de la liste bloc_jb.- '''
        blockPar2 = []
        blockPar3 = []
        bloc_jb = string.split(
            'Event ')     # Note : prendre juste Event plus espace pour que ca marche
        # del bloc_jb[2]                          # permet d'enlever la deuxieme occurence qui comporte que les parametre de conf du datastage
        # enleve la permiere occ qui est vide
        del bloc_jb[0]
        # ceci est la liste d'element ou bloc a suprrimer
        msgId_list = ['IIS-DSTAGE-RUN-I-0126',
                    'IIS-DSTAGE-RUN-I-0034', 'IIS-DSTAGE-RUN-I-0070']
        for i, l in enumerate(bloc_jb):       # i, la ligne  et l est la ligne
            if msgId_list[0] in l:
                # suppression de l'environnement varaible inutiles
                del bloc_jb[i]
                for l2 in bloc_jb:
                    if (msgId_list[1] in l2) or (msgId_list[2] in l2):
                        blockPar2.append(l2)
                for l3 in blockPar2:
                    # conversion de str en list car blockTextPar etait en format list
                    blockPar2_list = l3.split('\n')
                    for l4 in blockPar2_list:
                        if r'=' in l4:
                            blockPar3.append(l4)
                            blockPar3 = list(set(blockPar3))
        return blockPar3




# # ===================MAIN0 : nettoyage du dossier ===================================================
p = CleanFolder()
# print(p)
content = p.cleaning_files()
### affichage
print("------ traitement1: Resultat nettoyage du dossier {} !!!!------".format(p))
for i in content:
    print(i,sep='\n')
print('---<>_<>__ Dossier nettoye!!!!---<>_<>__', sep='\n')



# # ===================MAIN1===================================================

# Initiation des listes suivants en vue de creeer un dataframe en output
jobName = []
stageName = []
stageType = []
recordType = []
fileName = []
fileNameTrue =[]
datasetName =[]
datasetValueTrue =[]
logFile =[]

# global realFilePathFull

# Initialisation du tuple file_job: relier les logfile au jobname
tuple_file_Job = []

#compteur
num_job = []  # nombre de job pour un fic XML donnee
num_stage = []  # nombre de job pour un fic XML donnee

# basePath = os.path.dirname(__file__)
# fullPath = os.path.join(basePath, "SUPprd.xml")
# print(fullPath)

b = Xml_logfile()
fullPath = b.document()

# Instanciation du module etree
## methode parse
tree = etree.parse(fullPath)
root = tree.getroot()

# Initiation des listes de collection des jobs extraits dans les fichiers xml
collectionJobFromXML = []

p = ParseElementXML()
fullPath = p.document()
root = p.getRoot(fullPath)

# A decommenter.....
for job in root:
    collectionJobFromXML.append(job.attrib.get('Identifier'))
print("------ traitement2: collection des jobs dans xml {} !!!!------".format(fullPath))
# print(len(collectionJobFromXML))
collectionJobFromXML = list(set(collectionJobFromXML))
collectionJobFromXML = p.removeDuplicates(collectionJobFromXML)
collectionJobFromXML.remove(None)
print(len(collectionJobFromXML), sep='\n')
# print(collectionJobFromXML)

######## ======================== ======================

# some resultat:
# # Jx_FEUILLET_01_CHG_CPTRENDU    job a trouver

# /Users/ganasene/Downloads/folder/logsfullDS/SUPprdJx_FEUILLET_01_CHG_CPTRENDUlog.txt
q = ParseLog()
path_to_logfullDS = q.changeDir()           # changement de repertoire
tuple_job_logfile = []
compt = 0
for jobFromXML in collectionJobFromXML:
    # jobName.append(jobFromXML)  # col 1


    compt += 1
    # print(f"job {compt}/{len(collectionJobFromXML)} ({jobFromXML})")

    for logfile in os.listdir(path_to_logfullDS):
        with open(logfile, encoding='utf8') as f:
            f = f.read()

            if jobFromXML in f:
                # num_job.append(jobFromXML)    # colonne 1 resultat jobs
                # jobName.append(jobFromXML)  # col 1

                print(f"job {compt}/{len(collectionJobFromXML)} {jobFromXML} -->{logfile}")
                job_logfile = (jobFromXML, logfile)
                tuple_job_logfile.append(job_logfile)

                
                # num_job.append(jobFromXML)    # colonne 1 resultat jobs

                bloc = q.blockEventID(f)
                blockTextPar = bloc      # je change de nom seulement (format -  list)
                
                jobNameRecord = []
                logFileRecord = []
                stageNameRecord = []
                stageTypeRecord = []
                recordTypeRecord = []
                fileNameRecord = []
                fileNameTrueRecord = []
                datasetNameRecord = []
                datasetValueTrueRecord = []


                ### traitement du fichier xml
                for job in root:
                    jobN = job.attrib.get('Identifier')

                    # num_job.append(jobN)    # colonne 1 resultat jobs
                    # jobName.append(jobN)     #### col 1

                    for record in job:
                        attribute = record.attrib.get('Type')
                        if attribute == 'CustomStage':
                            for PropertyOrcollection in record:
                                attribute_Name = PropertyOrcollection.attrib.get('Name')
                                if attribute_Name == 'Name':
                                    TextPropertyOrcollection = str(PropertyOrcollection.text)
                                    # print(f"\t\t\t3.{jobN}, {logfile}, stageName: {TextPropertyOrcollection}, 'recordType':{attribute}", )
                                    jobName.append(jobN)     # col 1
                                    logFile.append(logfile)     # col 1
                                    stageName.append(TextPropertyOrcollection)     # col 1
                                    stageType.append("NaN")     # col 1
                                    recordType.append(attribute)    # col 4


                                elif attribute_Name == 'StageType':
                                    TextPropertyOrcollection = str(PropertyOrcollection.text)

                                    # print(f"\t\t\t4.{jobN}, {logfile}, stageType: {TextPropertyOrcollection}, 'recordType':{attribute}", )
                                    jobName.append(jobN)     # col 1
                                    logFile.append(logfile)     # col 1
                                    stageType.append(TextPropertyOrcollection)     # col 1
                                    stageName.append('NaN')     # col 1
                                    recordType.append(attribute)    # col 4



#                         elif attribute == 'CustomOutput':

#                             for PropertyOrcollection in record:
#                                 if PropertyOrcollection.tag == 'Collection' and PropertyOrcollection.attrib.get("Name") == 'Properties':
#                                     attribute_Name = PropertyOrcollection.attrib.get('Name')

#                                     for subrecord in PropertyOrcollection:

#                                         for prop in subrecord:

#                                             if prop.attrib.get('Name') == 'Name':
#                                                 Textprop = str(prop.text)
#                                                 # fileKey = Textprop
#                                                 if Textprop == r"file\(20)":
#                                                     pass
#                                                     # print("\t\t\t\t>"+Textprop)
#                                                 elif Textprop == "dataset":
#                                                     # print("\t\t\t\t>"+Textprop)
#                                                     pass
#                                                 else:
#                                                     pass
#                                             else:            
#                                                 Textprop = str(prop.text)
#                                                 fileValue = Textprop
#                                                 if r')file' in fileValue and jobN == jobFromXML:
                                                    
#                                                     # recordType.append('CustumOupt')    # col 4

#                                                     print(f'\t\t{jobN} --> {logfile} --> {fileValue}')

#                                                     PAR_list = p.recuperer_PAR_dir(fileValue )   # recuperation des parametres directory

#                                                     # print("PAR",len(PAR_list),PAR_list)

#                                                     blockTextPar_list = blockTextPar
#                                                     filePath = []                   # les filepath fonctionnent correctement si le bloc est au debut du logfile. donc il me faut trouver une solution pour resoudre le cas ou le boc est a une ligne x du logfile. pour cela se referer a la variable PAR
#                                                     for par in PAR_list:                 # la valeur PAR_list = 0  signifie que le bloc n'est pas en debut du logfile
#                                                         for line in blockTextPar_list:
#                                                     #         line = line.strip()  # pour enlever tous les espaces a gauche et a droite
#                                                             if r'=' in line:       # ceci est du a une levee dexcpection  ie unpacking items
#                                                                 kline, vline = p.recupererCleOuValeurInString(line, sep="=")
#                                                                 if  par == kline:
#                                                                     filePath.append(vline)

#                                                     # print(jobN+"-->"+logfile+"-->filePath",len(filePath), filePath)

#                                                     if len(filePath) == 1:
#                                                         realFilePath = os.path.join(filePath[0])
#                                                         realFilePath = p.buildFullPath(PAR_list,realFilePath)
#                                                         print(
#                                                             f"{jobN}-->{logfile}-->filePath:{len(filePath)}-->{fileValue} -->Path du file: {realFilePath} -->Custom Output \n")
#                                                         # print("Path du file: ",realFilePath)
#                                                         jobName.append(jobN)
#                                                         logFile.append(logfile)
#                                                         fileName.append(fileValue)
#                                                         datasetName.append('NaN')
#                                                         datasetValueTrue.append('NaN')

#                                                         fileNameTrue.append(realFilePath)
#                                                         recordType.append('Custom Output')

#                                                     elif len(filePath) == 2:
#                                                         realFilePath = os.path.join(filePath[0], filePath[1])
#                                                         realFilePath = p.buildFullPath(PAR_list,realFilePath)
#                                                         # print("Path du file: ",realFilePath)
#                                                         print(
#                                                             f"{jobN}-->{logfile}-->filePath:{len(filePath)}-->{fileValue} -->Path du file: {realFilePath}  -->Custom Output \n")

#                                                         jobName.append(jobN)
#                                                         logFile.append(logfile)
#                                                         fileName.append(fileValue)
#                                                         datasetName.append('NaN')
#                                                         datasetValueTrue.append('NaN')

#                                                         fileNameTrue.append(realFilePath)
#                                                         recordType.append('Custom Output')


#                                                     elif len(filePath) == 3:
#                                                         realFilePath = os.path.join(filePath[0], filePath[1], filePath[2])
#                                                         realFilePath = p.buildFullPath(PAR_list,realFilePath)
#                                                         # print("Path du file: ",realFilePath)
#                                                         print(
#                                                             f"{jobN}-->{logfile}-->filePath:{len(filePath)}-->{fileValue} -->Path du file: {realFilePath} -->Custom Output \n")
 
#                                                         jobName.append(jobN)
#                                                         logFile.append(logfile)
#                                                         fileName.append(fileValue)
#                                                         datasetName.append('NaN')
#                                                         datasetValueTrue.append('NaN')

#                                                         fileNameTrue.append(realFilePath)
#                                                         recordType.append('Custom Output')


#                                                     elif len(filePath) == 4:
#                                                         realFilePath = os.path.join(filePath[0], filePath[1], filePath[2], filePath[3])
#                                                         realFilePath = p.buildFullPath(PAR_list,realFilePath)
#                                                         # print("Path du file: ",realFilePath)
#                                                         print(
#                                                             f"{jobN}-->{logfile}-->filePath:{len(filePath)}-->{fileValue}--> Path du file:{realFilePath} -->Custom Output \n")

#                                                         jobName.append(jobN)
#                                                         logFile.append(logfile)
#                                                         fileName.append(fileValue)
#                                                         datasetName.append('NaN')
#                                                         datasetValueTrue.append('NaN')

#                                                         fileNameTrue.append(realFilePath)
#                                                         recordType.append('Custom Output')


#                                                     elif len(filePath) == 5:
#                                                         realFilePath = os.path.join(filePath[0], filePath[1], filePath[2], filePath[3], filePath[4])
#                                                         realFilePath = p.buildFullPath(PAR_list,realFilePath)
#                                                         # print("Path du file: ",realFilePath)
#                                                         print(
#                                                             f"{jobN}-->{logfile}-->filePath:{len(filePath)}-->{fileValue} --> Path du file:{realFilePath} -->Custom Output \n")
 
#                                                         jobName.append(jobN)
#                                                         logFile.append(logfile)
#                                                         fileName.append(fileValue)
#                                                         datasetName.append('NaN')
#                                                         datasetValueTrue.append('NaN')

#                                                         fileNameTrue.append(realFilePath)
#                                                         recordType.append('Custom Output')


#                                                 else:
#                                                     pass


#                                             #         # tup = (jobN, fileValue )
#                                             #         # tuple_file_Job.append(tup)
#                                             #         # # print("\t\t\t\t4>"+fileValue )


#                                                 datasetValue = Textprop
#                                                 if ('.ds' in datasetValue) and (jobN == jobFromXML):
#                                                     print(f'\t\t{jobN}->{logfile}->{datasetValue}')
#                                                     # print(blockTextPar)       # affiche le premier bloc du logfile
#                                                     PAR_dataset_list = p.recuperer_PAR_dir(datasetValue)   # recuperation des parametres directory
#                                                     print("PARdatasetlist", len(PAR_dataset_list), PAR_dataset_list)
#                                                     # in logfile...
#                                                     blockTextPar_list = blockTextPar      
#                                                     filePathDataset = []                   # les filepathDataset fonctionnent correctement si le bloc est au debut du logfile. donc il me faut trouver une solution pour resoudre le cas ou le boc est a une ligne x du logfile. pour cela se referer a la variable PAR
#                                                     for par in PAR_dataset_list:                 # la valeur PAR_list = 0  signifie que le bloc n'est pas en debut du logfile
#                                                         for line in blockTextPar_list:
#                                                     #         line = line.strip()  # pour enlever tous les espaces a gauche et a droite
#                                                             if r'=' in line:       # ceci est du a une levee dexcpection  ie unpacking items
#                                                                 kline, vline = p.recupererCleOuValeurInString(line, sep="=")
#                                                                 if  par == kline:
#                                                                     filePathDataset.append(vline)

#                                                     print("filePathDataset",len(filePathDataset))

#                                                     if len(filePathDataset) == 1:
#                                                         realFilePathDataset = os.path.join(filePathDataset[0])
#                                                         realFilePathDataset = p.buildFullPath(PAR_dataset_list,realFilePathDataset)

#                                                         # print("path du dataset: ",realFilePathDataset)
#                                                         print(
#                                                             f"{jobN}-->{logfile}-->filePathDataset:{len(filePathDataset)}-->{datasetValue} --> Path du dataset:{realFilePathDataset} -->Custom Output \n")


#                                                         jobName.append(jobN)
#                                                         logFile.append(logfile)
#                                                         datasetName.append(datasetValue)
#                                                         fileName.append('NaN')
#                                                         fileNameTrue.append('NaN')
#                                                         datasetValueTrue.append(realFilePathDataset)
#                                                         recordType.append('Custom Output')

#                                                     elif len(filePathDataset) == 2:
#                                                         realFilePathDataset = os.path.join(filePathDataset[0], filePathDataset[1])
#                                                         realFilePathDataset = p.buildFullPath(PAR_dataset_list,realFilePathDataset)

#                                                         # print("path du dataset: ",realFilePathDataset)
#                                                         print(
#                                                             f"{jobN}-->{logfile}-->filePathDataset:{len(filePathDataset)}-->{datasetValue} --> Path du dataset:{realFilePathDataset} -->Custom Output \n")


#                                                         jobName.append(jobN)
#                                                         logFile.append(logfile)
#                                                         datasetName.append(datasetValue)
#                                                         fileName.append('NaN')
#                                                         fileNameTrue.append('NaN')
#                                                         datasetValueTrue.append(realFilePathDataset)
#                                                         recordType.append('Custom Output')

#                                                     elif len(filePathDataset) == 3:
#                                                         realFilePathDataset = os.path.join(filePathDataset[0], filePathDataset[1], filePathDataset[2])
#                                                         realFilePathDataset = p.buildFullPath(PAR_dataset_list,realFilePathDataset)

#                                                         # print("path du dataset: ",realFilePathDataset)
#                                                         print(
#                                                             f"{jobN}-->{logfile}-->filePathDataset:{len(filePathDataset)}-->{datasetValue} --> Path du dataset:{realFilePathDataset} -->Custom Output \n")



#                                                         jobName.append(jobN)
#                                                         logFile.append(logfile)
#                                                         datasetName.append(datasetValue)
#                                                         fileName.append('NaN')
#                                                         fileNameTrue.append('NaN')
#                                                         datasetValueTrue.append(realFilePathDataset)
#                                                         recordType.append('Custom Output')

#                                                     elif len(filePathDataset) == 4:
#                                                         realFilePathDataset = os.path.join(filePathDataset[0], filePathDataset[1], filePathDataset[2], filePathDataset[3])
#                                                         realFilePathDataset = p.buildFullPath(PAR_dataset_list,realFilePathDataset)

#                                                         # print("path du dataset: ",realFilePathDataset)
#                                                         print(
#                                                             f"{jobN}-->{logfile}-->filePathDataset:{len(filePathDataset)}-->{datasetValue} --> Path du dataset:{realFilePathDataset} -->Custom Output \n")


#                                                         jobName.append(jobN)
#                                                         logFile.append(logfile)
#                                                         datasetName.append(datasetValue)
#                                                         fileName.append('NaN')
#                                                         fileNameTrue.append('NaN')
#                                                         datasetValueTrue.append(realFilePathDataset)
#                                                         recordType.append('Custom Output')

#                                                     elif len(filePathDataset) == 5:
#                                                         realFilePathDataset = os.path.join(filePathDataset[0], filePathDataset[1], filePathDataset[2], filePathDataset[3], filePathDataset[4])
#                                                         realFilePathDataset = p.buildFullPath(PAR_dataset_list,realFilePathDataset)

#                                                         # print("path du dataset: ",realFilePathDataset)
#                                                         print(
#                                                             f"{jobN}-->{logfile}-->filePathDataset:{len(filePathDataset)}-->{datasetValue} --> Path du dataset:{realFilePathDataset} -->Custom Output \n")


#                                                         jobName.append(jobN)
#                                                         logFile.append(logfile)
#                                                         datasetName.append(datasetValue)
#                                                         fileName.append('NaN')
#                                                         fileNameTrue.append('NaN')
#                                                         datasetValueTrue.append(realFilePathDataset)
#                                                         recordType.append('Custom Output')
#                                                         # print(
#                                                         #     "path du dataset: ", realFilePathDataset)

#                                                         print(
#                                                             f"{jobN}-->{logfile}-->filePathDataset:{len(filePathDataset)}-->{datasetValue} --> Path du dataset:{realFilePathDataset} -->Custom Output \n")


#                                                     # recordType.append('CustomOutput')                            # ajout de lattribut Custominput dams la colonne recordType

#             else:
#                 # jobName.append(jobFromXML)  # col 1
#                 pass
                


# # # # pas commode de gerer les length, l'astuce trouve est de manipuler les colonnes sous un format dataframe

# print("|----Informations sur les elements extraits de ce fichier XML---|")
print("1./Nombre de jobs dans ce fichier:", len(jobName))
print("2./Nombre de stage dans ce fichier:", len(stageName))
print("3./Nombre de stageType dans ce fichier:", len(stageType))
# # print("4./Nombre de fileName de ce fichier:", len(fileName))
print("4./Nombre de logFile de ce fichier:", len(logFile))
# print("4./Nombre de fileName de ce fichier:", len(fileName))
# print("4./Nombre de datasetName de ce fichier:", len(datasetName))
# print("5./Nombre de fileNameTrue de ce fichier:", len(fileNameTrue))
# print("5./Nombre de datasetValueTrue de ce fichier:", len(datasetValueTrue))
print("5./Nombre de recordType de ce fichier:", len(recordType))
# # print("6./Nombre de datasetValue de ce fichier:", len(datasetValueTrue),datasetValueTrue)
# # # print('\n')




# # jobName = []
# # stageName = []
# # stageType = []
# # recordType = []
# # fileName = []
# # fileNameTrue =[]
# # datasetValueTrue =[]
# # logFile =[]

# data ={
#     "jobName" : jobName,
#     'logFile': logFile,
#     # "stageName" :stageName,
#     # "stageType": stageType,
#     'fileName': fileName,
#     'fileNameTrue': fileNameTrue,
#     'datasetName': datasetName,
#     'datasetValueTrue': datasetValueTrue,
#     'recordType': recordType,
# }

# df = pd.DataFrame(data)
# # print(df)
# df.to_csv('/Users/ganasene/Desktop/outputxml3.csv')
