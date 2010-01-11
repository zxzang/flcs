
import string, random

positions = [22.23423, 8.345345]

def updatePosition(positions):
    positions[0]=positions[0]+random.uniform(-0.0123,0.0232)
    positions[1]=positions[0]+random.uniform(-0.0123,0.0232)
    tmp = "/web/main/updateLocation.html?longitude="+str(positions[0])+"&latitude="+str(positions[1])
    return tmp

for x in range(100):
    print updatePosition(positions)
    x+=1
    
    while k <100:
        