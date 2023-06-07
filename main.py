
import requests
import json5
from datetime import datetime

def get_orders(auth_token, start_date, end_date):
    url = "https://api.squarespace.com/1.0/commerce/orders"

    # Ensure dates are in ISO 8601 format
    if not isinstance(start_date, str) or not isinstance(end_date, str):
        start_date = datetime.strptime(start_date, "%Y-%m-%d").isoformat()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").isoformat()

    headers = {
        'Authorization': f'Bearer {auth_token}',
    }

    params = {
        'modifiedAfter': start_date,
        'modifiedBefore': end_date
    }

    all_orders = []
    while True:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = json5.loads(response.content.decode('utf-8'))
            all_orders.extend(data['result'])
            if 'nextPageCursor' in data['pagination']:
                params['cursor'] = data['pagination']['nextPageCursor']
            else:
                break
        else:
            print(f"Error: {response.status_code}")
            break
    return all_orders


# usage
auth_token = '22abd801-7679-47f2-8616-13fba006a243'
start_date = '2023-05-26'  # Change to your desired start date
end_date = '2023-06-06'  # Change to your desired end date
orders = get_orders(auth_token, start_date, end_date)
print(orders)
