FROM python:3.13
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN apt-get update && apt-get install -y locales && rm -rf /var/lib/apt/lists/*
RUN locale-gen en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US:en
ENV LC_ALL=en.UTF-8
ENV PYTHONIOENCODING=utf-8
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
COPY main.py /app
COPY spamclass.keras /app           
CMD ["fastapi", "run", "/app/main.py", "--port", "8000"]