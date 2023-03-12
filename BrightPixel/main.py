
# Import namespaces
from dotenv import load_dotenv
import openai
import os
from uuid import uuid4
import urllib.request

# Set default save path
save_path = "./images/"

# Get Configuration Settings
load_dotenv()
openai_key = os.getenv('OPENAI_API_KEY')

# Configure openai
openai.api_key = openai_key

# Create image function
def create_image(request, save=True):
    response = openai.Image.create(
        prompt=request,
        n=1,
        size="1024x1024"
    )
    image_url = response['data'][0]['url']
    full_save_path = save_path + f"openai_{uuid4()}.png"
    urllib.request.urlretrieve(image_url, full_save_path)
    return full_save_path

# Main function
def main():
    error_msg = ""
    while True:
        print("Waiting for user input (write 'quit' to exit)...")
        request = input()
    
        if request == "quit":
            print("Exiting...")
            break
        elif request == "error":
            print("Error message: " + error_msg)

        # Create image
        try:
            create_image(request)
            print(f"\nImage created successfully! Saved to: {full_save_path}\n")
        except Exception as e:
            print("Error creating image - try again")
            error_msg = str(e)
            continue

# Run main
if __name__ == "__main__":
    main()
