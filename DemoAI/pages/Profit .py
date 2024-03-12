import streamlit as st
import re
import requests
import base64
import json
from dateutil import parser
from urllib.parse import urlparse, parse_qs

# Constants
CLIENT_ID = "8FFAD7C8D2C34EDA975DCEACAE877084"
CLIENT_SECRET = "gRzlrGqLnXy2lmlydWHiz7WxB0fAH3AMORj6HMjdURyI_UV8"
REDIRECT_URI = "https://www.alkhuzam.com/"  # Update with your redirect URI
SCOPE = "accounting.reports.read"
STATE = "12345"

# URLs
AUTH_URL = f"https://login.xero.com/identity/connect/authorize?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope={SCOPE}&state={STATE}"
TOKEN_URL = "https://identity.xero.com/connect/token"
INVOICE_API_URL = "https://api.xero.com/api.xro/2.0/Reports/ProfitAndLoss"

# Main function to exchange code for tokens
def exchange_code_for_tokens(code):
    headers = {
        "Authorization": "Basic " + base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode(),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI
    }
    response = requests.post(TOKEN_URL, headers=headers, data=data)
    json_response = response.json()
    
    if response.status_code == 200:
        access_token = json_response.get('access_token')
        #st.write(access_token)
        if access_token:
            return access_token
        else:
            st.error("Access token not found in response.")
            return None
    else:
        st.error("Error exchanging code for tokens: " + str(response.status_code))
        return None

# Function to extract code from URL
def extract_code_from_url(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    return query_params.get('code', [None])[0]



#  Check the full set of tenants you've been authorized to access
def XeroTenants(access_token):
    connections_url = 'https://api.xero.com/connections'
    response = requests.get(connections_url,
                           headers = {
                               'Authorization': 'Bearer ' + access_token,
                               'Content-Type': 'application/json'
                           })
    json_response = response.json()
    st.write(json_response)
    
    for tenants in json_response:
        json_dict = tenants
    return json_dict['tenantId']
    
# Function to call Profit and Loss API  
def get_invoices(access_token):
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "xero-tenant-id": "f00ebacd-31e5-43e8-a772-0f0ddd88646a",
        "Accept": "application/json"
    }
    response = requests.get(INVOICE_API_URL, headers=headers)
    if response.status_code == 200:
        
        xero_output = open('proloss.txt', 'w')
        xero_output.write(response.text)
        xero_output.close()

        invoices = open(r'proloss.txt', 'r').read()
        json_invoice = json.loads(invoices)
        analysis = open(r'proloss.csv', 'w')
        analysis.write('Type' + ',' + 'Total')
        analysis.write('\n')
        values = []
        section_title = ""
        for report in json_invoice['Reports']:
         for section in report.get('Rows', []):  # Using .get() to handle missing 'Rows' key
            for row in section.get('Rows', []):  # Using .get() to handle missing 'Rows' key
                if row['RowType'] == 'Row':
                    cells = [cell['Value'] for cell in row['Cells']]
        #            #values.append(cells)
                    values = ','.join(cells) + '\n'  # Joining values into a comma-separated string
                    analysis.write(values)
    
        return values     
    else:
        return None





# Streamlit app
def main():
    st.title("We dont know the app name yet :)")
    st.markdown(f"Click [here]({AUTH_URL}) to authorize your app.")

    # Retrieve code from URL
    #code = st.text_input("Enter the code received after authorization:")
    redirect_url = st.text_input("Enter the redirect URL:")
    code = extract_code_from_url(redirect_url)
    
    if st.button("Exchange code for tokens"):
     st.write(code)
     if code:
       access_token = exchange_code_for_tokens(code)
       if access_token:
        invoices = get_invoices(access_token)
        if invoices:
            st.write("Data received:")
            #st.write(invoices)
            #with open("inv.txt", "w") as file:
            # file.write(invoices)
            st.success("Data have been written to 'proloss.txt'")
        else:
            st.write("Error fetching Data.")
       else:
           st.write("Error exchanging code for tokens.")
     else:
        st.write("Please enter the code.")

    st.write(' ')
    st.write(' ')
    st.write(' ')
    st.write(' ')
    st.write(' ')
    st.write(f"© 2024 Alkhuzam Co. | An Independent Member Of Morison Global. All Right Reserved.  <span style='color:red'></span>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
    