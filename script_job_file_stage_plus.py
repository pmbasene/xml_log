#!/anaconda3/bin/python
# coding: utf-8

import os
from lxml import etree
import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
from pprint import pprint
# import random
# from XML_HANDLE import *

from XML_HANDLE import Xml_logfile
from clean_file import CleanFolder

""" 
DESCRIPTION DES MODULES
--------------------------
Modules :
- lxml: permet de parser les fichiers xml. 
Pour plus d'infos rtfm la documentation sur le package lxml consulter:  https://docs.python.org/3.4/library/xml.etree.elementtree.html#module-xml.etree.ElementTree   ;)
- Pandas et Numpy permettent de travailler sur des dataframes et de manipuler les donnees plus facilement.
- clean_file.py permet de nettoyer au prealable le dossier qui contient les excecutables.

Taches :
- extraire les valeurs des cles(jobname, filename, directory) qui sont en format string ou variable depuis les fichiers XML.
- recuperer leurs valeurs exactes en utilisant les jobnames des fichiers xml pour trouver leurs fichiers excecutables corespndantes.

"""


class ParseElementXML():
    """cette classe a ete creee dans l'optique de faciliter l'extraction de données à partir d'un fichier de format XML.
    Elle comporte un ensemble de fonctions qui permettent de recuperer, manipuler, et extraire à partir du xml-projet

    Note: Pour l'instant afin d'eviter toutes erreurs d'excecution, les fichier XML doivent etre dans le meme dossier que le prog  main_scrpit.py """

    def document(self, fileProjetXML="SUPprd.xml"):
        #DOC-FTSACprd.xml, SUPprd.xml , MGTPRD.xml
        """cette fonction prend en input le nom du fichier .xml et renvoie le path absolu. Ce dernier sera utilise aussi en input par la fonction 
        getroot() pour instancier le module lmxl.etree """
        basePath = os.path.dirname(
            __file__)    # path abs du dossier de ce file
        fullPath = os.path.join(basePath, fileProjetXML)
        # fullPath = os.path.abspath(fileProjetXML)
        # os.chdir(fullPath)
        # # ---------------------------------------------------------------------,
        # try:
        #     basePath = os.path.dirname(__file__)
        #     fullPath = os.path.join(basePath, fileProjetXML)
        #     print(fullPath)
        # return fullPath
        # except OSError:
        # return "verifier bien le path du fichier. Il doit etre dans le dossier"
        # __________________________________#
        # print(fullPath)
        return fullPath

    def getRoot(self, fullPath):
        """getroot() prend en input le path absolu un objet appele root """
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
        # return liste
        # liste = [liste.append(x) for x in listDoublons if x not in liste]   # list method comprehension
        return liste

    def recupererCleOuValeurInString(self, string, sep=" "):
        '''cette fonction prend en entree une chaine de caractere <str>  
        et un separateur(= ou , ou ; ou : etc) et retourne la cle et la valeur de la chaine splitee'''
        key, val = string.split(sep)
        Key = key.strip()
        Val = val.strip()
        return Key, Val

    def recuperer_PAR_dir(self, string):
        """ cette fonction prend en entree une la valeur du file du xML (format string) et retourne une liste d'elements filtres (format list).
        Comment ca marche : Elle splite d'abord une chaine de caractere en se basant sur le separator # qui est donne en entree, ensuite filtre tous les items non desirables 
        tels que les items vides, underscore, etc. et retourne finalement que les variables-repertoires du logfile  """
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
        """ cette fonction prend en input le filePath cad la liste des key-repertoire des chemins PATH des files,...  """

        realFilePath = " "
        if len(filePath) == 1:
            realFilePath = os.path.join(filePath[0])
            realFilePath = self.buildFullPath(PAR_list, realFilePath)

        elif len(filePath) == 2:
            realFilePath = os.path.join(filePath[0], filePath[1])
            realFilePath = self.buildFullPath(PAR_list, realFilePath)

        elif len(filePath) == 3:
            realFilePath = os.path.join(filePath[0], filePath[1], filePath[2])
            realFilePath = self.buildFullPath(PAR_list, realFilePath)

        elif len(filePath) == 4:
            realFilePath = os.path.join(
                filePath[0], filePath[1], filePath[2], filePath[3])
            realFilePath = self.buildFullPath(PAR_list, realFilePath)

        elif len(filePath) == 5:
            realFilePath = os.path.join(
                filePath[0], filePath[1], filePath[2], filePath[3], filePath[4])
            realFilePath = self.buildFullPath(PAR_list, realFilePath)

        elif len(filePath) == 6:
            realFilePath = os.path.join(
                filePath[0], filePath[1], filePath[2], filePath[3], filePath[4], filePath[5])
            realFilePath = self.buildFullPath(PAR_list, realFilePath)

        elif len(filePath) == 7:
            realFilePath = os.path.join(
                filePath[0], filePath[1], filePath[2], filePath[3], filePath[4], filePath[5], filePath[5])
            realFilePath = self.buildFullPath(PAR_list, realFilePath)

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

        return PAR_list, filePath

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
                            PAR_list, filePath = self.retrieveFilePath(
                                fileValue, blockTextPar)
                            realFilePath = self.makePathForFileOrFileDataset(
                                filePath, PAR_list)
                            # print(realFilePath)

                            fileValueRecord.append(fileValue)
                            fileValueTrueRecord.append(realFilePath)

                            tup = (jobN, logfile, fileValue,
                                   realFilePath, attribute_type)
                            tuple_Job_logfile_file_trueFile_attr.append(tup)
                            # print(
                            # f"{jobN},{logfile},{fileValue},{realFilePath},NaN,NaN,NaN ,NaN,{attribute_type}")
                            # print(f"jobN, logfile, fileValue, realFilePath, datasetValue, realFilePathDataset, stageName, stageType,recordTypeRecord")
                            # return fileValueRecord, fileValueTrueRecord,
                            # print(tup)

                        datasetValue = Textprop
                        if ('.ds' in datasetValue) and (jobN == jobFromXML):

                             # print(realFilePathDataset)
                            PAR_dataset_list, filePathDataset = self.retrieveFilePath(
                                datasetValue, blockTextPar)
                            realFilePathDataset = self.makePathForFileOrFileDataset(
                                filePathDataset, PAR_dataset_list)

                            datasetValueRecord.append(datasetValue)
                            datasetValueTrueRecord.append(realFilePathDataset)
                            # print(
                            # f"{jobN},{logfile},NaN,NaN,{datasetValue},{realFilePathDataset},NaN,NaN,{attribute_type}")
                            # print(f"jobN, logfile, fileValue, realFilePath, datasetValue, realFilePathDataset, stageName, stageType,recordTypeRecord")
                            #  return realFilePathDataset, datasetValueTrueRecord

        return fileValueRecord, fileValueTrueRecord, datasetValueRecord, datasetValueTrueRecord, tuple_Job_logfile_file_trueFile_attr

        # def funcname2(record):

        #     for PropertyOrcollection in record:  # ACCES NIVEAU 4
        #         attribute_Name = PropertyOrcollection.attrib.get('Name')

        #         if attribute_Name == 'Name':
        #             TextPropertyOrcollection = str(PropertyOrcollection.text)
        #             stageName = TextPropertyOrcollection
        #                             # print(f"{jobN}, {logfile}, NaN, NaN, NaN,  NaN, {stageName},NaN, {attribute_type}")
        #                             # print(f"jobN, logfile, fileValue, realFilePath, datasetValue, realFilePathDataset, stageName, stageType,recordTypeRecord")

        #         elif attribute_Name == 'StageType':
        #             TextPropertyOrcollection = str(PropertyOrcollection.text)
        #             stageType = TextPropertyOrcollection
        #             # print(f"{jobN}, {logfile}, NaN, NaN, NaN, NaN, NaN,{stageType},{attribute_type}")
        #             # print(f"jobN, logfile, fileValue, realFilePath, datasetValue, realFilePathDataset, stageName, stageType,recordTypeRecord")


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


### ===================MAIN0 : nettoyage du dossier ===================================================
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

datasetName = []
datasetValueTrue = []
logFile = []

b = Xml_logfile()
######## ======================== ======================

q = ParseLog()
path_to_logfullDS = q.changeDir()           # changement de repertoire
tuple_job_logfile = []
compt = 0
jobFromXMLpd = []
logfilepd = []
tuple_job_logfilepd = []

print(f'Projet,job,file,truefile,stage,idIO,typeIO')

# fileProjetXML = "MGTPRD.xml"
for fileProjetXML in os.listdir('/Users/ganasene/Downloads/projet_xml_insyco/xmlFile/'):
    if (fileProjetXML != ".DS_Store") and (fileProjetXML != ".vscode"):

        # fileProjetXML, ext= os.path.splitext(fileProjetXML)

        # print(fileProjetXML)

        filename, ext = os.path.splitext(fileProjetXML)

        ###DOC-FTSACprd.xml, SUPprd.xml , MGTPRD.xml, SOC-CLIPIprd.xml, DOC-OCTAVprd.xml
        ###UTIprd.xml Docprd.xml,SOC-OSCARprd.xml
        #no files in FTSACprd.xml ,DOC-OCTAVprd.xml, UTIprd.xml
        #1 file in SOC-CLIPIprd.xml
        fullPath = b.document(fileProjetXML)

        # Instanciation du module etree
        ## methode parse
        tree = etree.parse(fullPath)
        root = tree.getroot()

        # Initiation des listes de collection des jobs extraits dans les fichiers xml
        jobList = []
        stageNumberList= []
        stageList = []
        fileInput = []
        fileOutput= []
        idInputList = []
        idOuputList = []

        p = ParseElementXML()
        fullPath = p.document(fileProjetXML)
        root = p.getRoot(fullPath)


        # snippet pour  rechercher et collecter les PAR au niveau des logs
        for logfile in os.listdir(path_to_logfullDS):
            with open(logfile, encoding='utf8') as f:
                f = f.read()
                # for idx, jobFromXML in enumerate(collectionJobFromXML):
                    # if jobFromXML in f:

                for job in root:
                    jobName = job.attrib.get('Identifier')
                    jobName = str(jobName)

                    # print(jobName)
                    if jobName in f:
                        # print(jobName+'-->'+logfile)
                            
                        jobList.append(jobName)
                        blockTextPar = q.blockEventID(f)

                        for record in job:

                            attribute_type = record.attrib.get('Type')
                            attribute_identifier = record.attrib.get('Identifier')

                            if attribute_type == 'CustomStage':
                                stageNumberList.append(attribute_type)    # col 4


                                for PropertyOrcollection in record:  # ACCES NIVEAU 4
                                    attribute_Name = PropertyOrcollection.attrib.get('Name')
                                    if attribute_Name == 'Name':
                                        
                                        stageName = str(PropertyOrcollection.text)
                                        stageList.append(stageName)


                                    elif attribute_Name == 'InputPins':
                                        idxs = str(PropertyOrcollection.text)          # idxs ---> identifianr
                                        
                                        if r"|" in idxs:
                                            idInput = idxs.split('|')       # les id des inputs
                                            idInputList.append(idInput)
                                            # print(jobName+';'+stageName+';'+str(idInputList)+';'+attribute_Name)
                                            
                                        else:
                                            idInput = idxs
                                            idInputList.append(idInput)
                                            # print(jobName+';'+stageName+';'+str(idInputList)+';'+attribute_Name)

                                        # print(jobN,'--',stageType,'--', stageName,'--',idInput,'(I)')
                                
                                    elif attribute_Name == 'OutputPins':
                                        idxs = str(PropertyOrcollection.text)          # idxs ---> identifianr
                                        if r"|" in idxs:
                                            idOutput = idxs.split('|')
                                            idOuputList.append(idOutput)
                                            
                                            
                                            # print(jobName+';'+stageName+';'+str(idOuputList)+';'+attribute_Name)

                                        else:
                                            idOutput = idxs
                                            idOuputList.append(idOutput)
                                            # print(jobName+';'+stageName+';' +str(idOuputList)+';'+attribute_Name)


                                            

                            elif attribute_type == 'CustomInput':
                                for PropertyOrcollection in record:
                                    if PropertyOrcollection.tag == 'Collection' and PropertyOrcollection.attrib.get("Name") == 'Properties':
                                        # attribute_Name = PropertyOrcollection.attrib.get('Name')
                                        for subrecord in PropertyOrcollection:     # ACCES NIVEAU 5
                                            # print(idInput, 'Input')
                                            # print(stageName)
                                            

                                            for prop in subrecord:
                                                if prop.attrib.get('Name') == 'Value':
                                                    fileValue = str(prop.text)
                                                    datasetValue = str(prop.text)
                                                    if (r')file' in fileValue) and (attribute_identifier == idInput):
                                                        # if attribute_identifier == idInput:
                                                        # print(idInput, 'Input')
                                                        # print(stageName)

                                                        
                                                        PAR_list, filePath = p.retrieveFilePath(fileValue, blockTextPar)
                                                        realFilePath = p.makePathForFileOrFileDataset(  filePath, PAR_list)
                                                        

                                                        print(filename+','+jobName+','+fileValue+','+realFilePath+','+stageName+','+attribute_identifier+','+attribute_type)
                                                        fileInput.append(fileValue)

                                                    if ('.ds' in datasetValue) and (attribute_identifier == idInput):
                                                        # print(idInput, 'Input')
                                                        # print(stageName)

                                                        PAR_list, filePath = p.retrieveFilePath(fileValue, blockTextPar)
                                                        realFilePath = p.makePathForFileOrFileDataset(  filePath, PAR_list)

                                                        print(filename+',' + jobName+','+datasetValue + ',' + realFilePath + ',' + stageName+','+attribute_identifier+','+attribute_type)
                                                        fileInput.append(datasetValue)

                                            

                            elif attribute_type == 'CustomOutput':
                                for PropertyOrcollection in record:
                                    if PropertyOrcollection.tag == 'Collection' and PropertyOrcollection.attrib.get("Name") == 'Properties':
                                        # attribute_Name = PropertyOrcollection.attrib.get('Name')

                                        for subrecord in PropertyOrcollection:     # ACCES NIVEAU 5
                                            for prop in subrecord:
                                                if prop.attrib.get('Name') == 'Value':
                                                    fileValue = str(prop.text)
                                                    datasetValue = str(prop.text)
                                                    if r')file' in fileValue and (attribute_identifier == idOutput):

                                                        PAR_list, filePath = p.retrieveFilePath(fileValue, blockTextPar)
                                                        realFilePath = p.makePathForFileOrFileDataset(  filePath, PAR_list)

                                                        print( filename+','+jobName+','+fileValue+','+realFilePath+','+stageName+','+attribute_identifier+','+attribute_type)
                                                        fileOutput.append(fileValue)

                                                    if ('.ds' in datasetValue) and (attribute_identifier == idOutput):

                                                        PAR_list, filePath = p.retrieveFilePath(fileValue, blockTextPar)
                                                        realFilePath = p.makePathForFileOrFileDataset(  filePath, PAR_list)

                                                        print(filename+','+jobName+','+datasetValue+','+realFilePath +','+stageName+','+attribute_identifier+','+attribute_type)
                                                        fileOutput.append(datasetValue)
                            


# # # print("------ traitement2: collection des jobs dans xml {} !!!!------".format(fullPath))
print(len(jobList))
    

jobList = list(set(jobList))
jobList = p.removeDuplicates(jobList)
# # # stageList = p.removeDuplicates(stageList)    # ne supprime pas les doublons des stages, maybe c important
# # # stageList = p.removeDuplicates(stageList)
# jobList.remove(None)

print(len(jobList))
# # # print(len(stageNumberList))
# # print(len(stageList))
# # print(len(fileInput))
# # print(len(fileOutput))


# # # print(stageList)
# # print(idInputList)
