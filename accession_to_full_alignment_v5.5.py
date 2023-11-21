#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 13:15:20 2022

@author: kendra
"""

##KZ 12_22_22 
#script to take in a csv with columns "Taxon" which should have genus_species 
# and "Accession" which should have the accession of the mito genome


#Things you need:
from Bio import Entrez, SeqIO
import csv
import os
from Bio.Seq import translate
import itertools
import argparse
#make sure you have the command line version of mega downloaded!
#https://www.megasoftware.net/ select "cc" instead of gui.
#The file structure for this is simple. You need a folder that is empty other than your .csv file reeferenced in lines 10-11.
#as well as the .mao file

#NOTE if you have gb files that are not on ncbi that you want included in the pipeline,
#make a folder in the working directory named group_name_gb and add them there.
#files should be named species_genus.gb
##ALSO if you want to inlcude fasta files that are not downloaded from ncbi, crate a folder in the same directory named "fastas" and put them there.
#make sure the files are named "animal_name.fa" and the genes are named "cox1" for example.

#You do need internet to run this since it is downloading from NCBI. 
#only works for vertebrate mitochondrial code rn

#If you just need to rerun the script to adjust some alignments or naming, go ahead and change the answer for
#the prior steps to "no".

##########
#Change email, group_name, and working_dir. Keep Yes for everything if this is the first run.
##########



parser = argparse.ArgumentParser(
    description=""""Oh......... your'e using this thing. It's supposed to take in a csv with columns 
    'Taxon' and 'Accession' and return a concatenated alignment of the 13 mito genes.
    NOTE if you have gb OR fasta files that are not on ncbi that you want included in the pipeline
    make a folder in the working directory named group_name_gb and add them there.
    make sure the files are named "animal_name.fa" and the genes are named "cox1" for example.

    You do need internet to run this since it is downloading from NCBI. 

    If you just need to rerun the script to adjust some alignments or naming, go ahead and change the answer for
    the prior steps to "no".""",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-e", "--email", help="NCBI wants your data!!")
parser.add_argument("-g", "--group_name",default=os.path.basename(os.getcwd()).split("_")[0],help="Cats?Rats? idk whatevers in there. ")
parser.add_argument("-b", "--gb_file_dwnld",default="no",help="Put no here unless you really  need to download the files for the first time or redownload them. NCBI wont like all the requests if you keep doing it over and over")
parser.add_argument("-v", "--vert_status",default="vert",help="do they have a backbone? Can they stand up for themselves? vert or invert")
parser.add_argument("-f", "--gene_files",default="yes",help="Do you want to remake the unaligned gene files again?")
parser.add_argument("-a", "--align_genes",default="yes",help="Do you want to remake the aligned gene files again?")
parser.add_argument("-x", "--excluded_genes",default="yes",nargs="*",help="Any genes you don't want? name them like 'cox2'")
parser.add_argument("-d", "--local_files",default="no",help="Do you plan to add any local files? (.gb or .fa works)'")

args = vars(parser.parse_args())


#They want to steal your personal info.
Entrez.email = args['email']


#What is this group of animals? cats? rats? bats? worms? can be whatever makes sense to you
group_name = args['group_name']


#working directory. This pipeline will make all the new folders youll need. Make sure your csv
#with the accessions is in this folder
working_dir = os. getcwd() + "/"

#Do you need to download gb files? yes or no also wont download them.
gb_files_download = args['gb_file_dwnld']

#vert or invert
vert_status =args['vert_status'] #or vert

#make gene files?
gene_file_make=args["gene_files"]

#align individual genes?
gene_align=args['align_genes']

#Any mito genes you want to exclude?
mito_genes_exclude = args['excluded_genes']

#Add local files?
add_local_files = args["local_files"]

############
#shouldnt need to enter anything below this
############
extended_output_file = open("output_extended.txt","w")



if add_local_files == "yes":
    if group_name+"_gb" not in os.listdir(working_dir):
        os.mkdir(working_dir+group_name+"_gb")

    input_message = """\n\nOhhhh you want to add local files? 
Great! Just make sure they are in .gb or .fa format!
Also, gb files with features should have the genes as gene feature types be named like "ATP6" for example.
Fasta files just need to have the gene abbreviation somewhere in their name or description. >ATP6 or >rat_atp6 works!
Go ahead and put them in the folder,""" +group_name+"_gb. Type something once you're ready:" 
    type_something = input(input_message)
    print(type_something)



vert_mao = """; Please do not edit this file! If this file is modified, results are unpredictable.
; Instead of modifying this file, simply create a new MEGA Analysis Options file by using MEGA.
[ MEGAinfo ]
ver                               = 10200331-x86_64 macOS            
[ DataSettings ]
datatype                          = snNucleotide                     
containsCodingNuc                 = True                             
missingBaseSymbol                 = ?                                
identicalBaseSymbol               = .                                
gapSymbol                         = -                                
[ ProcessTypes ]
ppAlign                           = true                             
ppMuscle                          = true                             
[ AnalysisSettings ]
Gap Penalties                     = ====================             
Gap Open                          = -2.90                            
Gap Extend                        = 0.00                             
Hydrophobicity Multiplier         = 1.20                             
Memory/Iterations                 = ====================             
Max Memory in MB                  = 2048                             
Max Iterations                    = 16                               
Advanced Options                  = ====================             
Genetic Code                      = Vertebrate Mitochondrial         
Cluster Method (Iterations 1,2)   = UPGMA                            
Cluster Method (Other Iterations) = UPGMA                            
Min Diag Length (Lambda)          = 24                               
GeneticCodeTable                  = FFLLSSSSYY**CCWWLLLLPPPPHHQQRRRRIIMMTTTTNNKKSS**VVVVAAAADDEEGGGG"""

invert_mao = """; Please do not edit this file! If this file is modified, results are unpredictable.
; Instead of modifying this file, simply create a new MEGA Analysis Options file by using MEGA.
[ MEGAinfo ]
ver                               = 10200331-x86_64 macOS            
[ DataSettings ]
datatype                          = snNucleotide                     
containsCodingNuc                 = True                             
missingBaseSymbol                 = ?                                
identicalBaseSymbol               = .                                
gapSymbol                         = -                                
[ ProcessTypes ]
ppAlign                           = true                             
ppMuscle                          = true                             
[ AnalysisSettings ]
Gap Penalties                     = ====================             
Gap Open                          = -2.90                            
Gap Extend                        = 0.00                             
Hydrophobicity Multiplier         = 1.20                             
Memory/Iterations                 = ====================             
Max Memory in MB                  = 2048                             
Max Iterations                    = 16                               
Advanced Options                  = ====================             
Genetic Code                      = Invertebrate Mitochondrial       
Cluster Method (Iterations 1,2)   = UPGMA                            
Cluster Method (Other Iterations) = UPGMA                            
Min Diag Length (Lambda)          = 24                               
GeneticCodeTable                  = FFLLSSSSYY**CCWWLLLLPPPPHHQQRRRRIIMMTTTTNNKKSSSSVVVVAAAADDEEGGGG"""



if "muscle_align_coding_vert_mito.mao" not in os.listdir(working_dir) and vert_status == "vert":
    file_open = open(working_dir+"muscle_align_coding_vert_mito.mao","w")
    file_open.write(vert_mao)
    file_open.close()
    
    
if "muscle_align_coding_invert_mito.mao" not in os.listdir(working_dir)and vert_status == "invert":
    file_open = open(working_dir+"muscle_align_coding_invert_mito.mao","w")
    file_open.write(invert_mao)
    file_open.close()

#If you need to download gb files then do that first
csv_species = []
if gb_files_download == "yes":
    print("\n\nDownloading your gb files\n\n")
    for file in os.listdir(working_dir):
        #only open if csv file
        if file[-4:]==".csv":
            #if you already make a folder with some gb files in it then the folder doesnt need to be made.
            if group_name+"_gb" not in os.listdir(working_dir):
                os.mkdir(working_dir+group_name+"_gb")
            with open(working_dir+file) as accession_csv_file: #opens csv file
                csv_reader = csv.reader(accession_csv_file, delimiter=',')
                next(csv_reader) #skips header
                for row in csv_reader:
                    record_file = open(working_dir+group_name+"_gb/"+row[0]+'.gb', 'w') #writes gb file for each line
                    csv_species.append(row[0])
                    handle = Entrez.efetch(db="nucleotide", id=row[1], rettype="gb", retmode="text") #fetches from ncbi
                    record = handle.read()
                    record_file.write(record.rstrip('\n')) #writes file
elif gb_files_download.lower() == "no" or "nugget" in gene_file_make.lower():
    print("Skipping downnloading gb files.")
else:
    print("Input yes or no")
                   
    
                    
#starts with gb files
mito_genes = ["ND1","ND2","ND3","ND4","ND4L","ND5","ND6","CYTB","COX1","COX2","COX3","ATP6","ATP8"]
#remove genes you may not want to include
for gene in mito_genes_exclude:
    if gene in mito_genes:
        mito_genes.remove(gene)
    
if vert_status  == "vert":
    coding_table=2
elif vert_status == "invert":
    coding_table = 5
    
    
    
named_mito_genes = []
    
class NamedMitoGene:
    def __init__(self,species,gene_name,gene_seq,gene_location):
        self.species = species
        self.name =gene_name
        self.seq = gene_seq
        self.location = gene_location
    def __str__(self):
        return self.name + "\n" + self.seq
    

    
def parse_mito_genes(path,file):
    extension = file.split(".")[-1]
    species = file[:-3]
    #parsing from gb file features
    if extension=="gb" or extension == "genbank":
        for gb_record in SeqIO.parse(open(path+file,"r"), "genbank"):
            if len(gb_record.features) <2:
                print(gb_record.name + "may not be annotated!")
            for feature in gb_record.features:
                if feature.type=="gene":
                    if 'note' in dict(feature.qualifiers).keys() and len(dict(feature.qualifiers)['note'])<10 and 'gene' not in dict(feature.qualifiers).keys():
                        gene_name = dict(feature.qualifiers)['note'][0]
                    else:
                        gene_name = str(list(feature.qualifiers.values())[0][0])
                    gene_location = feature.location
                    gene_seq = feature.extract(gb_record).seq
                    named_mito_gene = NamedMitoGene(species, gene_name,gene_seq, gene_location)
                    named_mito_genes.append(named_mito_gene)
                
    #parsing from fasta records    
    elif extension == "fa" or extension == "fasta":
        sequences = SeqIO.parse(path+file, "fasta")
        for record in sequences:
            gene_name = record.name
            gene_description = record.description
            for gene in mito_genes:
                if gene in gene_name.upper() or gene in gene_description.upper():
                    gene_name = gene
            gene_seq = record.seq
            named_mito_gene = NamedMitoGene(species, gene_name,gene_seq, gene_location)
            named_mito_genes.append(named_mito_gene)
  
    
def tweak_mito_gene(named_gene):
    named_gene.name = named_gene.name.upper()     #uppercaseing everything to avoid confusion
    #correcting some common cox gene misnaming
    if named_gene.name == "COI" or named_gene.name == "COXI" or named_gene.name == "CO1":
        named_gene.name = "COX1"
    if named_gene.name == "COII" or named_gene.name == "COXII"or named_gene.name == "CO2":
        named_gene.name = "COX2"
    if named_gene.name == "COIII" or named_gene.name == "COXIII"or named_gene.name == "CO3":
        named_gene.name = "COX3"  
        
    if named_gene.name == "NAD1" or named_gene.name == "NAD1"or named_gene.name == "NAD1":
        named_gene.name = "ND1"  
    if named_gene.name == "NAD2" or named_gene.name == "NAD2"or named_gene.name == "NAD2":
        named_gene.name = "ND2"  
    if named_gene.name == "NAD3" or named_gene.name == "NAD3"or named_gene.name == "NAD3":
        named_gene.name = "ND3"  
    if named_gene.name == "NAD4" or named_gene.name == "NAD4"or named_gene.name == "NAD4":
        named_gene.name = "ND4"  
    if named_gene.name == "NAD4L" or named_gene.name == "NAD4L"or named_gene.name == "NAD4L":
        named_gene.name = "ND4L"  
    if named_gene.name == "NAD5" or named_gene.name == "NAD5"or named_gene.name == "NAD5":
        named_gene.name = "ND5"  
    if named_gene.name == "NAD6" or named_gene.name == "NAD6"or named_gene.name == "NAD6":
        named_gene.name = "ND6"  
    if named_gene.name == "COB" or named_gene.name == "COB"or named_gene.name == "COB":
        named_gene.name = "CYTB"  
        
    named_gene.seq = str(named_gene.seq)
    if len(named_gene.seq) % 3 != 0 and named_gene.name in mito_genes:
        extended_output_file.write("\n"+named_gene.species +" "+ named_gene.name +" had to be trimmed! Was not divisible  by three.")
        named_gene.seq =  named_gene.seq[:len(named_gene.seq)%3*-1]
        
    translated_seq = str(translate(named_gene.seq,table=coding_table))
    if translated_seq[:-1].count("*") >0  and named_gene.name in mito_genes: #lets you know about internal stop codons
#        extended_output_file.write("\ninternal stop codon in "+named_gene.name+" "+named_gene.species+"\n")
         stop_count_f1 = translated_seq[:-1].find("*")
         extended_output_file.write("\nTrying other frames for "+named_gene.name+" "+named_gene.species+"\n")
         translated_seq_f2 = str(translate(named_gene.seq[1:],table=coding_table))
         stop_count_f2 = translated_seq_f2[:-1].find("*")
         translated_seq_f3 = str(translate(named_gene.seq[2:],table=coding_table))
         stop_count_f3 = translated_seq_f3[:-1].find("*")
         
         if stop_count_f2 == -1:
             named_gene.seq =named_gene.seq[1:(stop_count_f2*3)-2]
             extended_output_file.write(named_gene.name+" "+named_gene.species+"Stop codon in frame 1. Added Frame 2\n")
         elif stop_count_f3 == -1:
             named_gene.seq = named_gene.seq[2:(stop_count_f3*3)-1]
             extended_output_file.write(named_gene.name+" "+named_gene.species+"Stop codon in frame 1. Added Frame 3\n")     

         elif stop_count_f1 >= stop_count_f2 and stop_count_f1 >= stop_count_f3:
            named_gene.seq =named_gene.seq[0:stop_count_f1*3]
            extended_output_file.write(named_gene.name+" "+named_gene.species+" Cut off at "+ str(stop_count_f1*3)+" due to internal stop codons. Added Frame 1\n")
         elif stop_count_f2 >= stop_count_f1 and stop_count_f2 >= stop_count_f3:
            named_gene.seq =named_gene.seq[1:(stop_count_f2*3)-2]
            extended_output_file.write(named_gene.name+" "+named_gene.species+" Cut off at "+ str(stop_count_f2*3)+" due to internal stop codons. Added Frame 2\n")
         elif stop_count_f3 >= stop_count_f2 and stop_count_f3 >= stop_count_f1:
            named_gene.seq = named_gene.seq[2:(stop_count_f3*3)-1]
            extended_output_file.write(named_gene.name+" "+named_gene.species+" Cut off at "+ str(stop_count_f3*3)+" due to internal stop codons. Added Frame 3\n")

    
    if translated_seq[-1] =="*": #removes stop codons if they are at the end of the alignment
        named_gene.seq =  named_gene.seq[:-3]
    gene_index = 0
    for letter in named_gene.seq:
        if letter.upper() not in "ATGC-" and gene_index % 3==0:
            named_gene.seq = named_gene.seq[:gene_index]+"---"+named_gene.seq[gene_index+3:]
        if letter.upper() not in "ATGC-" and gene_index % 3==1:
            named_gene.seq = named_gene.seq[:gene_index-1]+"---"+named_gene.seq[gene_index+2:]
        if letter.upper() not in "ATGC-" and gene_index % 3==2 and gene_index < len(named_gene.seq):
            named_gene.seq = named_gene.seq[:gene_index-2]+"---"+named_gene.seq[gene_index+1:]
        gene_index+=1
            
            
    return named_gene
        
gene_order = []

if gene_file_make=="yes":
    gene_order_sub = []
    
    print("\n\nMaking your gene files\n\n")
    os.mkdir(working_dir+group_name+"_genes")
    for file in os.listdir(working_dir+group_name+"_gb/"):
        parse_mito_genes(working_dir+group_name+"_gb/",file)
    
    for named_gene in named_mito_genes:
        named_gene = tweak_mito_gene(named_gene)
    
    
    for named_gene in named_mito_genes: 
        if named_gene.name in mito_genes:
            gene_order_sub.append(named_gene.name)
        gene_order.append(gene_order_sub)
        write_file = open(working_dir+group_name+"_genes/"+named_gene.name+".fa","a")
        write_file.write(">"+named_gene.species+"\n"+named_gene.seq+"\n")
        write_file.close() 
    
    gene_species_combinations_total = itertools.product([named_gene.species for named_gene in named_mito_genes],mito_genes)
    gene_species_combinations_present = [(named_gene.species,named_gene.name) for named_gene in named_mito_genes]
    missing_genes = list(set(gene_species_combinations_total).difference(gene_species_combinations_present))
    for missing_gene in missing_genes:
        missing_gene_message = "Oh no... "+ str(missing_gene)+" was not present! Would you like to add it here? Paste the gene sequence if you do and just type 'no' if not."
        type_missing_gene = input(missing_gene_message)
        if len(type_missing_gene) >10:
            write_file = open(working_dir+group_name+"_genes/"+missing_gene[1]+".fa","a")
            write_file.write(">"+missing_gene[0]+"\n"+type_missing_gene+"\n")
            write_file.close() 
        else:
            print("Ok. I left the gene out. It will appear as dashes (-) in the final alignment.")
#        print(str(missing_gene) + "was not present!!") 
    
    
    
    


    
    
elif gene_file_make.lower() == "no" or "nugget" in gene_file_make.lower():
    print("Skipping creating gene files")
else:
    print("Input yes or no ")

  


#This uses command line mega to generate all your alignments
if gene_align =="yes":    
    print("\n\nAligning your gene files with Mega")
    os.mkdir(working_dir+group_name+"_genes_aligned")
    if vert_status == "vert":
        for mito_gene in mito_genes:
            os.system("megacc -a "+working_dir+"muscle_align_coding_vert_mito.mao -d "+working_dir+group_name+"_genes/"+mito_gene+".fa -o "+working_dir+group_name+"_genes_aligned/"+mito_gene+"_aligned.fa"+" -f fasta >/dev/null 2>&1")
    elif vert_status == "invert":
        for mito_gene in mito_genes:
            os.system("megacc -a "+working_dir+"muscle_align_coding_invert_mito.mao -d "+working_dir+group_name+"_genes/"+mito_gene+".fa -o "+working_dir+group_name+"_genes_aligned/"+mito_gene+"_aligned.fa"+" -f fasta >/dev/null 2>&1")
    else:
        print("You didn't say vert or invert.")
      
elif gene_align.lower() == "no" or "nugget" in gene_file_make.lower():
    print("Skipping creating gene alignment")
else:
    print("Input yes or no.")




#2023_10_18_new_feature: gets gene order:
    
    

    


#concats
gene_set = set()
animal_set = set()
seq_dict = {}
gene_len_dict = {}





#first loop for getting all genes and animals to check if everything looks ok and to get the sets.
#will crash if not complete
for mito_gene in mito_genes:
    fasta_parsed = SeqIO.parse(working_dir+group_name+"_genes_aligned/"+mito_gene+"_aligned.fasta","fasta")
    for gene in fasta_parsed:
        gene_name = mito_gene
        animal_name = "_".join(gene.description.split(" "))
        gene_set.add(gene_name)
        animal_set.add(animal_name)
        seq_dict[gene_name+"_"+animal_name]=str(gene.seq)
        gene_len_dict[gene_name]=len(seq_dict[gene_name+"_"+animal_name])





gene_order_file_open = open(working_dir+group_name+"_gene_order.txt","w")


all_gene_orders = []

for animal in animal_set:
    genes = []
    gene_starts = []
    gene_strands = []
    for gene in gene_set:
        for named_gene in named_mito_genes:
            if named_gene.species.replace(" ","_") == animal and named_gene.name == gene:
                genes.append(named_gene.name)
                gene_starts.append(int(named_gene.location.start))
                gene_strands.append(str(named_gene.location.strand))
                gene_order_file_open.write(animal + "\t"+ gene+"\t"+ str(named_gene.location.start) +"\t" +str(named_gene.location.strand)+"\n")
  

    

        

#make directory and concatenated file
print("\n\nConcatenating!!! Almost there\n\n")
os.mkdir(working_dir+group_name+"_genes_concat")
file_open = open(working_dir+group_name+"_genes_concat/"+group_name+"_concat.fa","w")
#writes concated file
for animal in animal_set:
    file_open.write(">"+animal+"\n")
    for gene in gene_order[0][0:13]: #temp fix
        if gene+"_"+animal in seq_dict.keys():
            file_open.write(seq_dict[gene+"_"+animal])
        else:
            file_open.write("-"*gene_len_dict[gene])
    file_open.write("\n")
start = 1


file_open_gene_order = open(working_dir+"/"+group_name+"_gene_order.fa","w")

for sub_gene_order in gene_order:
    file_open_gene_order.write(str(sub_gene_order[0:13]))

for gene in gene_order[0][0:13]:
    print(gene +" is "+str(start)+" to "+ str(gene_len_dict[gene]+start-1)+" in final alignment.")
    start = gene_len_dict[gene]+start
                    
file_open.close()
extended_output_file.close()

print("Done!!")


                    
                    