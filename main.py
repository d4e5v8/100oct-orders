import requests
import json
import time
import csv

from datetime import datetime


def get_orders(auth_token, start_date, end_date):
    url = "https://api.squarespace.com/1.0/commerce/orders"

    # Ensure dates are in ISO 8601 UTC format
    print('100|OCT orders... here we go')

#    print(start_date)
#    print(end_date)

    headers = {
        'Authorization': f'Bearer {auth_token}',
    }

    params = {
        'modifiedAfter': start_date,
        'modifiedBefore': end_date
    }

    all_orders = []
    while True:
        response = requests.get(url, headers=headers, params=params)#
#        print(url)
#        print(headers)
#        print(params)
#        print('.')
        if response.status_code == 200:
            data = json.loads(response.content.decode('utf-8'))
            all_orders.extend(data['result'])
#            print(data['pagination']['hasNextPage'])
            if data['pagination']['hasNextPage']:
                time.sleep(1)
                params = {
                    'cursor' : data['pagination']['nextPageCursor']
                }
#                print(params)
            else:
                break
        else:
            print(f"Error: {response.status_code}")
            break
    return all_orders


# usage
auth_token = '0ed8689f-0649-4436-998f-3077d3c3f857'
start_date = '2023-05-01T08:00:00Z'  # Change to your desired start date
end_date = '2023-06-15T00:00:00Z'  # Change to your desired end date
orders = get_orders(auth_token, start_date, end_date)

nb_of_orders_retrieved = len(orders)
# print(type(nb_of_orders_retrieved))


# Now we got the list of all orders over the period, need to split into two lists:
# product ID 644ab8918a97511ab4375314 - Car Display Ticket
# product ID 644abffb0be53a6986136cd8 - Guest Ticket
carDisplayTicket = '644ab8918a97511ab4375314'
guestTicket = '644abffb0be53a6986136cd8'

display_cars_list = ''
guests_list = ''
csv_file_name = './Downloads/100oct2023CC-4seasons.csv'
csv_file_fields = ['Order #', 'Name', '# tickets', 'Year', 'Make', 'Model', 'Color', 'Phone']

# f = open('path/to/csv_file', 'w')
# create the csv writer
# writer = csv.writer(f)
# write a row to the csv file
# writer.writerow(row)
# close the file
# f.close()

pt = 0
while (pt < nb_of_orders_retrieved):
    line_items = orders[pt]['lineItems']
    billed_to_fname = orders[pt]['billingAddress']['firstName']
    billed_to_lname = orders[pt]['billingAddress']['lastName']
    print('Billed to: ', billed_to_fname, ' ', billed_to_lname)
    nb_lines = len(line_items)
    pt_line = 0
    while pt_line < nb_lines:
#        print('line', pt_line)
        line_item = line_items[pt_line]
        if line_item['productId'] == guestTicket or line_item['productId'] == carDisplayTicket:
            print(pt, ': -->> Order: ', orders[pt]['orderNumber'])
            if line_item['productId'] == guestTicket:
                nb_tickets = line_item['quantity']
                print('Nb of tickets: ',nb_tickets)
                guest_name = line_item['customizations'][0]['value']
                print('Guest: ', guest_name)
                car_year = ''
                car_make = 'no car'
                print('Make: ', car_make)
                car_model = ''
                car_color = ''
            elif line_item['productId'] == carDisplayTicket:
                nb_tickets = line_item['quantity']
                print('Nb of tickets: ', nb_tickets)
                guest_name = line_item['customizations'][0]['value']
                print('Guest: ', guest_name)
                car_year = line_item['customizations'][4]['value']
                print('Year: ', car_year)
                car_make = line_item['customizations'][5]['value']
                car_model = line_item['customizations'][6]['value']
                car_color = line_item['customizations'][7]['value']
                print('Make: ', car_make)
                print('Model: ', car_model)
                print('Color: ', car_color)
            print("------")
        single_line_item = line_items[pt_line]
        pt_line = pt_line + 1
    pt = pt+1






