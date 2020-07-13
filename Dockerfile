FROM joyzoursky/python-chromedriver:3.7-selenium

COPY requirements.txt /requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY python-instagram-bot python-instagram-bot

ENV PYTHONPATH "${PYTONPATH}:/python-instagram-bot"

CMD ["python", "./python-instagram-bot/main.py"]