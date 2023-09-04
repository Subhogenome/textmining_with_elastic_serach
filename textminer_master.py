# importing custom modules
from textminer_pubmed import TextMiner as txt
from textminer_pubmed import TextMiner_and as txa
from textminer_pubmed import TextMiner_not as txn
from texminer_clinical import TextMiner_clinical as tco
from texminer_clinical import TextMiner_and_clinical as tca
from texminer_clinical import TextMiner_not_clinical as tcn
#importing modules
import argparse
import os
import pandas as pd
#creating command line based input variables
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', help='Keyword input')
parser.add_argument('-dict', '--dictionary',nargs='*', help='specify the dictionary to be used')
parser.add_argument('-db', '--database', help='pubmed , clinical , clinical_n_pumbed')
parser.add_argument('-q', '--query', help='and or not ')
parser.add_argument('-not', '--na', help='not qury file')
args = parser.parse_args()
finput = str(args.input)
dicinput = str(args.dictionary)
dbinput = str(args.database)
quinput = str(args.query)
nainput = str(args.na)
# specify the directory where in you have the database created
work_dir = "."
# club modules helps in clubming files when you are using multiple dictionaries
def club():
    df=pd.read_csv(work_dir+r"/abstract_mesh_clinical.csv")
    dc=pd.read_csv(work_dir +r"/abstract_mesh.csv")
    df.rename(columns = {'NCTID':'ID'}, inplace = True)
    dc.rename(columns = {'PMID':'ID'}, inplace = True)
    df.rename(columns = {'details':'abstract'}, inplace = True)
    df=pd.concat([df,dc])
    #df=df[df["Database"]=="Database"]
    df.to_csv(work_dir+r"/abstract_mesh.csv",index=False)

    df=pd.read_csv(work_dir+r"/final_output_mesh.csv")
    dc=pd.read_csv(work_dir+r"/final_output_mesh_clinical.csv")
    dc.rename(columns = {'NCTID_x':'ID_x'}, inplace = True)
    dc.rename(columns = {'NCTID_y':'ID_y'}, inplace = True)
    df.rename(columns = {'PMID_x':'ID_x'}, inplace = True)
    df.rename(columns = {'PMID_y':'ID_y'}, inplace = True)

    df=pd.concat([dc,df])
    #df=df[df["Database"]=="Database"]
    df.to_csv(work_dir+r"/final_output_mesh.csv",index=False)
    df=pd.read_csv(work_dir+r"/first_display_clinical.csv")
    dc=pd.read_csv(work_dir+r"/first_display.csv")
    df=pd.concat([dc,df])
    #df=df[df["Database"]=="Database"]
    df.to_csv(work_dir+r"/first_display.csv",index=False)

def club_master():
    try:
     df=pd.read_csv(work_dir+r"/abstract_mesh_clinical.csv")
     df=df[df["Database"]!="Database"]
     df.to_csv(work_dir+r"/abstract_mesh_clinical.csv",index=False)
    except FileNotFoundError:
      df=pd.read_csv(work_dir+r"/abstract_mesh.csv")
      df=df[df["Database"]!="Database"]
      df.to_csv(work_dir+r"/abstract_mesh.csv",index=False)

    
    try:
      df=pd.read_csv(work_dir+r"/final_output_mesh.csv")
      df=df[df["Database"]!="Database"]
      df.to_csv(work_dir+r"/final_output_mesh.csv",index=False)
    except FileNotFoundError:
      df=pd.read_csv(work_dir+r"/final_output_mesh_clinical.csv")
      df=df[df["Database"]!="Database"]
      df.to_csv(work_dir+r"/final_output_mesh_clinical.csv",index=False)
    
    try:
     df=pd.read_csv(work_dir+r"/first_display.csv")
     df=df[df["Database"]!="Database"]
     df.to_csv(work_dir+r"/first_display.csv",index=False)    
    except FileNotFoundError:
     df=pd.read_csv(work_dir+r"/first_display_clinical.csv")
     df=df[df["Database"]!="Database"]
    
     df.to_csv(work_dir+r"/first_display_clinical.csv",index=False)
# master class helps in running different queries as the user provides through a command line
def master_class(finput,dicinput,dbinput,quinput,nainput):
    if quinput == "or" and dbinput == "pubmed":
       db=dbinput
       dict=dicinput
       
       entity= work_dir+r"/database/"+db+r"/"+dict+r"/"+"entity_pmid.csv"
       dic= work_dir+r"/database/"+db+r"/"+dict+r"/"+f"{dict}.csv"
       dir=work_dir+r"/database/"+db+r"/"+dict+r"/"+"entity_count.csv"
       txt.key_words(finput,work_dir)
       txt.common(work_dir+r"/work/pmid_syn.csv",entity,dic,dir,work_dir)
       txt.mesh(work_dir+r"/abstract_mesh.csv",dic,work_dir)
       txt.final_output(work_dir+r"/abstract_mesh.csv",dic,work_dir)
    elif quinput == "and" and dbinput == "pubmed":
       db=dbinput
       dict=dicinput
       
       entity=work_dir+r"/database/"+db+r"/"+dict+r"/"+"entity_pmid.csv"
       dic=work_dir+r"/database/"+db+r"/"+dict+r"/"+f"{dict}.csv"
       dir=work_dir+r"/database/"+db+r"/"+dict+r"/"+"entity_count.csv"
       txa.key_words(finput,work_dir) 
       txa.common(work_dir+r"/work/pmid_syn.csv",entity,dir,dic,work_dir)
       txa.mesh(work_dir+r"/abstract_mesh.csv",dic,work_dir)
       txa.final_output(work_dir+r"/abstract_mesh.csv",dic,work_dir)
    elif quinput == "not" and dbinput == "pubmed": 
       db=dbinput
       dict=dicinput 
       
       entity=work_dir+r"/database/"+db+r"/"+dict+r"/"+"entity_pmid.csv"
       dic=work_dir+r"/database/"+db+r"/"+dict+r"/"+f"{dict}.csv"
       dir=work_dir+r"/database/"+db+r"/"+dict+r"/"+"entity_count.csv"
       txn.key_words(finput,nainput,work_dir)
       txn.common(work_dir+r"/work/pmid_not_syn.csv",entity,dir,dic,work_dir)
       txn.mesh(work_dir+r"/abstract_mesh.csv",dic,work_dir)
       txn.final_output(work_dir+r"/abstract_mesh.csv",dic,work_dir)

    elif quinput == "or" and dbinput == "clinical":
       db=dbinput
       dict=dicinput

       entity=work_dir+r"/database/"+db+r"/"+dict+r"/"+"entity_clinical.csv"
       dic=work_dir+r"/database/"+db+r"/"+dict+r"/"+f"{dict}.csv"
       dir=work_dir+r"/database/"+db+r"/"+dict+r"/"+"entity_count.csv"
       tco.key_words(finput,work_dir)
       try :
        tco.common(work_dir+r"/work/clinical_syn.csv",entity,dic,dir,work_dir)
        tco.mesh(work_dir+r"/abstract_mesh_clinical.csv",dic,work_dir)
        tco.final_output(work_dir+r"/abstract_mesh_clinical.csv",dic,work_dir)
       except (KeyError, ValueError):
           raise Exception("Keyword not found")
    elif quinput == "and" and dbinput == "clinical":
       db=dbinput
       dict=dicinput

       entity=work_dir+r"/database/"+db+r"/"+dict+r"/"+"entity_clinical.csv"
       dic=work_dir+r"/database/"+db+r"/"+dict+r"/"+f"{dict}.csv"
       dir=work_dir+r"/database/"+db+r"/"+dict+r"/"+"entity_count.csv"
       tca.key_words(finput,work_dir)
       try : 
        tca.common(work_dir+r"/work/clinical_syn.csv",entity,dir,dic,work_dir)
        tca.mesh(work_dir+r"/abstract_mesh_clinical.csv",dic,work_dir)
        tca.final_output(work_dir+r"/abstract_mesh_clinical.csv",dic,work_dir)
       except (KeyError, ValueError):
           raise Exception("Keyword not found")
    elif quinput == "not" and dbinput == "clinical":
       db=dbinput
       dict=dicinput

       entity=work_dir+r"/database/"+db+r"/"+dict+r"/"+"entity_clinical.csv"
       dic=work_dir+r"/database/"+db+r"/"+dict+r"/"+f"{dict}.csv"
       dir=work_dir+r"/database/"+db+r"/"+dict+r"/"+"entity_count.csv"
       tcn.key_words(finput,nainput,work_dir)
       try:
        tcn.common(work_dir+r"/work/clinical_not_syn.csv",entity,dir,dic,work_dir)
        tcn.mesh(work_dir+r"/abstract_mesh_clinical.csv",dic,work_dir)
        tcn.final_output(work_dir+r"/abstract_mesh_clinical.csv",dic,work_dir)
       except (KeyError, ValueError):
           raise Exception("Keyword not found")
    elif quinput == "or" and dbinput == "clinical_n_pubmed":
       db="clinical"
       dict=dicinput

       entity=work_dir+r"/database/"+db+r"/"+dict+r"/"+"entity_clinical.csv"
       dic=work_dir+r"/database/"+db+r"/"+dict+r"/"+f"{dict}.csv"
       dir=work_dir+r"/database/"+db+r"/"+dict+r"/"+"entity_count.csv"
       tco.key_words(finput,work_dir)
       try:
        tco.common(work_dir+r"/work/clinical_syn.csv",entity,dic,dir,work_dir)
        tco.mesh(work_dir+r"/abstract_mesh_clinical.csv",dic,work_dir)
        tco.final_output(work_dir+r"/abstract_mesh_clinical.csv",dic,work_dir)
       except (KeyError, ValueError):
           raise Exception("Keyword not found")
       db="pubmed"
       dict=dicinput

       entity=work_dir+r"/database/"+db+r"/"+dict+r"/"+"entity_pmid.csv"
       dic=work_dir+r"/database/"+db+r"/"+dict+r"/"+f"{dict}.csv"
       dir=work_dir+r"/database/"+db+r"/"+dict+r"/"+"entity_count.csv"
       txt.key_words(finput,work_dir)
       txt.common(work_dir+r"/work/pmid_syn.csv",entity,dic,dir,work_dir)
       txt.mesh(work_dir+r"/abstract_mesh.csv",dic,work_dir)
       txt.final_output(work_dir+r"/abstract_mesh.csv",dic,work_dir)
       club()
    elif quinput == "and" and dbinput == "clinical_n_pubmed":
       db="pubmed"
       dict=dicinput

       entity=work_dir+r"/database/"+db+r"/"+dict+r"/"+"entity_pmid.csv"
       dic=work_dir+r"/database/"+db+r"/"+dict+r"/"+f"{dict}.csv"
       dir=work_dir+r"/database/"+db+r"/"+dict+r"/"+"entity_count.csv"
       txa.key_words(finput,work_dir)
       txa.common(work_dir+r"/work/pmid_syn.csv",entity,dir,dic,work_dir)
       txa.mesh(work_dir+r"/abstract_mesh.csv",dic,work_dir)
       txa.final_output(work_dir+r"/abstract_mesh.csv",dic,work_dir)
       db="clinical"
       dict=dicinput

       entity=work_dir+r"/database/"+db+r"/"+dict+r"/"+"entity_clinical.csv"
       dic=work_dir+r"/database/"+db+r"/"+dict+r"/"+f"{dict}.csv"
       dir=work_dir+r"/database/"+db+r"/"+dict+r"/"+"entity_count.csv"
       tca.key_words(finput,work_dir)
       try:
        tca.common(work_dir+r"/work/clinical_syn.csv",entity,dir,dic,work_dir)
        tca.mesh(work_dir+r"/abstract_mesh_clinical.csv",dic,work_dir)
        tca.final_output(work_dir+r"/abstract_mesh_clinical.csv",dic,work_dir)
       except (KeyError, ValueError):
           raise Exception("Keyword not found")
        
       club()
    elif quinput == "not" and dbinput == "clinical_n_pubmed":
       db="pubmed"
       dict=dicinput

       entity=work_dir+r"/database/"+db+r"/"+dict+r"/"+"entity_pmid.csv"
       dic=work_dir+r"/database/"+db+r"/"+dict+r"/"+f"{dict}.csv"
       dir=work_dir+r"/database/"+db+r"/"+dict+r"/"+"entity_count.csv"
       txn.key_words(finput,nainput,work_dir)
       txn.common(work_dir+r"/work/pmid_not_syn.csv",entity,dir,dic,work_dir)
       txn.mesh(work_dir+r"/abstract_mesh.csv",dic,work_dir)
       txn.final_output(work_dir+r"/abstract_mesh.csv",dic,work_dir)

       db="clinical"
       dict=dicinput

       entity=work_dir+r"/database/"+db+r"/"+dict+r"/"+"entity_clinical.csv"
       dic=work_dir+r"/database/"+db+r"/"+dict+r"/"+f"{dict}.csv"
       dir=work_dir+r"/database/"+db+r"/"+dict+r"/"+"entity_count.csv"
       tcn.key_words(finput,nainput,work_dir)
       try:
        tcn.common(work_dir+r"/work/clinical_not_syn.csv",entity,dir,dic,work_dir)
        tcn.mesh(work_dir+r"/abstract_mesh_clinical.csv",dic,work_dir)
        tcn.final_output(work_dir+r"/abstract_mesh_clinical.csv",dic,work_dir)
        tca.final_output(work_dir+r"/abstract_mesh_clinical.csv",dic,work_dir)
       except (KeyError, ValueError):
           raise Exception("Keyword not found")
       club()
    

#def joined(dbinput):
 #   cmd= f"awk 'FNR==1 && NR!=1{next;}{print}' *abstract*.csv > abstract_{dbinput}.csv"
  #  os.system(cmd)
   # cmd= f"awk 'FNR==1 && NR!=1{next;}{print}' *first_display*.csv > first_display_{dbinput}.csv"
    #os.system(cmd)
    #cmd= f"awk 'FNR==1 && NR!=1{next;}{print}' *final_output*.csv > final_output_{dbinput}.csv"
    #os.system(cmd)
def listToString(s):
   
    # initialize an empty string
    str1 = " "
   
    # return string 
    return (str1.join(s))
            



def remove_files(files):
     with open(files,'r+') as file:
         file.truncate(0)
            
output= ["abstract_mesh_clinical.csv","final_output_mesh.csv","final_output_mesh_clinical.csv","abstract_mesh.csv","first_display_clinical.csv","final_output_mesh_Clinical.csv","first_display.csv"]
# master function takes in the variables from command line and pass it on the master_class function which further runs different querries
def master(finput,dicinput,dbinput,quinput,nainput):
  for i in output:
       if os.path.exists(i):
                 os.remove(i)


  
  dicinput=dicinput.split()
  print(dbinput)
  for i in dicinput:
      a=i.strip("[]")
      d=a.strip("'")
      d=d.replace("'", "")
      d=d.strip(",")
      
      
      master_class(finput,d,dbinput,quinput,nainput)
     # club_master()

if __name__ == "__main__":
    master(finput,dicinput,dbinput,quinput,nainput)
