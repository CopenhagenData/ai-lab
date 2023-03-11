import openai
import os
import re
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

class request_manager:
    def __init__(self) -> None:
        self.request = None
        self.request_type = None
        self.response = None

    def set_request(self, request) -> None:
        self.request = request

    def get_type(self, request) -> str:
        request_type = 'chat'
        self.request_type = request_type
        return request_type
    
    def approve_request(self, request) -> bool:
        if len(request) > 3000:
            print("Please use shorter request...")
            return False
        
        return True

    def request_code(self, 
            request,
            prefix = "Only reply with executable python code. ",
            suffix = "\n Do not include any text that cannot be executed as python code. Print answer."   
        ) -> str:
        print("\nThank you for the code request...\n")
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prefix + request + suffix,
            temperature=0,
            max_tokens=1000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        self.response = response
        return response.choices[0].text

    def request_chat(self, request) -> str:
        print("\nThank you for the chat request...\n")
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=request,
            temperature=0,
            max_tokens=500,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        self.response = response
        return response.choices[0].text

    def query(self, request=None, request_type=None) -> str:
        if request == None:
            request = self.request
        
        if request_type == None:
            request_type = self.request_type

        approval = self.approve_request(request)

        if not approval:
            return 'Request not approved!'

        if request_type == 'code':
            response = self.request_code(request)
        elif request_type == 'chat':
            response = self.request_chat(request)
        elif request_type == 'imagine':
            response = self.request_imagine(request)
        else:
            response = 'No request type'
        
        return response
    
    def exec_code(self, code = None, error_handling_level = 2):
        if code == None:
            code =  self.response
        
        counter = 0

        while counter < error_handling_level:
            try:
                exec(code)
                print('\n\n')
                counter = error_handling_level + 1
                return
            except Exception as e:
                print('\n\nQuery failed, attempting to correct... \n\n')
                L = len(str(e))
                if L > 100:
                    L = 100

                code = self.request_code(
                    request=code,
                    prefix="Correct my code: ",
                    suffix=f"\n I recieve the error {str(e)[0:L]} \n Do not include any text that cannot be executed as python code."
                )
                counter += 1

    def improve_request(request):
        matches = re.findall(r'<(\w+)>', request)
        if len(matches) > 0:
            print(request)
            
        for match in matches:
            input_param = input(f'Please insert {match}: ')
            request = request.replace(f"<{match}>", input_param)

        return request 