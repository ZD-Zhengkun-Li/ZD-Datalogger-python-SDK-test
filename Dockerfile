#FROM node:8-alpine
#FROM armv7/armhf-ubuntu
#FROM balenalib/odroid-xu4-alpine-node
#FROM balenalib/odroid-xu4-ubuntu-node:8.15.1
FROM ubuntu:18.04

RUN apt update
RUN apt-get update
RUN apt install python3.9
RUN apt-get update && apt-get install -y \
    python3-pip
RUN apt-get update
