#!/bin/bash

docker run -p 9000:9000 olast45/olast-ebiznes-ex2:latest

ngrok http 9000

