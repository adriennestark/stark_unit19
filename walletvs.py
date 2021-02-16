import subprocess
import json

command = './derive -g --mnemonic="oblige monkey actual pudding ramp affair unveil nut belt input dust happy" --cols=path,address,privkey,pubkey --format=json'

p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
output, err = p.communicate()
p_status = p.wait()

keys = json.loads(output)
print(keys)
