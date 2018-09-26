import re
import pandas as pd
import chardet
import json
from pathlib import Path
from argparse import ArgumentParser

strTypes = "@to:#date-time# @from:#date-time# @leave-type:#LeaveType#"

class DataGenerator(object):
    
    strEntities = ""
    dictRasaRoot = {}

    def __init__(self):
        arrCommonExamples = []
        dictCommonExamples = {}
        dictCommonExamples["common_examples"] = arrCommonExamples
        self.dictRasaRoot["rasa_nlu_data"] = dictCommonExamples
        pass

    def findEntities(self,strInput,strIntent):
        objPattern = r"@(.*?):?#(.*?)#"
        arrResult = re.findall(objPattern, strInput)
        arrParts = []
        intPreviousRange = 0
        arrEntities = []
        dictStatement = {}

        for result in arrResult:
            strOriginalString = "@" + result[0] + ":" + "#" + result[1] + "#"
            intStartRange = strInput.index(strOriginalString)
            strPart = strInput[intPreviousRange:intStartRange]
            arrParts.append(strPart)
            strPart2 = strInput[intStartRange:intStartRange+len(strOriginalString)]
            arrParts.append(strPart2)
            intPreviousRange = intStartRange + len(strOriginalString)

        if intPreviousRange < len(strInput):
            strPart3 = strInput[intPreviousRange:]
            arrParts.append(strPart3)

        intCurrentRange = 0
        strFinalUpdatedMessage = ""
        for tmpPart in arrParts:
            arrResult = re.findall(objPattern, tmpPart)
            if len(arrResult) > 0:
                objResult = arrResult[0]
                tmpPart = objResult[1]
                dictEntity = {}
                dictEntity["start"] = intCurrentRange
                dictEntity["end"] = intCurrentRange + len(tmpPart)
                dictEntity["value"] = tmpPart
                dictEntity["entity"] = objResult[0]
                arrEntities.append(dictEntity)

            intCurrentRange = intCurrentRange + len(tmpPart)
            strFinalUpdatedMessage = strFinalUpdatedMessage + tmpPart
        
        dictStatement["text"] = strFinalUpdatedMessage
        dictStatement["entities"] = arrEntities
        dictStatement["intent"] = strIntent
        self.putInCommonExamples(dictStatement)
        return dictStatement

    def putInCommonExamples(self,dictStatement):
        arrCommonExamples = self.dictRasaRoot["rasa_nlu_data"]["common_examples"]
        arrCommonExamples.append(dictStatement)

    def findDataTypeName(self,strVariable):
        objPattern = r"@(.*?):?#(.*?)#"
        arrResult = re.findall(objPattern, self.strEntities)
        for result in arrResult:
            # print(result)
            if result[0] == strVariable:
                return result[1]

    def readCSVFile(self,strInputFile,strOutputFile="output.json"):

        config = Path(strInputFile)
        if config.is_file():
            with open(strInputFile, 'rb') as f:
                result = chardet.detect(f.read())
            df = pd.read_csv(strInputFile, encoding=result['encoding'])

            if len(df.columns) >= 2:
                strIntentColumn = df.columns[0]
                strTrainingColumn = df.columns[1]

                for row in df.iterrows():
                    self.findEntities(row[1][strTrainingColumn],row[1][strIntentColumn])

                with open(strOutputFile, 'w') as fp:
                    json.dump(self.dictRasaRoot, fp, indent=2)
            else:
                raise Exception("CSV file's structure is invalid")
                print("There should be 2 columns.")
                print("1. Intents")
                print("2. Training Data")
        else:
            raise Exception('Hey! you made mistake. The file does not exist.')

    def definedSynonyms(self,strDatatype):
        pass    
