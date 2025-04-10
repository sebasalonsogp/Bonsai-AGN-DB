#!/home/jack/.pyenv/versions/3.9.5/bin/python
import os
import argparse
import subprocess

# 1.) Get command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("rowData")
parser.add_argument("sedName")
parser.add_argument("pathFile")
args = parser.parse_args()

# 2.) run create_cigale_cat.py
os.chdir("/home/data/blackbase/scripts/Alex")
subprocess.run(f"/home/data/blackbase/scripts/Alex/create_cigale_cat.py --row_data=\"{args.rowData}\" --image_path=\"{args.sedName}\"", shell=True)

# 3.) Use pcigale.ini file as template and replace "DATA_FILE_HERE"
template_path = "/home/data/blackbase/cigale-v2022.0/pcigale_template.ini"
pcigale_file_folder = "/".join(template_path.split("/")[:-1]) + f"/inis/{args.sedName}"
os.makedirs(pcigale_file_folder, exist_ok=True)

subprocess.run(f"cp /home/data/blackbase/cigale-v2022.0/pcigale_template.ini.spec {pcigale_file_folder}/pcigale.ini.spec", shell=True)

with open(template_path) as f:
	text = f.read()

#ini_path = f"{pcigale_file_folder}/{args.sedName}.ini"
ini_path = f"{pcigale_file_folder}/pcigale.ini"
with open(ini_path, "w") as f:
	f.write(text.replace("DATA_FILE_HERE", f"data_file = /home/data/blackbase/scripts/Alex/{args.sedName}.txt"))


# 4.) Run "pcigale"
os.chdir(pcigale_file_folder)
subprocess.run(f"/home/jack/.pyenv/versions/3.9.5/bin/pcigale run", shell=True)

# 5.) Run "pcigale-plots"
subprocess.run(f"/home/jack/.pyenv/versions/3.9.5/bin/pcigale-plots sed --format png", shell=True)

# 6.) copy output image to args.pathfile.
subprocess.run(f"cp {pcigale_file_folder}/out/{args.sedName}_best_model.png {args.pathFile}", shell=True)


