import requests

# Your SerpAPI key (replace with your actual key)
api_key = 'fa4b10d45affce296c1329520421facbae438cec3715fb3cca987262d6639f8d'

# Function to get S&P 500 value
def get_sp500_value():
    # URL for the Google Finance engine for S&P 500 data
    url = f'https://serpapi.com/search?engine=google_finance&q=S&P+500&api_key={api_key}'
    
    # Sending the GET request to the API
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON data returned by the API
        data = response.json()

        # Debugging: Print the full response to inspect its structure
        print("Full Response:")
        print(data)

        # Extract the stock price for S&P 500 from the JSON data
        try:
            stock_value = data['financials']['price']['raw']  # This may vary based on actual API response structure
            return stock_value
        except KeyError:
            print("Error: The expected data structure is not found in the response.")
            return None
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return None

# Test the function
if __name__ == "__main__":
    print(get_sp500_value())