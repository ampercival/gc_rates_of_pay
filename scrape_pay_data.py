from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests

def create_session():
    """
    Creates a session with a random user agent.

    This function initializes a session for making HTTP requests while
    simulating a random browser user agent. This can help in preventing
    the web server from blocking the requests due to scraping activities.

    Returns:
        session (requests.Session): A session object configured with a random user agent.
    """
    
    # Initialize UserAgent with a list of browser types to simulate.
    ua = UserAgent(browsers=['chrome', 'edge', 'firefox', 'safari'])
    # Create a dictionary with the 'User-Agent' header using a random user agent string.
    headers = {'User-Agent': ua.random}

    # Create a session object from the requests library.
    session = requests.Session()
    # Update the session's headers with the created 'headers' dictionary.
    session.headers.update(headers)

    # Return the configured session object.
    return session

def get_pay_list(url, session):
    
    response = session.get(url)  # Make the GET request using the session object.
    soup = BeautifulSoup(response.text, 'lxml')  # Parse the HTML response.

    # Find the dropdown by its ID or name
    dropdown = soup.find('select', {'id': 'dropdown'})

    # Initialize a list to store each option's data
    classification_data = {}

    # Define the URL prefix to check against
    url_prefix = "https://www.tbs-sct.gc.ca/agreements-conventions/view-visualiser-eng.aspx"

    # Loop through each option in the dropdown
    for option in dropdown.find_all('option'):
        # Extract the label and value (URL) of each option
        label = option.get('label')
        value = option.get('value')
        # Check if the label and value are not None and the URL starts with the specified prefix
        
        if label and value and value.startswith(url_prefix):
            
            # parse the value
            id, bookmark = parse_url(value)

            # Store the data in the options_data dictionary
            classification_data[label] = {  # Use label as the key for the top-level dictionary
                'url': value,
                'id': id,
                'Bookmark': bookmark
            }

    # Print each item in a readable format
    for classification, details in classification_data.items():
        print(f"Classification: {classification}")
        for key, value in details.items():
            print(f"  {key}: {value}")
        print()  # Add an empty line for better readability

    return classification_data

def parse_url(url):

    # Splitting by "?", which separates the base URL from the query parameters and fragment
    parts = url.split('?')
    query_fragment = parts[1]  # Taking everything after the "?"

    # Splitting by "#" to separate the query part and the fragment
    parts = query_fragment.split('#')
    query = parts[0]  # The query part
    bookmark = parts[1]  # The bookmark part

    # Splitting the query part by "=" to get the ID value
    parts = query.split('=')
    id_value = parts[1]  # The ID value

    return id_value, bookmark

def main():

    pay_lists_url = "https://www.tbs-sct.canada.ca/pubs_pol/hrpubs/coll_agre/rates-taux-eng.asp"
    
    # Initialize a session with a random user agent for web requests.
    session = create_session()

    paylist = get_pay_list(pay_lists_url, session)

    # Print the number of options that were stored
    print(f"Found {len(paylist)} classifications to scrape")

if __name__ == "__main__":
    main()