# Speech recognition simple web app

Speech-recognition application built with Flask, using GCP infrastracture: Google Speech to text API, Google bucket storage, Google Cloud Run

# Deploy to cloud
```
gcloud builds submit --tag gcr.io/{projectid}/audio-server 
gcloud beta run deploy audio-server --image gcr.io/{projectid}/audio-server --platform managed --memory 1Gi --timeout=3600s
```
