import requests
import json
import time
import csv

with open('data/all_data/authors_gender.tsv', 'w+') as authors_gender:
    wr = csv.writer(authors_gender, delimiter='\t')

    unique_names = {}
    with open("data/all_data/authors.tsv") as file:
        for i, line in enumerate(file):
            if i == 0: 
                wr.writerow(["doi", "name", "gender", "orcid", "roles", "add", "corr"])
                continue
            if i > 10:
            	break

            lines = line.split("\t")
            names = lines[1].strip().split(" ::: ")
            print names

            first = names[1]; last = names[0]
            print(i, first + " " + last)
            if (first, last) in unique_names.keys():
                new_lines = [lines[0], lines[1], unique_names[(first, last)], lines[2], lines[3], lines[4], lines[5]]
                wr.writerow(new_lines)
                continue
            
            path = "http://abel.lis.illinois.edu/cgi-bin/ethnea/search.py?Fname={0}&Lname={1}&format=json".format(first, last)
            r = requests.get(path)

            text = r.text.strip().replace('\'', '"')
            x = json.loads(text)

            empirical = x[u'Genni']
            print("empirical: {0}".format(empirical))
            unique_names[(first, last)] = empirical

            time.sleep(0.1)

            new_lines = [lines[0], lines[1], empirical, lines[2], lines[3], lines[4], lines[5]]
            wr.writerow(new_lines)