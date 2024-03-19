FROM python:3.9
WORKDIR /ai-api
COPY ./requirements.txt /ai-api/requirements.txt
COPY ./README.md /ai-api/README.md
COPY ./setup.py /ai-api/setup.py
COPY ./imagebind /ai-api/imagebind
RUN pip install .
COPY . .
CMD python -m uvicorn app.main:app --port ${PORT} --host 0.0.0.0