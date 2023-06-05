# Email Content Classification with NLP
This Python program utilizes the Spacy library and Google APIs to analyze the content of email messages and classify them based on their context. It extracts the label, snippet, and body of a Gmail message and performs natural language processing (NLP) to understand the content. The program checks for specific keywords and assigns appropriate labels to the messages.

# Prerequisites
To run this program, you need the following:

1. Python 3.x installed on your machine.
2. Spacy library installed. You can install it using pip install spacy.
3. Google API credentials file (credentials.json) with access to the Gmail API. You can obtain the        credentials by creating a project in the Google Cloud Console and enabling the Gmail API.
4. The google-api-python-client library installed. You can install it using pip install google-api-python-client.

# Usage
Place the credentials.json file in the same directory as the Python script.

Replace 'MESSAGE_ID' in the code with the actual ID of the Gmail message you want to analyze.

Run the Python script.

# Program Flow
1. The program loads the Google API credentials from the credentials.json file and initializes the Gmail API client.

2. Spacy's English language model (en_core_web_sm) is loaded to perform NLP analysis.

3. The getMessages function fetches the label, snippet, and body of the specified Gmail message using the Gmail API.

4. The message snippet and body are decoded from base64 and stored as strings.

5. The NLP analysis is performed on the message body using Spacy.

6. The program checks for specific keywords related to different categories such as education, health, career, shopping, and advertisements.

7. Based on the presence of keywords, the program assigns a label to the message.

8. The label assigned to the message is printed as the output. 

9. Code line for modifying labels has been commented out so that while testing you don't make any changes to your mail settings without being sure. 

# Customization
You can customize this program by modifying the keyword lists for different categories. Update the education_keywords, health_keywords, career_keywords, shopping_keywords, and ad_keywords lists according to your requirements. Feel free to add or remove keywords as needed to improve the accuracy of the classification.

# Note
Ensure that you have the necessary permissions and valid credentials to access the Gmail API. Make sure the required libraries are installed, and the credentials.json file is present in the same directory as the Python script.

Please be aware that this program provides a basic example of email content classification using NLP techniques. Depending on your specific use case, you may need to further refine and enhance the classification logic and adapt it to your needs.