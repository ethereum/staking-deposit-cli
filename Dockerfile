FROM python:3.7-alpine

WORKDIR /app

COPY requirements.txt setup.py ./

COPY eth2deposit ./eth2deposit

RUN apk add --update gcc libc-dev linux-headers

RUN pip3 install -r requirements.txt

RUN python3 setup.py install

ARG cli_command

ENTRYPOINT [ "python3", "./eth2deposit/deposit.py" ]

CMD [ $cli_command ]
