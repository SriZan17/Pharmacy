import openpyxl
import json
import os

wb = openpyxl.load_workbook("Pharmacy.xlsx")
sheet = wb["Sheet1"]
# get all the json files in the data folder

data = {}
path = "data/"
files = os.listdir(path)
files = [file for file in files if file.endswith(".json")]
for file in files:
    with open(path + file) as f:
        data.update(json.load(f))

i = 2
for key in data:
    SN = sheet["A" + str(i)]
    State_Name = sheet["B" + str(i)]
    Pharmacy_Name = sheet["D" + str(i)]
    Address = sheet["E" + str(i)]
    Phone = sheet["F" + str(i)]
    Fax = sheet["G" + str(i)]
    Email = sheet["H" + str(i)]
    Website = sheet["I" + str(i)]
    SN.value = i - 1
    State_Name.value = "NSW"
    Pharmacy_Name.value = key
    Address.value = data[key]["address"]
    Phone.value = data[key]["phone"]
    Fax.value = data[key]["fax"]
    Email.value = data[key]["email"]
    Website.value = data[key]["website"]
    i += 1
wb.save("Pharmacy.xlsx")
