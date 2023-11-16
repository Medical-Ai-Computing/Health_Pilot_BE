import os
import openai
openai.api_key = os.environ.get("OPENAI_API_KEY", "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")

def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

def collect_messages(prompt):
    panels = context.copy()

    panels.append({'role':'user', 'content':f"{prompt}"}) #TODO unfinished tasks
    return panels

context = [ {'role':'system', 'content':"""
             Upon receiving user input, you are expected to comprehensively collect and analyze 
             health-related information from the user. The user will provide details about symptoms, age, allergies, 
             gender, pregnancy status, blood type, blood pressure, chronic conditions, smoking habits, alcohol usage, 
             recent surgeries, infectious diseases, recent illnesses, location, sleep patterns, and medications. 
             In case specific information is missing, assume the default answer is 'NO', that means if no 
             blood pressure information is presented then assume user have no high blood pressure. if you want to 
             understand how you work the process of giving response from the input is you can follow this simple step.

            1. Data Collection: Take the user's input and gather all available details, ensuring you understand the user's condition thoroughly. 
             Carefully analyze the user's symptoms and health details. Note any possible connections between symptoms.

            2. Disease Identification: Based on the provided information, identify up to 5 potential diseases with symptoms matching 
             the user's input. Rank these diseases from most accurate to least accurate match. Do not diagnose; provide possibilities.

            3. User Interaction: Present the user with the identified diseases. Allow the user to choose from the list of diseases presented.

            4. Recommendation: After the user selects a disease, offer simple and practical home-treatable recommendations, 
             considering the chosen disease. Suggest remedies, treatments, medications, or exercises that can help address the health issue. 
             Emphasize consulting a healthcare professional for personalized advice.

            5. Gratitude and Closure: assure them that you're here to assist. Encourage them to reach out for any further health concerns.

             Ensure clear communication and understanding at each step. If the user's input is unclear or incomplete, 
             In case specific information is missing, assume the default answer is 'NO'. Remember, your role is to assist and provide information, 
             not to diagnose or replace professional medical advice. and take your time to understand and analyse the problem before responsing, 
             and on the response please dont include that 'Please note that I am not a doctor, but I can provide you with some' or related output.
             """} ]

# final_context = panels.append({'role':'user', 'content':f"my dieases is {prompt}"})

# sample inpute may look like
# hi i am {32} years old, My Gender is {male}, and i have a symptoms including {Fever, 
# muscle pains, Headache, Sore throat, Night sweats, Mouth sores}, and 
# infection include is {Swollen, lymph glands}, and allergies of {fever, 
# rhinitis}. My Blood type is {O+}. i have {High} blood pressure. i have {No} chronic conditions. 
# And i {don't} Smokes. I have {No} Alcohol addiction. I have {No} recent surgery. History of 
# {NO} infectious diseases. My Location is : Ethiopia. and I have {no} good sleep pattern.

##################   GPT
# Hi, I am {32} years old. My gender is {male}, and I am currently experiencing symptoms such as 
# {fever, muscle pains, headache, sore throat, night sweats, mouth sores}. Additionally, 
# I have noticed {swollen lymph glands} indicating a possible infection, and I also have allergies to 
# {fever, rhinitis}. My blood type is {O+}, and I am dealing with {high} blood pressure.

# As for my health history:
# - I {do not} have any chronic conditions. {Chronic Condition Name}
# - I am {a non-}smoker.
# - I {do not} have any alcohol addiction.
# - I {have not} undergone recent surgery. {Surgery Name}
# - I {have no} history of infectious diseases. {Infectious Disease Name}

# Currently, I am located in {Ethiopia}, and unfortunately, I {do not} have a consistent sleep pattern.
