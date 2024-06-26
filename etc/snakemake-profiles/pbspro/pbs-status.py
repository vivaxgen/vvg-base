#!/usr/bin/env python3

import sys
import subprocess
import yaml

jobid = sys.argv[1]

try:
    res = subprocess.run("qstat -f -F json -x {}".format(jobid), check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

    d = yaml.safe_load(res)

    #xmldoc = ET.ElementTree(ET.fromstring(res.stdout.decode())).getroot()
    #job_state = xmldoc.findall('.//job_state')[0].text

    job = (j := d['Jobs'])[list(j)[0]]
    job_state = job['job_state']

    if job_state == "F":
        exit_status = job['Exit_status']
        #exit_status = xmldoc.findall('.//exit_status')[0].text
        if exit_status == 0:
            print("success")
        else:
            print("failed")
    else:
        print("running")

except (subprocess.CalledProcessError, IndexError, KeyboardInterrupt) as e:
    print("failed")
