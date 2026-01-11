import argparse
import os
import sys
from dotenv import load_dotenv

from prompts import system_prompt
from call_function import available_functions, call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key is None:
    raise RuntimeError("No Gemini API key was found in the environment.")

from google import genai
from google.genai import types

client = genai.Client(api_key=api_key)

def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    for _ in range(20):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt,
            ),
        )
        for candidate in response.candidates:
            messages.append(candidate)
        if response.usage_metadata is None:
            raise RuntimeError("The request to Gemini failed.")
        if args.verbose == True:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        if response.function_calls is None:
            print("Response:")
            print(response.text)
            sys.exit(0)
        else:
            function_results = []
            for call in response.function_calls:
                function_call_result = call_function(call)
                if function_call_result.parts is None or len(function_call_result.parts) == 0:
                    raise Exception("types.Content.parts missing from function types.Content call result")
                if function_call_result.parts[0].function_response is None:
                    raise Exception("Call result types.Content.parts[0].function_response is missing")
                if function_call_result.parts[0].function_response.response is None:
                    raise Exception("Call response missing in result types.Content.parts[0].function_response.response")
                function_results.append(function_call_result.parts[0])
                if args.verbose == True:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
            messages.append(types.Content(role="user", parts=function_results))
    print("Maximum number of iterations reached. Aborting conversation.")
    sys.exit(1)

if __name__ == "__main__":
    main()
