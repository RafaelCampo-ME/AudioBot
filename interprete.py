from fileinput import filename
from urllib import response
import json
import requests
import time
import pandas as pd 
from api_secrets_audio import API_KEY
import os 



upload_endpoint = "https://api.assemblyai.com/v2/upload"
transcript_endpoint = "https://api.assemblyai.com/v2/transcript"


# Subir el archivo de audio para obtener la transcripcion

def read_file(filename, chunk_size=5242880):
    """Read the audio file"""
    with open(filename, "rb") as _file:
        while True:
            data = _file.read(chunk_size)
            if not data:
                break
            yield data

#Contine el apy key y el formato 


headers = {
	'authorization': API_KEY
}

def post_audio(filename):
    """Post the audio file in the endpoint"""
    response=requests.post(upload_endpoint,
                        headers=headers,
                        data=read_file(filename))

    audio_url = response.json()['upload_url']
    return audio_url 




def make_polling_endpoint(transcript_response):
    """Ask the API if the process had finished"""

    polling_endpoint = "https://api.assemblyai.com/v2/transcript/"
    polling_endpoint += transcript_response['id']
    return polling_endpoint



def wait_for_completion(polling_endpoint, header=headers):
    """Wait until the request status is completed"""

    while True:
        polling_response = requests.get(polling_endpoint, headers=header)
        polling_response = polling_response.json()

        if polling_response['status'] == 'completed':
            break

        time.sleep(5)



def get_paragraphs(polling_endpoint):
    """Get trascription of the text"""
    paragraphs_response = requests.get(polling_endpoint + "/paragraphs", headers=headers)
    paragraphs_response = paragraphs_response.json()

    paragraphs = []
    for para in paragraphs_response['paragraphs']:
        paragraphs.append(para)

    return paragraphs

def get_sentiment(polling_endpoint):
    """Get sentiment analysis results"""
    sentiment_response =  requests.get(polling_endpoint, headers=headers).json()["sentiment_analysis_results"]
    return sentiment_response
     
def export_sentiment(sentiment: json, filename):
    """Exports sentiment analysis results to .csv file"""
    sent_df=pd.DataFrame(sentiment)
    sent_df['filename'] =   filename  
    output_path='./AudioBot\Data\sentiment_results.csv' 
    if not os.path.isfile(output_path):
        sent_df.to_csv(output_path, mode='a',index=True, header=True)
    else:
        sent_df.to_csv(output_path, mode='a', index=True, header=False)

    return 'La informacion del sentiment se encuentra en el .csv' 



 
  
