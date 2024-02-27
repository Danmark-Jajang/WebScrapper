import csv

def save_to_file(file_name, jobs):
    file = open(f"{file_name}.csv","w")
    w = csv.writer(file)
    w.writerow(["title","company","lang","link"])

    for job in jobs:
        w.writerow(job.values())

    file.close()