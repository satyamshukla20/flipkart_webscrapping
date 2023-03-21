from flask import Flask,render_template,request
import pandas as pd
import csv
import boto3

app = Flask(__name__)

# create a boto3 S3 client
def s3data():
    s3_client = boto3.client('s3',"")

    bucket_name = 'flipkartsmartphonebucket'
    file_name = 'flipkart_smartphone_data.csv'

    with open('flipkart_data.csv', 'wb') as f:
        s3_client.download_fileobj(bucket_name, file_name, f)
s3data()
def get_data():
    data = pd.read_csv('flipkart_data.csv')
    return data

@app.route('/',methods=['GET', 'POST'])
def index():
    data = None
    if request.method == 'POST' and 'operation' in request.form:
        operation = request.form['operation']
        if operation == 'option1':
            data = get_data()
        elif operation == 'option2':
            data = get_data().nlargest(10, 'price')
        elif operation == 'option3':
            data=get_data().nlargest(10,'original_price')
        elif operation == 'option4':
            data = get_data().nsmallest(10, 'price')
        elif operation == 'option5':
            data=get_data().nsmallest(10,'original_price')
        elif operation == 'option6':
            data=get_data().nlargest(10,'rating')
        elif operation == 'option7':
            data=get_data().nlargest(10,'reviews')
        elif operation == 'option8':
            data=get_data()
            data['discount'] = data['original_price'] - data['price']
            data=data.nlargest(10,'discount')
        


    return render_template('index.html', request=request, data=data)


if __name__ == '__main__':
    app.run(debug=True)

