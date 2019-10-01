# coding:utf-8

import sys 
import os
import subprocess

# sys.stderr.write("test\n")
# sys.stderr.flush()
# sys.stdout.write("test2\n")

# print(type(sys.argv))
# print(os.getcwd())




class CleanFolder():


    def __init__(self, path_to_files= '/Users/ganasene/Downloads/folder/logsfullDS'):

        # initialisation dune liste dans laquelle sera stocke tous les files avec une taille de bits nulle
        self.removed_zero_size_files = []
        # initialisation d'une liste dans laquellle sera stocke les files d'extension type autres txt
        self.removed_no_txt_extenxion_file = []
        self.all_removed_files = []
        self.path_to_files =  path_to_files


    # def __str__(self):
    #     return self.path_to_files      # a decommenter pour voir le path

    def moveToTheFolder(self):
        pass

    def cleaning_files(self):
        '''cette fonction permet de nettoyer les files qui ne seront pas utiles pour le traitement
        Par exemple :
        - les files avec une taille de bits nulle
        - les files d'extension type autres txt
        - les fichiers caches du OS par exple .DS_store pour mac
        note : a ajouter --- afficher le nombre de fichier de taille zero supprime aussi....''' 

        os.chdir(self.path_to_files)
        files = os.listdir(self.path_to_files)
        for file in files:
            stat = os.stat(file)
            file_ext = os.path.splitext(file)
            # print(file_ext)

            if stat.st_size == 0:
                self.removed_zero_size_files.append(file)
                # print(file)
                os.remove(file)                     #suppression des fichiers
                self.all_removed_files.append(file)

            elif file == '.DS_Store':
                subprocess.call(['rm', '.DS_Store'])
                # print('... Suppression du fichier cachee .DS_Store dans le  rep {}'.format(os.getcwd()))
                self.all_removed_files.append(file)
            elif 'ljob' in file_ext[0]:
                os.remove(file)
                self.all_removed_files.append(file)
            
            
            elif file_ext[1] != ".txt":
                # print(file)
                self.removed_no_txt_extenxion_file.append(file)
                os.remove(file)                     #suppression des fichiers
                self.all_removed_files.append(file)

            else:
                pass 
        content = {
        "Files such as size are zeros bytes, are {} over {}".format(len(self.removed_zero_size_files), len(files)): "Removed files are the followings: \n {}".format(self.removed_zero_size_files),
        "Files such as extension are different to .txt, are {} over {}".format(len(self.removed_no_txt_extenxion_file), len(files)): "Removed files are the followings: \n {}".format(self.removed_no_txt_extenxion_file),
        "All removed Files, are {} over {}".format(len(self.all_removed_files), len(files)): "Removed files are the followings: \n {}".format(self.all_removed_files)
                              }
        return content

    # def afficheResultat(self):
    #     content = {
    #     "Files such as size are zeros bytes, are {} over {}".format(len(self.removed_zero_size_files), len(files)): "Removed files are the followings: \n {}".format(self.removed_zero_size_files),
    #     "Files such as extension are different to .txt, are {} over {}".format(len(self.removed_no_txt_extenxion_file), len(files)): "Removed files are the followings: \n {}".format(self.removed_no_txt_extenxion_file),
    #     "All removed Files, are {} over {}".format(len(self.all_removed_files), len(files)): "Removed files are the followings: \n {}".format(self.all_removed_files)

    #                           }
    #     return content




# ++=================Main===========+++++++
# p = CleanFolder()
# # print(p)

# content = p.cleaning_files()
# print("------  Resultat nettoyage du dossier {} !!!!------".format(p))
# print(content.keys()[0])
# print(content.values()[0])
# print(content.keys()[1])
# print(content.values()[1])
# print(content.keys()[2])
# print(content.values()[2])
# print('------  Dossier nettoye!!!!')








