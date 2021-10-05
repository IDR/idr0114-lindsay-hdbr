#!/usr/bin/env python

# This has to run as user omero-server.
# Assumes that omero-upload was installed on the server.
# git clone https://gitlab.com/idr/idr0082-pennycuick-lesions.git
# cd idr0082....
# cp attachments.txt /tmp
# cp upload_attachments.py /tmp
# chmod +x /tmp/upload_attachments.py
# sudo su omero-server
# cd /tmp
# . /opt/omero/server/venv3/bin/activate
# python upload_attachments.py

import csv
import collections

rows = []
image_names = []
paths =[]
match = 0
full_match = 0
match_count = 0
no_match_count = 0
repeat_check = ""
annot_file = "./experimentA/from_annot_im_and_dat.tsv"
attachment_file = "./experimentA/idr0114-experimentA-filePaths.tsv"    # "/tmp/attachments.txt"
dataset_names = ["C127_H4K5ac", "C127_H3K36me2", "C127_RNAP-S2P", "C127_H3K4me2",
                 "C127_H3K27me3", "C127_H3K9me2", "C127_SAF-A", "C127_Smc3", "C127_CTCF", "C127_Macro-H2A", 
                 "C127_H3K4me3", "C127_aHP1", "C127_Scc1", "C127_SCC1","C127_H3K36me3", "C127_H4K20me1",
                 "C127_30min-BrUTP", "C127_H3K9me3", "C127_H4K20me3", "C127_hnRNP", "HeLa_Rad21",
                 "HeLa_H3K4me3", "HeLa_H3K9me3", "HeLa_H3K27me3", "HeLa_hnRNPC", "HeLa_RNAP-S2P", "HeLa_Scc1", "HeLa_RNAPIIS2P"]

def process_line(line, count, match, rows):
    # /uod/idr/filesets/idr0082-pennycuick-lesions/20200417-ftp/S1_HandE.ndpi.ndpa
    # /uod/idr/filesets/idr0082-pennycuick-lesions/20200417-ftp/S2_HandE.ndpi.ndpa
    parts = line.split('	')
    path = parts[1]
    split_path = path.split('/')
    image_name = split_path[len(split_path)-1]
    image_names.append(image_name)
    paths.append(path)
    #image_names.append(image_name)
    return image_names,paths

def write_tsv(rows):
    with open('experimentA/test.tsv', mode='w') as tsv_file:
        tsv_writer = csv.writer(tsv_file, delimiter='\t')
        tsv_writer.writerows(rows)

with open(attachment_file) as fp:
    line = fp.readline().strip()
    count = 0
    while line and len(line) > 0:
        count += 1

        #print("Line %d" % count)
        #print (line)
        (image_names,paths) = process_line(line, count, 0, rows)
        line = fp.readline().strip()
#print ("match_count")
#print (match_count)
#print ("no match_count")
#print (no_match_count)

count3 = 0
for path in paths:
    #print(image_name)
    count3 += 1
    with open(annot_file) as ap:
        line = ap.readline().strip()
        count2 = 0
        bits = path.split('/')
        lenght = len(bits)
        image_name = bits[lenght - 1]
        while line and len(line) > 0:
            count2 += 1
            dataset_name = line.split('	')[0]
            print ("dataset name")
            print (dataset_name)
            if image_name in line:
                print(count3)
                print(image_name)
                print(count2)
                print(line)
                print("match")
                rows.append(['Project:name:idr0114-lindsay-hdbr/experimentA/Dataset:name:'+dataset_name, path])
                break
            line = ap.readline().strip()
print([item for item, count in collections.Counter(image_names).items() if count > 1])
write_tsv(rows)

