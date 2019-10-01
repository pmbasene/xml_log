#!/anaconda3/bin/python
import pandas as pd
# from mysql.connector import errorcode
# import mysql.connector
# from mysql.connector import (connection)
# import psycopg2


# # cnx = mysql.connector.connect(user='root',)
# # cnx.close()

# try:
#     connection = psycopg2.connect(user="ganasene",
#                                   host="127.0.0.1",
#                                   port="5432",
#                                   database="mabase")

#     cursor = connection.cursor()
#     # Print PostgreSQL Connection properties
#     print(connection.get_dsn_parameters(), "\n")

#     # Print PostgreSQL version
#     cursor.execute("SELECT version();")
#     record = cursor.fetchone()
#     print("You are connected to - ", record, "\n")

# except (Exception, psycopg2.Error) as error:
#     print("Error while connecting to PostgreSQL", error)
# finally:
#     #closing database connection.
#         if(connection):
#             cursor.close()
#             connection.close()
#             print("PostgreSQL connection is closed")

# # print(dir(psycopg2))


df_path = pd.read_csv("/Users/ganasene/Desktop/resultats_xml/job_path.csv")
df_stage = pd.read_csv("/Users/ganasene/Desktop/resultats_xml/job_stage.csv")

#### path datafrae
# print(df_path.head())
# cols=[col for col in df_stage]
# print(cols)
# rename columns

df_path.rename(columns={"jobName":"jobName_path","logFile":"logFile_path",\
               "recordType":"recordType_path", "projectName":"projectName_path"}, inplace=True)

df_stage.rename(columns={"jobName": "jobName_stage", "logFile": "logFile_stage",
                        "recordType": "recordType_stage", "projectName": "projectName_stage"}, inplace=True)


df_stage.to_json('/Users/ganasene/Desktop/resultats_xml/job_stage.json')
df_path.to_json('/Users/ganasene/Desktop/resultats_xml/job_path.json')

df_path.to_













# # print(len(tuple_Job_logfile_file_trueFile_attr))
# # print(len(tuple1_Job_logfile))


# tuple_Job_logfile_file_trueFile_attr = [
#     ("tableEnfant", "fanzonelog.txt", '#dir#rep#ok.csv','/dir/rep/ok.csv' ,"input"),
#     ("tabParent", "emploilog.txt", '#home#rep#ok', '/home/rep/ok.csv', "input"),
#     ("tabParents", "emploilog.txt", '#home#rep#ok', '/home/rep/ok.csv', "output"),
#     ("tableEcodel", "permilog.txt", '#dir#rep#ok', '/dir/rep/ok.csv', "output"),
#     ("epongAutre", "fanzoneslog.txt", '#home#rep#ok', '/dir/rep/ok.csv', "input"),
#     ("epongAutre", "fanzonelog.txt", '#home#rep#ok', '/dir/rep/ok.csv', "input"),
#     ("Enfant", "fanzonelog.txt", '#dir#deskto#ok', '/dir/rep/ok.txt', "input"),
# ]

# tuple1_Job_logfile_attr = [
#     ("tableEnfant", "fanzonelog.txt","input"),
#     ("tableEnfant", "fanzonelog.txt","input"),
#     ("tableEnfant", "fanzonelog.txt","input"),
#     ("tableEnfant", "fanzonelog.txt","input"),
#     ("tabParent", "emploilog.txt","input"),
#     ("tabParent", "emploilog.txt","input"),
#     ("tabParents", "emploilog.txt","output"),
#     ("tabParents", "emploilog.txt","output"),
#     ("tabParents", "emploilog.txt", "output"),
#     ("tabParents", "emploilog.txt", "output"),
#     ("tableEcodel", "permilog.txt","output"),
#     ("tableEcodel", "permilog.txt","output"),
#     ("tableEcodel", "permilog.txt","output",),
#     ("epongAutre", "fanzoneslog.txt","input"),
#     ("epongAutre", "fanzonelog.txt","input"),
#     ("epongAutre", "fanzonelog.txt","input"),
#     ("epongAutre", "fanzonelog.txt","input"),
#     ("epongAutre", "fanzonelog.txt","input"),
#     ("Enfant", "fanzonelog.txt","input")

# ]
# print(tuple1_Job_logfile_attr)
# print(len(tuple1_Job_logfile_attr))

# print('')

# newTuple =[]
# for h in range(len(tuple_Job_logfile_file_trueFile_attr)):
#     t0 = tuple_Job_logfile_file_trueFile_attr[h][0]
#     t1 = tuple_Job_logfile_file_trueFile_attr[h][1]
#     t4 = tuple_Job_logfile_file_trueFile_attr[h][4]

#     t3= tuple_Job_logfile_file_trueFile_attr[h][3]
#     # print(t0_1_4)
#     t0_1_4 = (t0, t1, t4)
#     for j in tuple1_Job_logfile_attr:
#         if t0_1_4 == j:
#             print(t0_1_4)
#             print(j)
#             newTuple.append(t3)
#         # else:
#         #     newTuple.append("NaN")


#     # print(t0_1)
#     # print(t4)
# print(newTuple)
# print(len(newTuple))
