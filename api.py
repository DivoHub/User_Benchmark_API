import requests
from bs4 import BeautifulSoup
import json
import time

class Gpu():

    def __init__(self):
        self.base_url = "https://www.techpowerup.com/gpu-specs/"
        self.parameters = {
        "mfgr" : ["NVIDIA","AMD","INTEL"],
        "lower_year" : 2020,
        "upper_year" : 2020 + 1 }
        self.url_list = []


    def create_url_list(self):
        for year in range(self.parameters["lower_year"],self.parameters["upper_year"]):
            self.url_list.append(f"{self.base_url}?mfgr={self.parameters['mfgr'][0]}&released={year}&mobile=No")
            #self.url_list.append(f"{self.base_url}?mfgr={self.parameters['mfgr'][1]}&released={year}&mobile=No")
            #self.url_list.append(f"{self.base_url}?mfgr={self.parameters['mfgr'][2]}&released={year}&mobile=No")
            #self.url_list.append(f"{self.base_url}?mfgr={self.parameters['mfgr'][0]}&released={year}&mobile=Yes")
            #self.url_list.append(f"{self.base_url}?mfgr={self.parameters['mfgr'][1]}&released={year}&mobile=Yes")
            #self.url_list.append(f"{self.base_url}?mfgr={self.parameters['mfgr'][2]}&released={year}&mobile=Yes")


    def update_url_list(self):
        self.url_list.clear()
        self.create_url_list()
        self.print_list(self.url_list) #testing line
        self.validate_url_list()


        for i in self.url_list:
            self.gpu_fetch(i)



    def validate_url_list(self):
        for each_url in self.url_list:
            if not (requests.get(each_url).ok):
                print (f"Error with URL: {each_url}")
                return False
            else:
                print(f"URL: {each_url} OK")
                time.sleep(1)
        return True

    def print_list(self, list_object):
        for item in list_object:
            print (item)
        return


    def dict_format(self, part_object):
        spec_list = part_object.find_all("td")
        core_counts = spec_list[7].string.split("/")
        part_dict = \
        {"vendor" : spec_list[0]['class'],
         "model" : spec_list[0].find('a').string,
         "url" : spec_list[0].find('a')['href'],
         "chip" : spec_list[1].string,
         "release_date" : spec_list[2].string,
         "bus" : spec_list[3].string,
         "memory" : spec_list[4],
         "gpu_clock" : spec_list[5],
         "memory_clock" : spec_list[6],
         "shader" : int(core_counts[0]),
         "tmu" : int(core_counts[1]),
         "rop" : int(core_counts[2])}
        print (part_dict) #testing line
        self.dict_validator(part_dict)
        return part_dict


    def dict_validator(self, dict_object):
        pass

    def gpu_fetch(self, url):
        new_request = requests.get(url)
        html_text = BeautifulSoup(new_request.text, "html.parser")
        html_text = html_text.find("table", class_="processors")
        parts_list = html_text.find_all("tr")
        del parts_list[0:2]
        parts_list = list(map(self.dict_format, parts_list))

    def update_reference():
        pass

    def query_user():
        user_input = str(input("Enter GPU model: \n"))
        query_object = {"quicksearch": user_input}
        new_query = requests.post("https://www.techpowerup.com/gpu-specs/", json = query_object)

        print (new_query.text)


    #Export dict object into json file in subfolder "export"
    def json_export(dict_object):
        print ("Creating JSON file...\n")
        new_file = open('export/data.json', 'x')
        json_object = json.dumps(dict_object, indent=2)
        new_file.write(json_object)
        new_file.close()
        print ("JSON file created.")

    def help(self):
        command_list = "json_export : export a json file containing gpu and cpu data" \
                       "gpu_list : output list of all GPUs in database" \
                       "cpu_list : output list of all CPUs in database" \
                       "find : returns True of False" \
                       "specs : returns detailed spec dictionary object from specified gpu or cpu (1 argument)" \
                       "list_all : return list of GPUs or CPUs containing string argument given" \
                       "compare : returns performance difference between two GPUs or CPUs (2 arguments)" \

        print (command_list)

class Cpu():

    def __init__(self):
        self.base_url = "https://www.techpowerup.com/cpu-specs/"
        self.parameters = {
        "mfgr" : ["AMD","INTEL"],
        "mobile" : ["No","Yes"],
        "lower_year" : 2010,
        "upper_year" : 2023 }
        self.url_list = []

    def cpu_fetch(new_request):
        URL = "https://www.techpowerup.com/cpu-specs/"
        html_query(URL)
        html_text = BeautifulSoup(new_request.text, "html.parser")
        html_text = html_text.find("table", class_="processors")
        parts_list = list(html_text.find_all("a"))
        for index in range(len(parts_list)):
            parts_list[index] = parts_list[index].string
        print (parts_list) #testing line

def main():
    api = Gpu()
    api.update_url_list()

if __name__ == '__main__':
    main()



