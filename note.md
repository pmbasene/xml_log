# Architecture  d'un fichier XML  

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