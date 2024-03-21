# Dockerfile
FROM python:3.9.18

WORKDIR /app

# Add the GDAL library
RUN apt-get update && apt-get install -y libgdal-dev && rm -rf /var/lib/apt/lists/*

# Set Gedal environment variables
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal


COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["tail", "-f", "/dev/null"]
# CMD streamlit run --server.port $PORT app.py
