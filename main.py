import interprete as intp 
from os import scandir
import json

path_audio_file = r'.\AudioBot\AudioFileFolder'
language_code =  'en_us' 


def audio_files_on_dir( path: str):
    """Get the names of all .wav files"""
    return([arch.path for arch in scandir(path) if arch.is_file()]) 

def perform_analysis():
    """Execute the sentiment analysis and export the results"""
    for i in audio_files_on_dir(path_audio_file):

        print(f"Reading file: {i}") 
        intp.read_file(i)

        print(f"Finish reading file: {i}. \nPosting file audio.")
        audio_url=intp.post_audio(i)
        print(f"Posting succesufull. \n")

        transcrip_aud=intp.request_transcript(upload_url=audio_url,language_code=language_code)
        print("Get the trascrip of the audio")

        print(json.dumps(transcrip_aud, indent=4, sort_keys=True))
        transcrip_aud_id= transcrip_aud['id']
        polling_endpoint = intp.transcript_endpoint + '/' + transcrip_aud_id

        print(f"Got endpoint for analysis: {polling_endpoint}")

        print("Waiting for analysis to finish.")
        intp.wait_for_completion(polling_endpoint)
        print("Analysis done.")

        
        sentiment_analysis= intp.get_sentiment(polling_endpoint)

        print(json.dumps(sentiment_analysis, indent=4, sort_keys=True) )
        print("Analysis succesfull")

        
        print(intp.export_sentiment(sentiment= sentiment_analysis,filename=i)) 
        print("Data export succesfully to .csv")


perform_analysis()