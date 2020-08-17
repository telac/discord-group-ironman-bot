FROM python:3.7-slim-stretch

ADD is_ironman.py root/
ADD conf.ini root/

RUN pip3 install discord.py
RUN pip3 install requests
RUN pip3 install bs4
WORKDIR root
CMD ["python3", "is_ironman.py"]
