import json 

def build_speechlet_response(title, output, output_text, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content':  output_text
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }
def build_response_withURL(title, output, url, text_output, reprompt_text, should_end_session): 
    return { 
        'outputSpeech':{ 
            'type': 'PlainText', 
            'text': output
        },
        'card':{
            'type': 'Standard', 
            'title': title, 
            'text' : text_output,
            'image': { 
                'largeImageUrl': url
            }
        },
        'reprompt': { 
            'outputSpeech':{
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }
def build_Dialog_Delegate(output_speech, should_end_session, delegate_type, slot1, slots, intent_name): 
    return { 
        "outputSpeech":{ 
            "type": "PlainText", 
            "text": output_speech
        },
        "ShouldEndSession": should_end_session, 
        "directives":[ 
            {
                "type": delegate_type, 
                "slotToElicit": slot1, 
                "updatedIntent":{ 
                    "name": intent_name,
                    "confirmationStatus": "NONE",
                    "slots": slots 
                }
            }
        ] 
    }

def build_response( session_attributes, speech_response): 
    return { 
        ' version' : '1.0', 
        'sessionAttributes': session_attributes,
        'response': speech_response
    }

def get_welcome_response(): 
    # initial state for when a customer says " alexa ask Hofstra"
    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to Alexa for hofstra " + \
                    "What would you like to know about hostra "
    output_text = "What would you like to know about hofstra?"
    reprompt_text = " Do you still want to know information about hofstra"
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output,output_text, reprompt_text, False))

def handle_session_end_request(): 
    # called when the customer says nothing or that is all or thank you
    session_attributes = {}
    card_title = "Session Ended"
    speech_output = """ Thank you for using alexa for hofstra.  
                    Have a great day """
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(card_title, 
                            speech_output, "Thank you" , should_end_session))

def get_map_build(intent, session,intent_request):
    # this fucntion is triggered if the person asks about a specific building location such as 
    # "where is adams hall ? " 
    session_attributes = {}
    card_title = "Building location"
    should_end_session = False
    try: 
        if intent['slots']['building']['value'] == None: 
            if(intent_request['dialogState'] == "STARTED"): 
                delegate_type = "Dialog.ElicitSlot"
                intent_name = intent
                slots = { 
                        "building":{ 
                            "name": "building", 
                            "confirmationStatus": "NONE"
                            }
                        }
                output_speech = " What building are you looking for"
                slot1 = "building"
                return build_response(session_attributes, build_Dialog_Delegate(
                     output_speech, should_end_session, delegate_type, slot1, slots, intent_name))
    except AttributeError: 
        pass
    # once dialog complete will execute regular intent
    if(intent['name'] == "Building_locations"):
        Id = intent['slots']['building']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['id']
        target_building = intent['slots']['building']['value']
        session_attributes = {"TargetBuilding": target_building}
        speech_output = "Since you are looking for " + target_building + " please " + \
                        "look at the map for " + Id + " You are currently located at Adams Hall " + \
                        " Which is number 25"
        output_text = " " + target_building + " is located at number: " + Id + " \n Thank you have a great day."
        repromt_text = None
        url = "https://git.cs.hofstra.edu/h701830314/Documents/raw/master/infocenter_print_campusmap.jpg"
        should_end_session = True
        return build_response(session_attributes, build_response_withURL(card_title, speech_output, url, output_text, repromt_text, should_end_session)) 
                           



def get_map_Dep(intent, session, intent_request): 
    session_attributes = {}
    card_title = "Department location"
    should_end_session = False
    try:
        if(intent['slots']['department']['value'] == None): 
            raise AttributeError
    except (AttributeError, KeyError): 
        if(intent_request['dialogState'] == "STARTED"): 
            delegate_type = "Dialog.ElicitSlot"
            intent_name = intent
            slots = { 
                "departments":{ 
                    "name": "departments", 
                    "confirmationStatus": "NONE"
                }
            }
            output_speech = " What department are you looking for"
            slot1 = "departments"
            return build_response(session_attributes, build_Dialog_Delegate(
                             output_speech, should_end_session, delegate_type, slot1, slots, intent_name))
    if(intent['name'] == "locatordepartments"):
        target_department = intent['slots']['department']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
        session_attributes = {"TargetDepartment": target_department}
        if target_department == "computer science Department":
            speech_output = "The " + target_department + " is located in Adams hall. " + \
                            "Please look at the map for number 25."
            output_text = "The " + target_department + " is located in adams hall look on the map for number 25"
            reprompt_text = None
            should_end_session = True
            url = "https://git.cs.hofstra.edu/h701830314/Documents/raw/master/infocenter_print_campusmap.jpg"
            return build_response(session_attributes, build_response_withURL( card_title, speech_output, url, output_text, reprompt_text, should_end_session))
        elif target_department == "Engineering Department":
            speech_output = "The "+ target_department + " is located in Weed Hall which is number 26 on the map " + \
                            "You are currently at adams hall, Weed hall is the building next door" + \
                            "Thank you have a great Day!"
            output_text = "The "+ target_department + " is located in Weed Hall number: 26 \n Thank you have a great Day!"
            repromt_text = None 
            should_end_session = True
            url = "https://git.cs.hofstra.edu/h701830314/Documents/raw/master/infocenter_print_campusmap.jpg"
            return build_response(session_attributes, build_response_withURL( card_title, speech_output, url, output_text, reprompt_text, should_end_session))
    #defalt output if nothing works
    speech_output = "I do not know which department you are looking for please try again"
    repromt_text = None
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(
                         card_title, speech_output, repromt_text, should_end_session))

def get_Faculty_info(intent, session): 
    session_attributes = {}
    card_title = "Professor Office Location"
    should_end_session = False
    if intent['name'] == "Faculty": 
        filename = open("professors.json","r")
        datastore = json.load(filename)
        name = intent['slots']['professors']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
        con = True
        count = 0
        while con:
            if datastore['values'][count]['name']['name'] == name: 
                con = False 
            else: 
                count = count + 1
        speech_output = datastore['values'][count]['name']['location'] + datastore['values'][count]['name']['fact']
        output_text = datastore['values'][count]['name']['output']
        reprompt_text = None
        should_end_session = True
        filename.close()
        return build_response(session_attributes, build_speechlet_response( card_title, speech_output, output_text, reprompt_text, should_end_session))
#       target_professor = intent['slots']['professors']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
#        if target_professor == "Dr. Zavou": 
#            speech_output = target_professor + " is located in adams hall. which is number 25 on the map. Her area of research is in cyber security" + \
#                                             " Thank you have a great day!"
#            output_text = target_professor + " is in adams hall number: 25 \n Thank you have a great day!" 
#            reprompt_text = None
#            should_end_session = True
#            url = "https://git.cs.hofstra.edu/h701830314/Documents/raw/master/infocenter_print_campusmap.jpg"
#            return build_response(session_attributes, build_response_withURL( card_title, speech_output, url, output_text, reprompt_text, should_end_session))
#        elif target_professor == "Dr. Krish" or target_professor == "Doctor Krish": 
#            speech_output = target_professor + " is located in adams hall . which is number 25 on the map." + target_professor + \
#                                             " is the chair of the computer science department and his research interest Machine Learning Data Mining Privacy" + \
#                                             " Thank you have a great Day"
#            output_text = target_professor + " is located in adams hall.  \n Adams Hall is number 25 on the map \n Thank you have a great Day!"
#            reprompt_text = None 
#            should_end_session = True 
#            url = "https://git.cs.hofstra.edu/h701830314/Documents/raw/master/infocenter_print_campusmap.jpg"
#            return build_response(session_attributes, build_response_withURL( card_title, speech_output, url, output_text, reprompt_text, should_end_session))
#        elif target_professor == "Dr. doboli" or target_professor == "doctor doboli": 
#            speech_output = target_professor + " is located in Adams Hall. which is number 25 on the map." + target_professor + \
#                         " Her area of interest is in Neural models for individual and group brainstorming and in Model extraction from trained neural networks"
#            output_text = target_professor + " is located in Adams Hall. \n Which is number 25 on the map. \n Thank you have a great day!" 
#            reprompt_text = None
#            should_end_session = True
#            url = "https://git.cs.hofstra.edu/h701830314/Documents/raw/master/infocenter_print_campusmap.jpg"
#            return build_response(session_attributes, build_response_withURL( card_title, speech_output, url, output_text, reprompt_text, should_end_session))
#        else: 
#            speech_output = " I am learning more every day unfortunately today I do not know the professor you are looking for. PLease try again another time."+\
#                            " Have a great day"
#            output_text = " I do not know that professor please try again later \n Have a great Day!"
#            reprompt_text = None
#            should_end_session = True
#            return build_response(session_attributes, build_speechlet_response( card_title, speech_output, repromt_text, should_end_session))
    
        

def get_map_rest(intent, session, intent_name): 
    session_attributes = {}
    card_title = "Resturants"
    if intent_name == "Resturant_locator_food":
        filename = open("food.json", "r")
        datastore = json.load(filename)
        name = intent['slots']['food']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
        con = True
        count = 0
        while con:
            if datastore['values'][count]['name']['name'] == name: 
                con = False 
            else: 
                count = count + 1
        
        speech_output = datastore['values'][count]['name']['value'] + datastore['values'][count]['name']['location']
        output_text = datastore['values'][count]['name']['output']
        reprompt_text = None
        should_end_session = True
        url = "https://git.cs.hofstra.edu/h701830314/Documents/raw/master/infocenter_print_campusmap.jpg"
        filename.close()
        return build_response(session_attributes, build_response_withURL( card_title, speech_output, url, output_text, reprompt_text, should_end_session))
    if intent_name == "Resturant_locator":
        filename = open("resturants.json", "r")
        datastore = json.load(filename)
        name = intent['slots']['restaurants']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
        con = True
        count = 0
        while con:
            if datastore['values'][count]['name']['name'] == name: 
                con = False 
            else: 
                count = count + 1
        
        speech_output = datastore['values'][count]['name']['location']
        output_text = datastore['values'][count]['name']['outputText']
        reprompt_text = None
        should_end_session = True
        filename.close()
        return build_response(session_attributes, build_speechlet_response( card_title, speech_output, output_text, reprompt_text, should_end_session))
    should_end_session = False
    speech_output = "I did not understand what you were asking about Hofstra restaurants. Please try again"
    output_text = "Please try again. Thank you" 
    return build_response(session_attributes, build_speechlet_response(
                          card_title, speech_output, output_text, "", should_end_session))

def get_random_fact(intent, session): 
    session_attributes = {}
    card_title = "Resturant location" 
    should_end_session = True
    speech_output = """This section is currently under maintance will be working soon" 
                     "Have a great day""" 
    return build_response(session_attributes, build_speechlet_response( 
        card_title, speech_output,"", should_end_session))


def on_launch(event, context): 
    return get_welcome_response()

def on_intent(intent_request, session): 
    # this function takes in alexas prompt and depending on the prompt that was 
    # trigger the corresponding function to that prompt
    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
    if intent_name == "Building_locations": 
        return get_map_build(intent, session, intent_request)
    elif intent_name == "locatordepartments": 
        return get_map_Dep(intent, session, intent_request)
    elif intent_name == "Resturant_locator": 
        return get_map_rest(intent, session, intent_name)
    elif intent_name == "RandomFacts": 
        return get_random_fact(intent, session)
    elif intent_name == "Faculty":
        return get_Faculty_info(intent,session)
    elif intent_name == "AMAZON.CancelIntent": 
        return handle_session_end_request()
    elif intent_name == "AMAZON.HelpIntent": 
        return on_launch(intent, session) 
    elif intent_name == "AMAZON.StopIntent": 
        return handle_session_end_request()
    elif intent_name == "Officehour": 
        return get_officeHours(intent,session)
    elif intent_name == "DPfinder": 
        return pro_dept_finder(intent,session)
    elif intent_name == "Resturant_locator_food": 
        return get_map_rest(intent, session, intent_name)
    else: 
        raise ValueError("Invalid intent")

def lambda_handler(event, context):

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'] , event['session'])
    elif event['request']['type'] == "SessionEndedRequest": 
        return handle_session_end_request()
