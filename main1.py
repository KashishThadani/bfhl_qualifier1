import requests

# Step 1: Send POST request to generate webhook
generate_url = "https://bfhldevapigw.healthrx.co.in/hiring/generateWebhook/PYTHON"

payload = {
    "name": "Kashish Thadani",          # Replace with your name
    "regNo": "0827AL221069",            # Replace with your registration number
    "email": "kashishthadani05@gmail.com"  # Replace with your email
}

response = requests.post(generate_url, json=payload)

if response.status_code == 200:
    data = response.json()
    webhook_url = data['webhook']
    access_token = data['accessToken']
    print("Webhook URL:", webhook_url)
    print("Access Token:", access_token)

    # Final SQL Query
    sql_query = """
    SELECT 
        p.AMOUNT AS SALARY,
        CONCAT(e.FIRST_NAME, ' ', e.LAST_NAME) AS NAME,
        TIMESTAMPDIFF(YEAR, e.DOB, CURDATE()) AS AGE,
        d.DEPARTMENT_NAME
    FROM PAYMENTS p
    JOIN EMPLOYEE e ON p.EMP_ID = e.EMP_ID
    JOIN DEPARTMENT d ON e.DEPARTMENT = d.DEPARTMENT_ID
    WHERE DAY(p.PAYMENT_TIME) != 1
    ORDER BY p.AMOUNT DESC
    LIMIT 1;
    """

    # Step 2: Submit the SQL query to the second API
    test_webhook_url = "https://bfhldevapigw.healthrx.co.in/hiring/testWebhook/PYTHON"
    
    headers = {
        "Authorization": access_token,  # Use the access token here
        "Content-Type": "application/json"
    }
    
    submit_payload = {
        "finalQuery": sql_query.strip()
    }
    
    # Send POST request to submit the SQL query to the second API
    submit_response = requests.post(test_webhook_url, headers=headers, json=submit_payload)
    
    if submit_response.status_code == 200:
        print("✅ Successfully submitted the query!")
        print("Response Data:", submit_response.json())
    else:
        print("❌ Submission failed:", submit_response.text)

else:
    print("❌ Failed to generate webhook:", response.text)
