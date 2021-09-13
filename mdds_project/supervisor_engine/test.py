import ConfigParser
import os
import base64
import uuid

# cf = ConfigParser.ConfigParser()
# cf.read("supervisor.conf")
# OUTPUT_DIR = cf.get("supervisor", "OUTPUT_DIR")
# SUPERVIE_DIR = cf.get("supervisor", "SUPERVIE_DIR")
#
# print(OUTPUT_DIR)
# print(SUPERVIE_DIR)

answer = "Wk4xMlo2NUM="

result = os.popen("wmic diskdrive get serialnumber")
context = result.read()
result.close()
def get_mac_address():
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e+2] for e in range(0,11,2)])

print type(context.splitlines())
print len(context.splitlines())
for line in context.splitlines()[1:]:
    print line.strip()
    print base64.b64encode(line.strip())

print get_mac_address()








