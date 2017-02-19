import httplib, urllib, base64
import sys
import binascii
import json
name=sys.argv[1]
f=open(name,'rb')
b=f.read()
key_detect = '063e048346f34160a08fad86ef6fcaed'
key_verify = 'abc0a80f89364a2e8c34323303046982'
# bulid new faceId list
oldlist = []
try:
    historyF = open('C:\Users\TaginDai\Desktop\data.json', 'r')
    history = json.load(historyF)
    i = 0
    for i in xrange(64):
        if(history[i]):
            #print(history[i]['faceId'])
            oldlist.append(str(history[i]['faceId']))
            i = i+1
except Exception as e:
    oldnum = len(oldlist)
    #print(oldlist)

detect_headers = {
    # Request headers
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': key_detect,
}
verify_headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': key_detect,
}

params = urllib.urlencode({
    # Request parameters
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
	'returnFaceAttributes':'age,gender,smile,facialHair,glasses'
})

try:
    conn = httplib.HTTPSConnection('api.projectoxford.ai')
    conn.request("POST", "/face/v1.0/detect?%s" % params, b, detect_headers)
    response = conn.getresponse()
    data = response.read()
    #print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))

# Detect Data
output = open('C:\Users\TaginDai\Desktop\data.json', 'w')
output.write(data)
output.close()


nowF = open('C:\Users\TaginDai\Desktop\data.json', 'r')
now = json.load(nowF)
# bulid new faceId list
newlist = []
try:
    i = 0
    for i in xrange(64):
        if(now[i]):
            #print(data[i]['faceId'])
            newlist.append(str(now[i]['faceId']))
            i = i+1
except Exception as e:
    newnum = len(newlist)
    print(newlist)
nowF.close()

# Verify pairwisely
conn = httplib.HTTPSConnection('api.projectoxford.ai')
occured = []
verify_params = urllib.urlencode({
})
same = 0
for newone in xrange(newnum):
    same = 0
    for oldone in xrange(oldnum):
        try:
            conn = httplib.HTTPSConnection('api.projectoxford.ai')
            conn.request("POST", "/face/v1.0/verify?%s" % verify_params, "{'faceId1':'"+str(newlist[newone])+"','faceId2':'"+str(oldlist[oldone])+"'}" , verify_headers)
            response = conn.getresponse()
            verify_data = json.load(response)
            conn.close()
            if(verify_data['isIdentical']):
                same = 1
                break
        except Exception as e:
            #print("[Errno {0}] {1}".format(e.errno, e.strerror))
            print("[Error aggggggain~]")

    occured.append(same)
print(occured)
vf = open('occured.txt','w')
vf.write(str(occured))
