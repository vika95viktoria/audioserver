FROM python:alpine3.7
COPY . /app
WORKDIR /app
RUN apk add ffmpeg bash libxml2-dev libxslt-dev libffi-dev gcc linux-headers musl-dev build-base
RUN pip install flask pydub wave google-cloud-storage python-docx pyyaml google-cloud-speech
EXPOSE 8080
ENTRYPOINT [ "python" ]
CMD [ "controller.py" ]