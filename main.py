import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, you MUST respond with a function call, never just text. Use a function call for every operation-even if you're not sure what to do, pick the closest function. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)

def call_function(function_call_part, verbose=False):
    if verbose == True:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f"- Calling function: {function_call_part.name}")
    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file
    }
    function_call_part.args.update({"working_directory": "./calculator"})
    func = function_map.get(function_call_part.name,)
    if func is None:
        return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_call_part.name,
            response={"error": f"Unknown function: {function_call_part.name}"},
        )
    ],
)
    else:
        function_result = func(**function_call_part.args)
        return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_call_part.name,
            response={"result": function_result},
        )
    ],
)



def main():
    print("Hello from ai-agent!")
    if len(sys.argv) < 2:
        print("You must provide a prompt!")
        sys.exit(1)
    messages = [
    types.Content(role="user", parts=[types.Part(text=sys.argv[1])]),
]
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions],system_instruction=system_prompt)
)

    if response.function_calls:
        for call in response.function_calls:
            function_call_result = call_function(call, verbose="--verbose" in sys.argv)
            if hasattr(function_call_result, "parts") and hasattr(function_call_result.parts[0], "function_response") and hasattr(function_call_result.parts[0].function_response, "response") and len(function_call_result.parts) > 0:
                if "--verbose" in sys.argv:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
            else:
                raise Exception("Function did not return the expected parts[0].function_response.response")
    else:
        print(response.text)
    
    prompt = sys.argv[1]
    if "--verbose" in sys.argv:
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
    


if __name__ == "__main__":
    main()
