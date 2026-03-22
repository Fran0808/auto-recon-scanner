FROM kalilinux/kali-rolling

RUN apt-get update && apt-get install -y \
    python3 \
    nmap \
    whois \
    whatweb \
    gobuster \
    dirb \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*

RUN wget https://github.com/Findomain/Findomain/releases/download/9.0.4/findomain-linux.zip \
    && unzip findomain-linux.zip \
    && mv findomain /usr/local/bin/findomain \
    && chmod +x /usr/local/bin/findomain \
    && rm findomain-linux.zip \
    && mkdir -p /usr/share/wordlists/dirb \
    && wget https://raw.githubusercontent.com/v0re/dirb/master/wordlists/common.txt -O /usr/share/wordlists/dirb/common.txt

WORKDIR /scanner

COPY . /scanner

RUN chmod +x scripts/*.sh

ENTRYPOINT ["python3", "app/main.py"]
