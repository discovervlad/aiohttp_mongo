FROM python:3.7
COPY app.py /
COPY requirements.txt /
RUN pip install -r requirements.txt
CMD [ "python", "-u", "app.py" ]
