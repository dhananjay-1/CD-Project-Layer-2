# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
#
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

#for running the Layer 3 cpp executable file
import subprocess
#
#For sending the result of current layer to next layer i am using firebase real time database
from firebase import Firebase
firebaseConfig = {
    "apiKey": "AIzaSyDqY9nCUQFlrLj_VItJjIHrjFG9NYtfqm0",
    "authDomain": "pythondbtest-5ccb5.firebaseapp.com",
    "databaseURL": "https://pythondbtest-5ccb5.firebaseio.com",
    "projectId": "pythondbtest-5ccb5",
    "storageBucket": "pythondbtest-5ccb5.appspot.com",
    "messagingSenderId": "115087157673",
    "appId": "1:115087157673:web:58dee673030846bd3c7cb8",
    "measurementId": "G-4VPP47EBM9"
  }
firebase = Firebase(firebaseConfig)

# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World! it finally worked, oh yeah")

        return []



#cppCodeHeader = "#include<bits/stdc++.h>\nusing namespace std;\nint main(){\n"
#cppCodeFooter = "\nreturn 0;\n}"
#cppCodeBody = ""
#nestedBlocksCounter = 0

def showCppCode(obj):

    inBlock = ""
    for _ in range(obj["nestedBlocksCounter"]):
        inBlock += "\n}"
    
    op = obj["cppCodeHeader"] + obj["cppCodeBody"] + inBlock + obj["cppCodeFooter"]
    print(op)


def prepareRes(codeNo, arr, useRoles=False):
    res = {"codeNo":codeNo}
    for obj in arr:
        entity = obj['entity']
        if useRoles and "role" in obj.keys():
            entity = obj['role']

        value = obj['value']
        res[entity] = value

    return res

def sendResToNextLayer(res):
    #firebase.database().child("nlpOutput").set(res)

    obj = firebase.database().child("cppCodeOutput").get().val()
    print("res of NLP Layer : ", res)

    s = ""
    for entity in res.keys():
        val = res[entity]
        if entity=="codeNo":
            s += str(val)
        else:
            s += "\n"+entity+" "+val

    s += "\n"+"end"
   
    ## Shell=False helps the process terminate
    path = "C:/Users/Dhananjay Deswal/Documents/DTU 6th Sem/Compiler Design/CD Project Layer 3/bin/Debug/CD Project Layer 3.exe"
    process = subprocess.Popen(path, shell=False, encoding='utf8', stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    ## Get exit codes
    out, err = process.communicate(s)
    errcode = process.returncode

    process.kill() 
    process.terminate()

    obj["cppCodeBody"] += "\n"+out

    firebase.database().child("cppCodeOutput").update({"cppCodeBody":obj["cppCodeBody"]})

    showCppCode(obj)

    

class ActionVariableCreation1(Action):

    def name(self) -> Text:
        return "action_variable_creation_1"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        arr = tracker.latest_message['entities']
        userMsg = tracker.latest_message['text']

        print("user message : ", userMsg)

        res = prepareRes(0, arr)
        sendResToNextLayer(res)

        dispatcher.utter_message(text="This is variable creation 1 intent")

        return []

class ActionAssignmentOperation(Action):

    def name(self) -> Text:
        return "action_assignment_operation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        arr = tracker.latest_message['entities']
        userMsg = tracker.latest_message['text']

        print("user message : ", userMsg)

        res = prepareRes(1, arr)
        sendResToNextLayer(res)

        txt = tracker.latest_message['intent']['name']
        dispatcher.utter_message(text=txt)

        return []

class ActionArithmeticOperation(Action):

    def name(self) -> Text:
        return "action_arithmetic_operation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        arr = tracker.latest_message['entities']
        userMsg = tracker.latest_message['text']

        print("user message : ", userMsg)

        res = prepareRes(2, arr, useRoles=True)
        sendResToNextLayer(res)

        txt = tracker.latest_message['intent']['name']
        dispatcher.utter_message(text=txt)

        return []

class ActionConditionalStatement(Action):

    def name(self) -> Text:
        return "action_conditional_statement"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        ref = firebase.database().child("cppCodeOutput")
        obj = ref.get().val()
        count = obj["nestedBlocksCounter"]
        firebase.database().child("cppCodeOutput").update({"nestedBlocksCounter":count+1})

        arr = tracker.latest_message['entities']
        userMsg = tracker.latest_message['text']

        print("user message : ", userMsg)

        userMsg = userMsg.split()
        conditionalKeyword = ""
        expression = ""

        if userMsg[0]=="if":
            conditionalKeyword = "if"
            expression = ' '.join(userMsg[1:])

        elif len(userMsg)>1 and userMsg[0]=="else" and userMsg[1]=="if":
            conditionalKeyword = "else if"
            expression = ' '.join(userMsg[2:])

        else:
            conditionalKeyword = "else"

        res = {"codeNo":3}
        res["conditionalKeyword"] = conditionalKeyword
        res["expression"] = expression

        sendResToNextLayer(res)

        txt = tracker.latest_message['intent']['name']
        dispatcher.utter_message(text=txt)

        return []

class ActionComeOut(Action):

    def name(self) -> Text:
        return "action_come_out"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        arr = tracker.latest_message['entities']
        userMsg = tracker.latest_message['text']

        ref = firebase.database().child("cppCodeOutput")
        obj = ref.get().val()
        count = obj["nestedBlocksCounter"]
        cppCodeBody = obj["cppCodeBody"]+"\n}"
        firebase.database().child("cppCodeOutput").update({"nestedBlocksCounter":count-1, "cppCodeBody":cppCodeBody})

        print("user message : ", userMsg)

        res = {"codeNo":4}
        sendResToNextLayer(res)

        txt = tracker.latest_message['intent']['name']
        dispatcher.utter_message(text=txt)

        return []

class ActionWhileLoop(Action):

    def name(self) -> Text:
        return "action_while_loop"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        arr = tracker.latest_message['entities']
        userMsg = tracker.latest_message['text']

        ref = firebase.database().child("cppCodeOutput")
        obj = ref.get().val()
        count = obj["nestedBlocksCounter"]
        firebase.database().child("cppCodeOutput").update({"nestedBlocksCounter":count+1})

        print("user message : ", userMsg)

        userMsg = userMsg.split()
        expression = ' '.join(userMsg[1:])

        res = {"codeNo":5}
        res["expression"] = expression

        sendResToNextLayer(res)

        txt = tracker.latest_message['intent']['name']
        dispatcher.utter_message(text=txt)

        return []

class ActionListCreation(Action):

    def name(self) -> Text:
        return "action_list_creation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        arr = tracker.latest_message['entities']
        userMsg = tracker.latest_message['text']

        print("user message : ", userMsg)

        res = prepareRes(6, arr)
        sendResToNextLayer(res)

        txt = tracker.latest_message['intent']['name']
        dispatcher.utter_message(text=txt)

        return []

class ActionInputVariable(Action):

    def name(self) -> Text:
        return "action_input_variable"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        arr = tracker.latest_message['entities']
        userMsg = tracker.latest_message['text']

        print("user message : ", userMsg)

        res = prepareRes(7, arr)
        sendResToNextLayer(res)

        txt = tracker.latest_message['intent']['name']
        dispatcher.utter_message(text=txt)

        return []