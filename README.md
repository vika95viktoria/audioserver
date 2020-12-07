# Speech recognition simple web app

Speech-recognition application build with Flask, using GCP infrastracture: Google Speech to text API, Google bucket storage, Google Cloud Run

# Deploy to cloud
```
gcloud builds submit --tag gcr.io/language-detection-247210/audio-server  --timeout=9000s
gcloud run deploy audio-server --image gcr.io/language-detection-247210/audio-server --platform managed --memory 1Gi
```
