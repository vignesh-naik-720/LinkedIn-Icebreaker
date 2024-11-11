# start.py
from dotenv import load_dotenv
from langchain.prompts.prompt import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from langchain_google_genai import ChatGoogleGenerativeAI
import getpass
import os

# Load environment variables
load_dotenv()

# Prompt for Google API Key if not set
if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Provide your Google API Key")

# Function to generate an icebreaker
def ice_break_with(name: str) -> str:
    try:
        # Lookup LinkedIn profile URL
        linkedin_username = linkedin_lookup_agent(name=name)
        if not linkedin_username:
            return "Error: LinkedIn username not found. Please check the input name."

        # Validate LinkedIn URL format
        if not linkedin_username.startswith("https://www.linkedin.com/in/"):
            return "Error: The LinkedIn URL is incorrectly formatted. It should start with 'https://www.linkedin.com/in/'."

        # Scrape LinkedIn profile data
        linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_username)
        
        if not linkedin_data:
            return "Error: Unable to retrieve LinkedIn profile data. Please ensure the profile exists and is publicly accessible."

        # Define the summary prompt
        summary_template = """
        Given the Linkedin information {information} about a person, please create:
        1. A short summary
        2. Two interesting facts about them
        """
        summary_prompt_template = PromptTemplate(
            input_variables=["information"], template=summary_template
        )
        
        # Initialize Google Generative AI model
        llm = ChatGoogleGenerativeAI(model="gemini-pro")
        
        # Generate response using the chain
        chain = summary_prompt_template | llm | StrOutputParser()
        res = chain.invoke(input={"information": linkedin_data})

        return res

    except Exception as e:
        # Handle general exceptions
        return f"An error occurred: {e}"

# Run the function
if __name__ == "__main__":
    print("Starting LinkedIn Icebreaker Generation")
    name = input("Enter the LinkedIn Profile Name: ")
    print(ice_break_with(name=name))
