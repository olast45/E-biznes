FROM ubuntu:24.04

# Python 3.10
RUN apt update && apt install -y software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt update \
    && apt install -y python3.10 python3.10-venv python3.10-dev

# Java 8
RUN apt update && apt install -y \
    curl zip unzip git openjdk-8-jdk \
    && rm -rf /var/lib/apt/lists/*

# Gradle and Kotlin via SDKMAN
ENV DEBIAN_FRONTEND=noninteractive

RUN curl -s "https://get.sdkman.io" | bash

RUN bash -c 'source $HOME/.sdkman/bin/sdkman-init.sh && sdk install gradle && sdk install kotlin'

ENV PATH=$PATH:/root/.sdkman/candidates/gradle/current/bin:/root/.sdkman/candidates/kotlin/current/bin

WORKDIR /my-app

COPY . .

CMD ["gradle", "run", "--warning-mode", "none"]
