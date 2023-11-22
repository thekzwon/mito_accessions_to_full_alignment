# mito_accessions_to_full_alignment
Script that takes accession numbers to mitogenomes as inputs and outputs concatenated alignments of the protein-coding mitochondrial genes.

#Readme file for accession to full alignment v4 script.
#Created by: Kendra Zwonitzer
#Contact: zwonitz2@utexas.edu

Overview:
This script is intended to generate a concatenated alignment file for all 13 protein-coding genes in animal mitogenomes. The script also returns the alignments for each of the individual genes, as well as the unaligned genes. The required input is either 1) a csv file with 'Taxon' and 'Accession' column headers. Note that all accession should be screened for completion and annotation. 2) genbank files of all the mitogenomes. 3) fasta files of all the mitochondrial protein coding genes per species. These three options can also be mixed if you have some genbanks, some fastas, and wish to download some using the script. 

The script works by first extracting the gene sequences from either fasta files or an annotated genbank files. 
Fasta files need to be one per species and formatted as such (gene order does not matter):

"""
>cox1
gactatgcag....
>cox2
gactatgcag....
"""
It then checks for any issues with the gene such as whether it needs to be trimmed because it is not a mulitple of 3 or whether there was a frameshift issue with the annotation. If this is the case, it automatically corrects this. Stop codons are also removed from the final alignment. 
Each of the 13 genes are then aligned using mega using translational align. More details can be seen in the .mao file of the output.
Finally, each of the 13 genes are concatenated into one big alignment.


Requirements:
-Python3(Packages Entrez and SeqIO from Bio, csv, os, translate from Bio.Seq, itertools, and argparse)
-installation of megacc (https://www.megasoftware.net/). This script generates commands that use megacc.


Usage:

accession_to_full_alignment_v4.0.py [-h] [-e EMAIL] [-g GROUP_NAME] [-b GB_FILE_DWNLD] [-v VERT_STATUS] [-f GENE_FILES] [-a ALIGN_GENES] [-x [EXCLUDED_GENES ...]] [-d LOCAL_FILES]

options:
  -h, --help            show this help message and exit
  -e EMAIL, --email EMAIL
                        NCBI wants your data!! (default: None)
  -g GROUP_NAME, --group_name GROUP_NAME
                        Cats?Rats? idk whatevers in there. (default: Parent folder)
  -b GB_FILE_DWNLD, --gb_file_dwnld GB_FILE_DWNLD
                        Put no here unless you really need to download the files for the first time or redownload them. NCBI wont
                        like all the requests if you keep doing it over and over (default: no)
  -v VERT_STATUS, --vert_status VERT_STATUS
                        do they have a backbone? Can they stand up for themselves? vert or invert (default: vert)
  -f GENE_FILES, --gene_files GENE_FILES
                        Do you want to remake the unaligned gene files again? (default: yes)
  -a ALIGN_GENES, --align_genes ALIGN_GENES
                        Do you want to remake the aligned gene files again? (default: yes)
  -x [EXCLUDED_GENES ...], --excluded_genes [EXCLUDED_GENES ...]
                        Any genes you don't want? name them like 'cox2' (default: yes)
  -d LOCAL_FILES, --local_files LOCAL_FILES
                        Do you plan to add any local files? (.gb or .fa works)' (default: no)



Examples:
The folder 'Sturnidae' under 'Examples' has a sample csv formatted file. 'Sturnidae_output' has what a successful run output looks like.

Here is what I used to generate the output:

accession_to_full_alignment_v4.0.py -b yes -e YOUREMAIL@XX.XX

'-b yes' means that I want to download the files in the csv file. I did not put a group name because my parent folder was already named "Sturnidae". 
These are vertebrates, so I left the default for -v. If they were invertebrates, I would have needed to add '-v invert' (currently all I have is those two options. I hope to add more soon). '-f' and '-a' are used if you are rerunning a big batch of files and didn't want to have to redo all of the steps. So you could say '-b no -f no' to just realign the genes if you noticed an error or a missing gene in a file and wanted to manually add it. Not all animals have 13 genes, so you could use -x to exclude genes.

If you had wanted to add local files, run this: accession_to_full_alignment_v4.0.py -b yes -e YOUREAIL@XX.XX -d

The script will generate a folder for you to add your files in (either in gb or fa format) and then you can confirm you are ready to continue.

If you are missing a gene in one of your files, the script will pause and give you the option to add it manually or to continue without that gene.

Here is the terminal feedback I got from running "accession_to_full_alignment_v4.0.py -b yes -e YOUREMAIL@XX.XX":

"""
Downloading your gb files




Making your gene files


/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/Bio/Seq.py:2804: BiopythonWarning: Partial codon, len(sequence) not a multiple of three. Explicitly trim the sequence or add trailing N before translation. This may become an error in future.
  warnings.warn(


Aligning your gene files with Mega


Concatenating!!! Almost there


ND4 is 1 to 1377 in final alignment.
COX3 is 1378 to 2160 in final alignment.
ATP8 is 2161 to 2325 in final alignment.
ATP6 is 2326 to 3006 in final alignment.
COX1 is 3007 to 4563 in final alignment.
COX2 is 4564 to 5244 in final alignment.
ND5 is 5245 to 7059 in final alignment.
ND4L is 7060 to 7353 in final alignment.
ND2 is 7354 to 8391 in final alignment.
ND6 is 8392 to 8907 in final alignment.
CYTB is 8908 to 10047 in final alignment.
ND3 is 10048 to 10395 in final alignment.
ND1 is 10396 to 11370 in final alignment.
Done!!
"""


The output has a .mao file which is used for the mega alignments. It tells mega what to run. 
It also has an output_extended file, which gives information on any genes that had to be frame corrected or trimmed. 
Sturnidae_gb has all the downloaded genbank files.
Sturnidae_genes has all the extracted genes from these files.
Sturnidae_genes_aligned has each gene individually aligned.
Sturnidae_genes_concat is the concatenated alignment.





