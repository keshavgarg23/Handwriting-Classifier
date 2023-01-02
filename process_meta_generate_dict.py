from bs4 import BeautifulSoup
import glob

dict = {}

for xml in glob.glob('./meta_Data/*'):      #list of all files in folder meta_data

    if(xml.split('/')[-1][0]>'d'):      #split path names on the bases of / and check for only for <= d 
        continue

    # print(xml)

    data = open(xml,"r",encoding='ISO-8859-1')      # encoding found in the file

    soup = BeautifulSoup(data,features="xml",)  # creating a bs4 obj

    form = soup.find('form')        # finding first forms
    if(form and form.has_attr("writer-id")):        # checking if form has writer-id attribute
        writer_id = form["writer-id"]           # extracting the writer id
    else:
        continue
    file_name = form["id"]      # extracting the image name

    if(writer_id in dict.keys()):   # already there then append to list
        dict[writer_id].append(file_name)
    else:                         # else add to dict
        dict[writer_id]=[file_name]

print(dict)