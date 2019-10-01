# Fonctionnalité du script main_scrpit.py

1. lister par projet, tous les jobs et les executables dans lesquels ils sont.  

# Architecture  d'un fichier XML  

voir ce lien à propos de DOM (document Object Model) 
http://41mag.fr/quest-ce-que-le-dom-dune-page-web.html


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
    |        |        |    |                             |
    |        |        |    |                             |___subrecord [ attributs: None]
    |        |        |    |                                  |
    |        |        |    |                                  |___proprety [ attributs: Name, Value]


# Notes xml SUPprd  


1. dataset
   - Toutes les valeurs des dataset ne sont pas sous la forme path.ds.  

    - certains valeurs sont du type:   /work/home/dsint1/applications/sup/feuillet/datastage/temp/PAR_FIC_CPTE_RENDU_REJETS_NB.ds  


- IIS-DSEE-TFCN-00009 in LABISChrgOCTAV01OCTAVT_OEUV job

2. RESULTAT TRAITEMEMNT FICHIER XML

    - SUPprd.xml  
    ------------
        > nombre de jobs: 701  
        > nombre de ligne :  
        > files found:

            >> fileValueTrueRecord: 292,
            >> datasetValueTrueRecord: 259

    - DOC-FTSACprd.xml :113
        > nombre de jobs : 113  
        > nombre de ligne : 305  
        > files found:  

            >> fileValueRecord: 0,
            >> fileValueTrueRecord: 0 
            >> datasetValueRecord: 0  
            >> datasetValueTrueRecord: 0 

    - MGTPRD.xml  
        > nombre de jobs : 1019
        > nombre de ligne : 7405
        > files found:

            >> fileValueRecord: 82,
            >> fileValueTrueRecord: 82,        
            >> datasetValueRecord: 1333 ,  
            >> datasetValueTrueRecord: 1333  

# Travail demandé

1. Extraire a partir des fichiers xml donnés:
   - Tous les jobs present dans chacun de ces fichiers xml   /ok
        a. le resultat de cette operation va retourner une listes de tous les jobs trouve dans un fichier XML donnee.
            note : l'objectif c'est de le faire avec tous les fichiers xml
    - Pour chaque job, extraire tous les noms et types de stage, files(txt, nan, csv, ds).   
    - Remplacer les references repertoire des files par leurs valeurs exactes qui se trouvent dans les fichiers execution (log).
    - Creer une table avec comme colonnes:
          -  
  
2. Aller chercher dans les jobs correspondants dans les fichiers executables (les logs).
        a. lire un par un tous les fichiers executables (log) qui sont le dossier logfullDS (faire une booucle for dans lequel with open sera appele)
        b. ensuite toujours dans cette meme boucle for, parcourir la liste collectionJobFromXML et pour chaque element i (qui est en fait le nom du job recuperer dans le fichier xml) de cette liste tester si il est bien presence un des fichier log.
            Si oui afficher le filename de ce fichier

## Methodologies  

j'ai obtenu les resultats suivants avec l'approche suivante:  

### App1: Approche naive: 






## Resultat bash
```BASH

SOC-CLIPIprd.xml

SOC-CLIPIprd.xml, jobFromXML, logfile
jobNameRecord: 337
, logFileRecord: 337,
     stageName: 337, 
 stageType: 337,
     recordType: 337 ,
 fileValueRecord: 1,
     fileValueTrueRecord: 1,
  datasetValueRecord: 0     ,
 datasetValueTrueRecord: 0 

[Done] exited with code=0 in 13.103 seconds
--------------------------------------------

DOC-OCTAVprd.xml

DOC-OCTAVprd.xml, jobFromXML, logfile
jobNameRecord: 124,
logFileRecord: 124,
stageName: 124, 
stageType: 124,
recordType: 124 ,
fileValueRecord: 0,
fileValueTrueRecord: 0,
datasetValueRecord: 0     ,
datasetValueTrueRecord: 0 

----------------------------------

[Done] exited with code=0 in 5.37 seconds

UTIprd.xml

UTIprd.xml, jobFromXML, logfile
jobNameRecord: 49
logFileRecord: 491,
stageName: 491, 
stageType: 491,
recordType: 491 ,
fileValueRecord: 0,
fileValueTrueRecord: 0,
datasetValueRecord: 0     ,
datasetValueTrueRecord: 0 

[Done] exited with code=0 in 28.5 seconds
----------------------------------------------

Docprd.xml

Docprd.xml, jobFromXML, logfile
jobNameRecord: 1409
logFileRecord: 1409,
stageName: 1409, 
stageType: 1409,
recordType: 1409 ,
fileValueRecord: 33,
fileValueTrueRecord: 33,
datasetValueRecord: 4     ,
datasetValueTrueRecord: 4 

[Done] exited with code=0 in 48.027 seconds
----------------------------------------------

MGTPRD.xml

MGTPRD.xml, jobFromXML, logfile
jobNameRecord: 7405
logFileRecord: 7405,
stageName: 7405, 
stageType: 7405,
recordType: 7405 ,
fileValueRecord: 82,
fileValueTrueRecord: 82,
datasetValueRecord: 1333     ,
datasetValueTrueRecord: 1333 

[Done] exited with code=0 in 567.259 seconds
---------------------------------------------

DOC-FTSACprd.xml

jobNameRecord: 305,
logFileRecord: 305,
stageName: 305, 
stageType: 305,
recordType: 305 ,
fileValueRecord: 0,
fileValueTrueRecord: 0,
datasetValueRecord: 0     ,
datasetValueTrueRecord: 0 

[Done] exited with code=0 in 9.465 seconds
---------------------------------------------

```
