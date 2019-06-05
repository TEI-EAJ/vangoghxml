
import glob
import xml.etree.ElementTree as ET
from datetime import datetime
from geopy.geocoders import Nominatim


prefix = ".//{http://www.tei-c.org/ns/1.0}"
prefix2 = ".//{http://www.vangoghletters.org/ns/}"


files = glob.glob('data/*.xml')

for i in range(len(files)):
    geolocator = Nominatim()
    print(i)
    input_path = files[i]

    tree = ET.parse(input_path)
    ET.register_namespace('', "http://www.tei-c.org/ns/1.0")
    root = tree.getroot()

    author = root.find(prefix + "author").text
    # print(author)

    addressee = root.find(prefix2 + "addressee").text
    # print(addressee)

    placeLet = root.find(prefix2 + "placeLet").text
    # print(placeLet)
    location = geolocator.geocode(placeLet)
    # print((location.latitude, location.longitude))

    dateLet = root.find(prefix2 + "dateLet").text
    date = None
    when_str = ""
    try:
        datetime_object = datetime.strptime(dateLet.split(", ")[1], '%d %B %Y')
        date = str(datetime_object).split(" ")[0]
        when_str = "<date when=\""+date+"\">"+dateLet+"</date>"
    except:
        print("Date Error")

    teiHeader = root.find(prefix + "teiHeader")

    try:
        teiHeader.append(
            ET.fromstring(
                '''
              <profileDesc>
            <correspDesc>
              <correspAction type="sent">
                <persName>'''+author+'''</persName>
                '''+when_str+'''
                <location>
                  <placeName>'''+placeLet+'''</placeName>
                  <geo>'''+str(location.latitude)+''' '''+str(location.longitude)+'''</geo>
                </location>
              </correspAction>
              <correspAction type="received">
                <persName>'''+addressee+'''</persName>
              </correspAction>
            </correspDesc>
          </profileDesc>
              '''
            ))

        tree.write("../docs/data/"+input_path.split("/")[-1], encoding="utf-8")
    except:
        print("Write Error")
