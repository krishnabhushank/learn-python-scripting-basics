from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/api/v1/getcomppids/checkItem', methods=['GET'])
def get_comppids():
    format_type = request.args.get('formatType')
    product = request.args.get('product')

    # Perform the necessary logic to get the desired response
    status_code = 0
    status_message = 'Success, traceId - 640f1874184b806fcb7ddc5f13fb0da0'
    comp_pid_list = [
        {
            "product": "017-26597",
            "WEBSITE": "BestBuy",
            "PID": "3044367",
            "SKU": None,
            "Source": "MANUAL",
            "Tag": "Corrected",
            "Time_Added": "2019-09-24 17:39:00",
            "meta": "LG-LFC24770ST"
        }
    ]

    response = {
        "status": {
            "statusCode": status_code,
            "statusMessage": status_message,
            "product": product
        },
        "comp_pid_list": comp_pid_list
    }

    return jsonify(response)


@app.route('/ecs/view-price.sws', methods=['POST'])
def view_price():
    # Process the POST request
    data = request.json

    # Perform necessary operations with the received data
    # ...

    response = [
        {
            "status": {
                "statusCode": 0,
                "statusMessage": "Success"
            },
            "productCode": "057/54677",
            "productTypeCode": "ITM",
            "priceEffectiveDate": "2023-06-27",
            "storeId": "3182",
            "suppressRegularPriceIfPromotionExist": False,
            "priceList": [
                {
                    "priceUID": 192696351,
                    "eventUID": 1001,
                    "promotionName": "CLEARANCE",
                    "productCode": "057/54677",
                    "productTypeCode": "ITM",
                    "priceLevel": 40,
                    "priceCode": "3182",
                    "storeIds": [],
                    "storeGroupNames": [],
                    "nationalPrice": False,
                    "priceStartDate": "1998-04-08",
                    "priceEndDate": "9999-12-31",
                    "offerType": 502,
                    "priceDetails": [
                        {
                            "offerDetailName": "PRICE",
                            "offerDetailValue": "1899.97",
                            "offerDetailList": None
                        },
                        {
                            "offerDetailName": "WAS_WAS_WAS_PRICE",
                            "offerDetailValue": "2799.99",
                            "offerDetailList": None
                        }
                    ],
                    "priceStartDateTime": 892008000000,
                    "priceEndDateTime": 253402232400000
                }
            ]
        }
    ]

    return jsonify(response)


if __name__ == '__main__':
    app.run()

    # Code serves /api/v1/getcomppids/checkItem for GET The GET endpoint retrieves the values of formatType and
    # product from the query parameters using request.args.get() Then, it performs the necessary logic to generate
    # the desired response and returns it as a JSON response using jsonify()

    # Code also serves another POST endpoint /ecs/view-price.sws It receives the request data in JSON format using
    # request.json it performs any necessary operations, and constructs the desired response structure. The response
    # is then returned as a JSON response using jsonify()
