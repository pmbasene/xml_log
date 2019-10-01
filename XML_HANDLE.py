#!/anaconda3/bin/python
# coding: utf-8

from lxml import etree
import xml.etree.ElementTree as ET
import os
import pandas as pd
import numpy as np

""" 
Pour la documentation sur le package lxml consulter le lien ci-dessous: 
- https://docs.python.org/3.4/library/xml.etree.elementtree.html#module-xml.etree.ElementTree

- Grands traits :
   - extraire la valeur (jobname, filename, directory ) de chaque job
   - relier le jobname de ce fichier xml aux excecutables afin de recuperer la valeur de la cle directory 

- Demarches detaillees:
    1. Extraire tous les jobs d'un ou les fichier(s) xml du repertoire logFullDS
    2. 



- structure dun fichier XML

    XML
    |
    |____DSExport [ attributs: None]
    |        |
    |        |__ Header [ attributs: Identifier, Type, Readonly]
    |        |    |
    |        |    |___job [attributs: Identifier, DateModified, TimeModified]
    |        |        |
    |        |        |___record [attributs: Identifier, Type, Readonly]
    |        |        |    |
    |        |        |    |___property [Name,Type] ||collection [Name, Type]
    |        |        |    |                                |
    |        |        |    |                                |___subrecord [ attributs: None]
    |        |        |    |                                        |
    |        |        |    |                                        |___proprety [ attributs: Identifier, Type, Readonly] ; content: text

"""
class Xml_logfile():


    def document(self, fileXML="SUPprd.xml"):
        basePath = os.path.dirname(__file__)
        fullPath = os.path.join(basePath, fileXML)
        # print(fullPath)
        return fullPath
    
    
    def getElements(self):
        pass



# jobName = []
# stagName = []
# stageType = []
# fileName = []
# tupleFile_Job = []


# #compteur
# num_job = []  # nombre de job pour un fic XML donnee
# num_stage = []  # nombre de job pour un fic XML donnee




#     # DOC-FTSACprod.xml
#     # SUPprd.xml

# # basePath = os.path.dirname(__file__)
# # fullPath = os.path.join(basePath, "SUPprd.xml")
# # print(fullPath)

# b = Xml_logfile()
# fullPath = b.document()
# print(fullPath)

# # instanciation du module etree 
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
#                     TextPropertyOrcollection =str(PropertyOrcollection.text)
                    
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
                            
#                             if prop.attrib.get('Name')=='Name':
#                                 Textprop = str(prop.text)
#                                 if Textprop == "file\(20)":
#                                     pass
#                                     # print("\t\t\t\t>"+Textprop) 
#                                 else:
#                                     pass                       
#                             else:
#                                 Textprop = str(prop.text)
#                                 if ')file' in Textprop:
#                                     # print(f'{jobN} ->{Textprop}')
#                                     tup = (jobN,Textprop)
#                                     tupleFile_Job.append(tup)

#                                     # print("\t\t\t\t4>"+Textprop)
#                                     fileName.append(Textprop)
                                    
#                                 else:
#                                     # fileName.append("NaN")
#                                     pass
#                 else:
#                     pass                    


# # pas commode de gerer les length, l'astuce trouve est de manipuler les colonnes sous un format dataframe

# print("|----Informations sur les elements extraits de ce fichier XML---|")
# print("1./Nombre de jobs dans ce fichier:",len(num_job))
# print("2.Nombre de stage dans ce fichier:", len(stagName))
# print("3./Nombre de stageType dans ce fichier:", len(stageType))
# print("4./Nombre de fileName de ce fichier:", len(fileName))
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


# # print('\n')
# # print(len(tupleFile_Job))
# # print(tupleFile_Job)



# # ++++++++++++++++++++++Dataframe++++++++++++++++++++++++++++
# file = []
# data ={
#     "jobName" : jobName,
#     "stagName" :stagName,
#     "stageType": stageType,
#     'fileName': np.nan
# }

# df = pd.DataFrame(data)
# # print(df)
# # # print(tupleFile_Job)

# # # tupleFile_Job = tupleFile_Job[31]
# # print(len(tupleFile_Job))
# # print(tupleFile_Job)

# # for i in range(len(tupleFile_Job)):
# #     print(tupleFile_Job[i][0], tupleFile_Job[i][1])
# # print('\n')

# idx = []
# tuple_idx_job =[]
# tuple_idx_file=[]
# for key ,job in enumerate(df.jobName):
#     for i in range(len(tupleFile_Job)):
#         if job == tupleFile_Job[i][0]:
#             idx_job = (key, job)
#             idx_file = (key, tupleFile_Job[i][1])
#             # print(idx_job)
#             tuple_idx_job.append(idx_job)
#             tuple_idx_file.append(idx_file)
#             idx.append(key)   
#             file.append(tupleFile_Job[i][1])
#         # else:
#         #     pass
#         #     # file.append('NaN')


# ### recuperation des index
# # print(idx)

# # print(file)     #
# # print("file", len(file))
# # print("idx",len(idx))

# # print(tuple_idx_job)
# # print('\n')
# # print(tuple_idx_file)

# # # ajout des valeurs dans la table


# # print("tuple_idx_job",len(tuple_idx_job))
# # for j in range(165):
# #     # print(j)
# #     # print(tuple_idx_job[j])
# #     # b = df.loc[j] 
# #     # print(b)

# # print(len(tuple_idx_job))

# # affection des files excates à la 4 eme colonne 
# for j in range(len(tuple_idx_job)):
#     # i == index , j== job, et lf = logfile
#     ix=tuple_idx_job[j][0]             # index des valeurs file
#     jb=tuple_idx_job[j][1]
#     lf = tuple_idx_file[j][1]  # file extrait du tuple
#     print(i)            #
#     print(j)
#     print(lf) 

#     df.loc[tuple_idx_job[j][0], 'fileName'] = tuple_idx_file[j][1]
    


# print(df)
# # df.to_csv('/Users/ganasene/Desktop/outputxml.csv')










# # for i in













                # print("\t\t---->"+PropertyOrcollection.attrib.get('Name'))


        
        # print("\t\t---->"+record.attrib.get('Type'))

        # for PropertyOrcollection in record:
        #     # PropertyOrcollection = PropertyOrcollection.tag
        #     print("\t\t"+PropertyOrcollection.tag, PropertyOrcollection.attrib)
        #     # print("\t\t---->"+PropertyOrcollection.attrib.get('Name'))

        #     print(
        #         f"\t\tinfos - nombre de child pour  {PropertyOrcollection.tag}:", len(PropertyOrcollection))
              
            # print("\t\t->"+str(PropertyOrcollection.text))

            # for SubRecord in PropertyOrcollection:
            #     print("\t\t\t"+SubRecord.tag,
            #            PropertyOrcollection.attrib)
            #     print(f"\t\t\tinfos - nombre de child pour  {SubRecord.tag}:", len(
            #     SubRecord))

            #     for j in SubRecord:
            #         print("\t\t\t\t"+j.tag,
            #           SubRecord.attrib)
            #         print(f"\t\t\t\tinfos - nombre de child pour  {j.tag}:", len(
            #         j))





            # # j == Property
                
            


    
   
    





# print(etree.tostring(tree.getroot()))
# for user in tree.xpath("/users/user"):
#     # print(user.text)
#     print(user.tag)
#     # print(user.get("data-id"))
















