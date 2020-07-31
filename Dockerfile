FROM python:3.8.5-slim-buster

WORKDIR /app

# Install Git and Vim
RUN apt-get update && \
  apt-get install -y gcc && \
  apt-get install -y git vim

# Generate deposit keys using Ethereum Foundation deposit tool
RUN git clone https://github.com/ethereum/eth2.0-deposit-cli.git && \
  cd eth2.0-deposit-cli && \
  python -m pip install -r requirements.txt && \
  python setup.py install && \
  chmod a+x ./deposit.sh

WORKDIR /app/eth2.0-deposit-cli

CMD ["./deposit.sh install"]

# Prevent Docker container from stopping after running it
ENTRYPOINT ["tail", "-f", "/dev/null"]
