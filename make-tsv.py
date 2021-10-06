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
attachment_file = "./experimentA/idr0114-experimentA-filePaths.tsv"
duplicate_names = ['3DView.avi', '3DView.jpg']

def process_line(line, count, match, rows):
    parts = line.split('	')
    path = parts[1]
    split_path = path.split('/')
    image_name = split_path[len(split_path)-1]
    image_names.append(image_name)
    paths.append(path)
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
        (image_names,paths) = process_line(line, count, 0, rows)
        line = fp.readline().strip()

count3 = 0
for path in paths:
    count3 += 1
    with open(annot_file) as ap:
        line = ap.readline().strip()
        count2 = 0
        bits = path.split('/')
        lenght = len(bits)
        image_name = bits[lenght - 1]
        dupe = False
        if image_name in duplicate_names:
            dupe = True
            image_name = bits[lenght-2]+'\\'+ image_name
        while line and len(line) > 0:
            count2 += 1
            dataset_name = line.split('	')[0]
            if image_name in line:
                rows.append(['Project:name:idr0114-lindsay-hdbr/experimentA/Dataset:name:'+dataset_name, path])
                break
            line = ap.readline().strip()
print([item for item, count in collections.Counter(image_names).items() if count > 1])
write_tsv(rows)

