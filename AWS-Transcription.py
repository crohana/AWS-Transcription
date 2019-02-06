from __future__ import print_function
import boto3
import time
import os

#Sets variables
s3 = boto3.client('s3')
print('Enter the s3 bucket name')
s3Bucket = input()

print('Enter name of file in Audio to upload')
fileName = input()
filePath = 'Audio/' + fileName
noExt, fileExt = os.path.splitext(filePath)
if fileExt == '.mp3':
    fileExt = 'mp3'
elif fileExt == '.mp4':
    fileExt = 'mp4'
elif fileExt == '.wav':
    fileExt = 'wav'
elif fileExt == '.flac':
    fileExt = 'flac'
else:
    print('Invalid format. Convert to mp3 | mp4 | wav | flac')
    exit()

#Uploads file from Audio
print('Uploading')
s3.upload_file(filePath,s3Bucket,fileName)

#Checks that file has been uploaded - I believe that this section is uneccessary
#but may be useful for longer upload times.
while False:
    s3.get_object(Bucket=s3Bucket,Key=fileName)
    print('Still uploading')
    time.sleep(5)

print('Starting Transcription')

### Audio Transcription Start ###

uri = 'https://s3-us-west-2.amazonaws.com/' + s3Bucket + '/' + fileName

print('Select speakers dialect. Options are US | AU | UK')
region = input()

print('How many speakers are in the file? Enter a numerical value between 1-10')
sNumber = int(input())
if sNumber > 1:
    print('Does each speaker have their own audio chanel? If unsure enter No.')
    qChannel = input()
    if qChannel != 'Yes' or 'yes':
        settingOptions = {
            'ChannelIdentification': False,
            'MaxSpeakerLabels': sNumber,
            'ShowSpeakerLabels': True
            }
    else:
         settingOptions = {
            'ChannelIdentification': True,
            'MaxSpeakerLabels': sNumber,
            'ShowSpeakerLabels': False
            }
else:
    settingOptions = {
        'ChannelIdentification': False,
        'ShowSpeakerLabels': False,
        }

transcribe = boto3.client('transcribe')
job_name = fileName
job_uri = uri
transcribe.start_transcription_job(
    TranscriptionJobName=job_name,
    Media={'MediaFileUri': job_uri},
    MediaFormat=fileExt,
    LanguageCode='en-' + region.upper(),
    Settings=settingOptions
)
while True:
    status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
    if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
        break
    print("Not ready yet...")
    time.sleep(5)
print(status)