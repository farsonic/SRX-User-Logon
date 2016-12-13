#!/usr/bin/python   
import gzip, os, sys, csv, re   
import subprocess
   
   
for envvar in ("PYTHONPATH", "LD_LIBRARY_PATH"):   
 if envvar in os.environ:   
  del os.environ[envvar]   
   
def openany(p):   
 if p.endswith(".gz"):   
  return gzip.open(p)   
 else:   
  return open(p)   
   
results_file = sys.argv[8]
  
#extract the raw log entry from the compressed csv file passed from splunk 
for row in csv.DictReader(openany(results_file)):   
 raw = row["_raw"]

#print raw
#extract fileds from the raw line entry 
user = re.search('user=(.*?\s)', raw).group(1)
user = user.replace(" ","")
ip = re.search('ip=(.*?\s)', raw).group(1)
ip = ip.replace(" ","")
posture = re.search('posture=(.*?)$', raw).group(1)
posture = posture.replace(" ","")

subprocess.call([sys.executable, '/opt/splunk/bin/scripts/User_logon.py', '-o','logon','-a',ip,'-d','my_domain','-r','Home-User','-u',user,'-p',posture])
