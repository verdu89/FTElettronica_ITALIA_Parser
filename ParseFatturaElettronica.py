import csv
import requests
import glob
from csv import DictWriter
from openpyxl import Workbook
import xml.etree.ElementTree as ET
import re


book = Workbook()
sheet = book.active
# grab the active worksheet

filnames = glob.glob('fatture/*.xml')
for filname in filnames:
    tree = ET.parse(filname)
    root = tree.getroot()
    celRow = []
    scadenza= []
    for item in root.findall('FatturaElettronicaBody/DatiGenerali/DatiGeneraliDocumento/Data'):
        dataFt = item.text
        celRow.append([dataFt])
    if root.findall('FatturaElettronicaBody/DatiPagamento/DettaglioPagamento/DataScadenzaPagamento'):
        for item in root.findall('FatturaElettronicaBody/DatiPagamento/DettaglioPagamento/DataScadenzaPagamento'):
            scadFt = item.text
            scadenza.append(scadFt)
            if len(scadenza) == 1:
                celRow.append(scadenza)
    else:
        celRow.append(['Immediata'])

    for item in root.findall('FatturaElettronicaBody/DatiGenerali/DatiGeneraliDocumento/Numero'):
        numFt = item.text
        celRow.append([numFt])
    if root.findall('FatturaElettronicaHeader/CedentePrestatore/DatiAnagrafici/Anagrafica/Denominazione'):
        for item in root.findall('FatturaElettronicaHeader/CedentePrestatore/DatiAnagrafici/Anagrafica/Denominazione'):
            fornitore = item.text
            celRow.append([fornitore])
    else:
        for item in root.findall('FatturaElettronicaHeader/CedentePrestatore/DatiAnagrafici/Anagrafica/Cognome'):
            fornitore = item.text
            celRow.append([fornitore])

    for item in root.findall('FatturaElettronicaBody/DatiGenerali/DatiGeneraliDocumento/ImportoTotaleDocumento'):
            totFt = item.text
            celRow.append([totFt])


    def savetoCSV(riga, filename):

        # specifying the fields for csv file
        fields = []

        # writing to csv file
        with open(filename, 'a+') as csvfile:

            # creating a csv dict writer object
            writer = csv.DictWriter(csvfile, fieldnames = fields, extrasaction='raise')

            # writing headers (field names)
            writer.writeheader()

            # writing data rows
            csvfile.write(str(celRow))

        csvfile.close()

    def main():


        # store news items in a csv file
        savetoCSV(filname, 'esportazione.csv')




        # calling main function

    main()
