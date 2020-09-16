import os
import requests

import pandas as pd
import matplotlib.pyplot as plt

import boto3
from pyathena import connect

import io
from io import BytesIO
from PIL import Image, ImageDraw, ExifTags, ImageColor

import sys

################################################################

def aws_label_rekog(x):
    
    ##########################################################
    # Get response URL for instagram image saved on https://imghost.asc.upenn.edu
    try:
        response_url = requests.get(x.finalurl)
    except:
        # fails on bad handshake or broken url...
        print('oops! Failed to get bad URL:', x.finalurl)
        pass

    ##########################################################
    # This try statement needs to be more specific! what are the errors you are hoping to catch???
    # basically this gets the image binary as this gets passed to AWS
    try:
        image = Image.open(BytesIO(response_url.content))
        stream = io.BytesIO()
        image.save(stream, format=image.format)
        image_binary = stream.getvalue()
    except:
        # Fails on expired URL or Gone...
        print('oops! corrupted image...')
        pass
    
    ##########################################################
    # From here we can take the binary and run one of the detections...
    # Why have different functions, that will have to get the binary 5 different times right? 
    # Instead here we can punch in the different responses under the one rekognition client
    
    # LABEL OBJECT DETECTION
    # does label not have attributes all? or is that only for faces?
    try:
        label_response = client.detect_labels(Image={'Bytes':image_binary})
        return(label_response)
    except:
        print('Rekognition Label API call failed for:',x.finalurl,'\n')
        e = sys.exc_info()
        print('sys error is: {}'.format(e))
        #label_response = None
        #pass
    # THINK ABOUT HOW WE CAN GET THE OTHER RESPONSES, AND RETURN MULTITPLE VALUES FOR LAMBDA FUNCTION...

def insta_finalurl_rekognition(your_instagram_df):

    print('\nRunning Label Rekognition...')
    
    your_instagram_df['AWS_Label_Rekognition'] = your_instagram_df.apply(lambda x: aws_label_rekog(x), axis=1)

    print('Complete! Exporting to json...')
    your_instagram_df.to_json('/data/{}_awsrekog.json'.format(your_instagram_df.username.unique()[0]))
    
    print('DF exported as ./data/{}_awsrekog.json'.format(your_instagram_df.username.unique()[0]))
    

################################################################  
# Run AWS Rekognition test for docker containerization
# Passing environment variable with path to AWS_CONFIG_FILE...
client = boto3.client('rekognition',region_name='us-east-1') 

# HARDCODED CREDENTIALS! DO NOT DO THIS...
#client = boto3.client('rekognition',
#                      aws_access_key_id=asc_tkn,
#                      aws_secret_access_key=sec_tkn,
#                      region_name='us-east-1') # <----Setup AWS Rekognition API calls using boto3.client()

wwe_df = pd.read_json('/app/configs/wwe_df.json')
# input in dockerfile is as of 09/15/2020 the wwe username! testing for RomanReigns now ...

aws_testing_df = wwe_df[wwe_df['username']==str(sys.argv[1])]
print('#'*60)
print('username is --> {}'.format(str(sys.argv[1])))
print('wwe_df shape is --> ', aws_testing_df.shape)
print('env var for cred path --> ', os.environ.get('AWS_CONFIG_FILE'))
print('\nOther env vars: {}\n'.format(os.environ))
insta_finalurl_rekognition(aws_testing_df)