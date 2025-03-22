FROM ubuntu:24.04

RUN apt update && apt install -y \
    curl zip unzip git openjdk-11-jdk \
    && rm -rf /var/lib/apt/lists/*

RUN curl -s "https://get.sdkman.io" | bash

RUN bash -c 'source $HOME/.sdkman/bin/sdkman-init.sh && sdk install scala && sdk install sbt'

ENV PATH=$PATH:/root/.sdkman/candidates/scala/current/bin:/root/.sdkman/candidates/sbt/current/bin

WORKDIR /my-app

COPY . .
RUN sbt compile

EXPOSE 9000

CMD ["sbt", "run"]