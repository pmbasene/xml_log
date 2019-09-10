#!/anaconda3/bin/python
# coding: utf-8

from lxml import etree
import xml.etree.ElementTree as ET
import os
import numpy as np
import pandas as pd
import random
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
# DOC-.xml

class ParseElementXML():
    """cette classe prend en entree le nom du fichier XML a parser et pretourne une colletction (format liste)nommé collectionJobFromXML des jobs dun fichier XML
    Note: le fichier XML doit etre dans le meme dossier que le fichier py """

    def document(self, fileXML="SUPprd.xml"):
        #DOC-FTSACprd.xml, SUPprd.xml , MGTPRD.xml
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
        # __________________________________#
        # print(fullPath)
        return fullPath

    def getRoot(self, fullPath):
        tree = etree.parse(fullPath)
        root = tree.getroot()
        # print(root.tag, root.attrib)
        # print(f"Infos - nombre de  child pour {root.tag}:", len(root))
        # print("_________-------_____----Header------___----___----___----___ ")
        return root

    def removeDuplicates(self, listDoublons):  # not use
        '''cette methode permet de supprimer les doublons dans une liste. 
            Elle prend en entree une liste d'elements et retourne ensuite la meme liste dans laquelle tous elements dupliques sont supprimes'''
        liste = []
        for i in listDoublons:
            if i not in liste:
                liste.append(i)
        return liste
 
    def recupererCleOuValeurInString(self, string, sep=" "):
        '''cette fonction prend en entree une chaine de caractere <str>  
        et un separateur(= ou , ou ; ou : etc) et retourne la cle et la valeur de la chaine splitee'''
        key, val = string.split(sep)
        Key = key.strip()
        Val = val.strip()
        return Key, Val

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

    def makePathForFileOrFileDataset(self, filePath, PAR_list):
        realFilePath = ""
        if len(filePath) == 1:
            realFilePath = os.path.join(filePath[0])
            realFilePath = self.buildFullPath(PAR_list, realFilePath)

        elif len(filePath) == 2:
            realFilePath = os.path.join(filePath[0], filePath[1])
            realFilePath = self.buildFullPath(PAR_list, realFilePath)

        elif len(filePath) == 3:
            realFilePath = os.path.join(filePath[0], filePath[1], filePath[2])
            realFilePath = self.buildFullPath(PAR_list,realFilePath)
           
        elif len(filePath) == 4:
            realFilePath = os.path.join(filePath[0], filePath[1], filePath[2], filePath[3])
            realFilePath = self.buildFullPath(PAR_list,realFilePath)
           
        elif len(filePath) == 5:
            realFilePath = os.path.join(filePath[0], filePath[1], filePath[2], filePath[3], filePath[4])
            realFilePath = self.buildFullPath(PAR_list,realFilePath)
           
        # else:
        #     fileValueTrueRecord.append(None)

        return realFilePath

    def retrieveFilePath(self, fileValue, blockTextPar):
        # les filepath fonctionnent correctement si le bloc est au debut du logfile. donc il me faut trouver une solution pour resoudre le cas ou le boc est a une ligne x du logfile. pour cela se referer a la variable PAR
        filePath = []
        # recuperation des parametres directory
        # print("PAR",len(PAR_list),PAR_list)
        blockTextPar_list = blockTextPar
        PAR_list = self.recuperer_PAR_dir(fileValue)

        # la valeur PAR_list = 0  signifie que le bloc n'est pas en debut du logfile
        for par in PAR_list:
            for line in blockTextPar_list:
                #         line = line.strip()  # pour enlever tous les espaces a gauche et a droite
                if r'=' in line:       # ceci est du a une levee dexcpection  ie unpacking items
                    kline, vline = self.recupererCleOuValeurInString(
                        line, sep="=")
                    if par == kline:
                        filePath.append(vline)

        return PAR_list ,filePath 

    def funcname(self, *param):
        #
        # PropertyOrcollection, fileValueRecord, fileValueTrueRecord, datasetValueRecord, datasetValueTrueRecord

        if PropertyOrcollection.tag == 'Collection' and PropertyOrcollection.attrib.get("Name") == 'Properties':
            # attribute_Name = PropertyOrcollection.attrib.get('Name')
            
            for subrecord in PropertyOrcollection:     # ACCES NIVEAU 5 

                 for prop in subrecord:
                    if prop.attrib.get('Name') == 'Value':
                        Textprop = str(prop.text)

                        fileValue = Textprop
                        if (r')file' in fileValue) and (jobN == jobFromXML):

                            # print(fileValue)
                            PAR_list, filePath = self.retrieveFilePath(fileValue, blockTextPar)
                            realFilePath = self.makePathForFileOrFileDataset(filePath, PAR_list)
                            # print(realFilePath)

                            fileValueRecord.append(fileValue)
                            fileValueTrueRecord.append(realFilePath)

                            tup = (jobN, logfile, fileValue, realFilePath,attribute_type)
                            tuple_Job_logfile_file_trueFile_attr.append(tup)
                            # print(f"{jobN},{logfile},{fileValue},{realFilePath},NaN,NaN,NaN ,NaN,{attribute_type}")
                            
                            # print(f"jobN, logfile, fileValue, realFilePath, datasetValue, realFilePathDataset, stageName, stageType,recordTypeRecord")

                            # return fileValueRecord, fileValueTrueRecord,

                            # print(tup)

                        datasetValue = Textprop
                        if ('.ds' in datasetValue) and (jobN == jobFromXML):

                             # print(realFilePathDataset)
                            PAR_dataset_list, filePathDataset = self.retrieveFilePath(datasetValue, blockTextPar)
                            realFilePathDataset = self.makePathForFileOrFileDataset(filePathDataset, PAR_dataset_list)

                            datasetValueRecord.append(datasetValue)
                            datasetValueTrueRecord.append(realFilePathDataset)

                            # print(f"{jobN},{logfile},NaN,NaN,{datasetValue},{realFilePathDataset},NaN,NaN,{attribute_type}")
                            # print(f"jobN, logfile, fileValue, realFilePath, datasetValue, realFilePathDataset, stageName, stageType,recordTypeRecord")



                            #  return realFilePathDataset, datasetValueTrueRecord
                
        return fileValueRecord, fileValueTrueRecord, datasetValueRecord, datasetValueTrueRecord, tuple_Job_logfile_file_trueFile_attr

class ParseLog():

    def changeDir(self):
        path_to_logfullDS = '/Users/ganasene/Downloads/folder/logsfullDS'
        r = os.chdir(path_to_logfullDS)
        return r

    def blockEventID(self, string):
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

content = p.cleaning_files()
### affichage
# print("------ traitement1: Resultat nettoyage du dossier {} !!!!------".format(p))
for i in content:
    # print(i, sep='\n')
    pass
# print('---<>_<>__ Dossier nettoye!!!!---<>_<>__', sep='\n')

# # ===================MAIN1===================================================
### Initiation des listes suivants en vue de creeer un dataframe en output
# jobName = []
# stageName = []
# stageType = []
# recordType = []
# fileName = []
# fileNameTrue = []
datasetName = []
datasetValueTrue = []
logFile = []

# Initialisation du tuple file_job: relier les logfile au jobname
tuple_Job_logfile_file_trueFile_attr = []

#compteur
num_job = []  # nombre de job pour un fic XML donnee
num_stage = []  # nombre de job pour un fic XML donnee

# basePath = os.path.dirname(__file__)
# fullPath = os.path.join(basePath, "DOC-.xml")
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
# print("------ traitement2: collection des jobs dans xml {} !!!!------".format(fullPath))
# print(len(collectionJobFromXML))
collectionJobFromXML = list(set(collectionJobFromXML))
collectionJobFromXML = p.removeDuplicates(collectionJobFromXML)
collectionJobFromXML.remove(None)
# print(len(collectionJobFromXML), sep='\n')
# print(collectionJobFromXML)

######## ======================== ======================


q = ParseLog()
path_to_logfullDS = q.changeDir()           # changement de repertoire
tuple_job_logfile = []
compt = 0

jobFromXMLpd =[]
logfilepd = []
tuple_job_logfilepd = []

# # +++++++++++====================== creation table :job - logfile - pk =====================
# for logfile in os.listdir(path_to_logfullDS):
#     with open(logfile, encoding='utf8') as f:
#         f = f.read()
#         for idx, jobFromXML in enumerate(collectionJobFromXML):
#             if jobFromXML in f:
#                 compt += 1
#                 # print(f"job {compt}/{len(collectionJobFromXML)} {jobFromXML} -->{logfile}")
#                 job_logfile = (jobFromXML, logfile)
#                 tuple_job_logfilepd.append(job_logfile)

# for i in range(len(tuple_job_logfilepd)):
#     jobFromXMLpd.append(tuple_job_logfilepd[i][0])
#     logfilepd.append(tuple_job_logfilepd[i][1])

# pk = random.sample(range(1000), len(tuple_job_logfilepd))

# dt0 ={
#     'pk':pk,
#     'jobFromXML': jobFromXMLpd,
#     'logfile': logfilepd,
# }

# df0 = pd.DataFrame(dt0)
# print(df0)

# # # ============================ 

print(f"jobName,logFile,filePath, realFilePath,datasetFile,realDatasetFilePath,stageName,stageType,recordType")


# print(jobN, logfile, fileValue, realFilePath, datasetValue, realFilePathDataset, attribute_type)




# jobNameRecord = []
# logFileRecord = []
# stageNameRecord = []
# stageTypeRecord = []
# recordTypeRecord = []
fileValueRecord = []
fileValueTrueRecord = []
datasetValueRecord = []
datasetValueTrueRecord = []

for logfile in os.listdir(path_to_logfullDS):
    with open(logfile, encoding='utf8') as f:
        f = f.read()
        for idx,jobFromXML in enumerate(collectionJobFromXML):

            if jobFromXML in f:
                compt += 1
                # print(f"job {compt}/{len(collectionJobFromXML)} {jobFromXML} -->{logfile}")
                # job_logfile = (idx, jobFromXML, logfile)
                # tuple_job_logfile.append(job_logfile)
                # print(job_logfile)
                # job_logFile[id] = tuple_job_logfile

                blockTextPar = q.blockEventID(f)     # retourne un bloc de lignes de type (key,value) separe par le signe '=' dans lequel se trouve les repertoires
                                                     # ce bloc sera utilise dans la section outupt file et permettra de trouver la valeur exacte du fileName et datasetName
                jobNameRecord = []
                logFileRecord = []
                stageNameRecord = []
                stageTypeRecord = []
                recordTypeRecord = []

                for job in root:  # ACCES NIVEAU 2
                    jobN = job.attrib.get('Identifier')

                    for record in job: #ACCES NIVEAU 3

                        attribute_type = record.attrib.get('Type')

                        if attribute_type == 'CustomStage':
                           
                            jobNameRecord.append(jobN)     # col 1
                            logFileRecord.append(logfile)     # col 1
                            recordTypeRecord.append(attribute_type)    # col 4

                            for PropertyOrcollection in record:    #ACCES NIVEAU 4

                                attribute_Name = PropertyOrcollection.attrib.get('Name')

                                if attribute_Name == 'Name':
                                    TextPropertyOrcollection = str(PropertyOrcollection.text)
                                    stageName = TextPropertyOrcollection
                                    print(f"{jobN}, {logfile}, NaN, NaN, NaN,  NaN, {stageName},NaN, {attribute_type}")
                                    # print(f"jobN, logfile, fileValue, realFilePath, datasetValue, realFilePathDataset, stageName, stageType,recordTypeRecord")
          

                                elif attribute_Name == 'StageType':
                                    TextPropertyOrcollection = str(PropertyOrcollection.text)
                                    stageType = TextPropertyOrcollection
                                    print(f"{jobN}, {logfile}, NaN, NaN, NaN, NaN, NaN,{stageType},{attribute_type}")

                                    # print(f"jobN, logfile, fileValue, realFilePath, datasetValue, realFilePathDataset, stageName, stageType,recordTypeRecord")

                                # col 1

                            stageNameRecord.append(stageName)                                        # col 1
                            stageTypeRecord.append(stageType)                                        # col 1
                        elif attribute_type == 'CustomOutput':

                            jobNameRecord.append(jobN)     # col 1
                            logFileRecord.append(logfile)     # col 1
                            recordTypeRecord.append(attribute_type)    # col 4
                            stageNameRecord.append(None)     # col 1
                            stageTypeRecord.append(None)     # col 1

                            for PropertyOrcollection in record:
                                
                                fileValueRecord, fileValueTrueRecord, realFilePathDataset, datasetValueTrueRecord, tuple_Job_logfile_file_trueFile_attr = p.funcname(
                                    PropertyOrcollection, fileValueRecord, fileValueTrueRecord, datasetValueRecord, datasetValueTrueRecord)
                                                                                                                               
                                # print(jobN,logfile+"-->filePath",len(filePath), filePath)
                        elif attribute_type == 'CustomInput':

                            jobNameRecord.append(jobN)     # col 1
                            logFileRecord.append(logfile)     # col 1
                            recordTypeRecord.append(attribute_type)    # col 4
                            stageNameRecord.append(None)     # col 1
                            stageTypeRecord.append(None)     # col 1

                            for PropertyOrcollection in record:
                                
                                fileValueRecord, fileValueTrueRecord, realFilePathDataset, datasetValueTrueRecord, tuple_Job_logfile_file_trueFile_attr = p.funcname(
                                    PropertyOrcollection, fileValueRecord, fileValueTrueRecord, datasetValueRecord, datasetValueTrueRecord)

            else:
                # jobName.append(jobFromXML)  # col 1
                pass


# print("lignes:",len(jobNameRecord))
# tuple1_Job_logfile_recordType = []
# for k in  range(len(jobNameRecord)):
 
#     tupl = (jobNameRecord[k], logFileRecord[k], recordTypeRecord[k])
#     tuple1_Job_logfile_recordType.append(tupl)

    
# # print(tuple_Job_logfile_file_trueFile_attr)
# # print(tuple1_Job_logfile_recordType)
# print('')
# print(len(tuple_Job_logfile_file_trueFile_attr))   #243
# print(len(tuple1_Job_logfile_recordType))     # 3433

# l1 = []
# l1True= []
# for j in range(len(tuple_Job_logfile_file_trueFile_attr)):
#     T_job =  tuple_Job_logfile_file_trueFile_attr[j][0]
#     T_jobFile = tuple_Job_logfile_file_trueFile_attr[j][1]

#     T_attr = tuple_Job_logfile_file_trueFile_attr[j][4]

#     T_fileValue = tuple_Job_logfile_file_trueFile_attr[j][2]
#     T_trueFileValue = tuple_Job_logfile_file_trueFile_attr[j][3]

#     T = (T_job,T_jobFile,T_attr)
#     # print(T)
#     for triplet in tuple1_Job_logfile_recordType:

#         # print("tripet", triplet)
#         print("T", T)

#         if T == triplet:
#             # print(T)
#             # print(triplet)
            

#             l1.append(T_fileValue)
#             l1True.append(T_trueFileValue)



# print(len(l1))
# print(len(l1True))





# print(f"jobNameRecord: {len(jobNameRecord)}\n, logFileRecord: {len(logFileRecord)},\n stageName: {len(stageNameRecord)}, \n stageType: {len(stageTypeRecord)},\n \
#     recordType: {len(recordTypeRecord)} ,\n fileValueRecord: {len(fileValueRecord)},\n fileValueTrueRecord: {len(fileValueTrueRecord)},\
#       \n  datasetValueRecord: {len(datasetValueRecord)} ,\n datasetValueTrueRecord: {len(datasetValueTrueRecord)} \n")
# # print(f"\t\t\t. jobNameRecord, {jobNameRecord} \n, logFileRecord ,{logFileRecord} \n , stageName: {stageNameRecord} \n,stageType: {len(stageTypeRecord)}, \n 'recordType':{recordTypeRecord} \n")


# # # print("|----Informations sur les elements extraits de ce fichier XML---|")
# # # print("1./Nombre de jobs dans ce fichier:", len())
# # # print("2./Nombre de stage dans ce fichier:", len(stageName))
# # # print("3./Nombre de stageType dans ce fichier:", len(stageType))
# # # # # print("4./Nombre de fileName de ce fichier:", len(fileName))
# # # print("4./Nombre de logFile de ce fichier:", len(logFile))
# # # # print("4./Nombre de fileName de ce fichier:", len(fileName))
# # # # print("4./Nombre de datasetName de ce fichier:", len(datasetName))
# # # # print("5./Nombre de fileNameTrue de ce fichier:", len(fileNameTrue))
# # # # print("5./Nombre de datasetValueTrue de ce fichier:", len(datasetValueTrue))
# # # print("5./Nombre de recordType de ce fichier:", len(recordType))
# # # # # print("6./Nombre de datasetValue de ce fichier:", len(datasetValueTrue),datasetValueTrue)
# # # # # # print('\n')


# data ={
#     "jobName" : jobNameRecord,
#     'logFile': logFileRecord,
#     "stageName" :stageNameRecord,
#     "stageType": stageTypeRecord,
#     # 'fileValueRecord': fileValueRecord,
#     # 'fileValueTrueRecord': fileValueTrueRecord,
#     # 'datasetValueRecord': datasetValueRecord,
#     # 'datasetValueTrueRecord': datasetValueTrueRecord,
#     'recordType': recordTypeRecord,
# }

# df = pd.DataFrame(data)
# # print(df)
# # df.to_csv('/Users/ganasene/Desktop/resultats_xml/outputxml_input_output_stage.csv')