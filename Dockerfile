FROM python:3.8.5-slim-buster

WORKDIR /app

# Prevent Python from generating .pyc files
ENV PYTHONGDONTWRITEBYTECODE 1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

# Install pip requirements
COPY requirements.txt setup.py ./

RUN python -m pip install -r requirements.txt && \
  python setup.py install

# RUN python -m pip install -r requirements.txt
# Install Git and Vim
RUN apt-get update && \
  apt-get install -y gcc && \
  apt-get install -y git vim

# Generate deposit keys using Ethereum Foundation deposit tool
RUN git clone https://github.com/ethereum/eth2.0-deposit-cli.git && \
  cd eth2.0-deposit-cli && \
  chmod a+x ./deposit.sh

# Save validator mnemonic keystore files

WORKDIR /launcher/eth2.0-deposit-cli

CMD ["./deposit.sh install"]

# Prevent Docker container from stopping after running it
ENTRYPOINT ["tail", "-f", "/dev/null"]
