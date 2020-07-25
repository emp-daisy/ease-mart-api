FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN python3 -m pip install --user --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5051

CMD ["python", "app.py"]