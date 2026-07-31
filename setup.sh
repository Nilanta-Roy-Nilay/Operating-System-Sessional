#!/bin/bash

sudo -v

sudo apt update && sudo apt upgrade -y

sudo snap install code --classic
sudo snap install sublime-text --classic

sudo apt install -y codeblocks

sudo apt install -y build-essential openjdk-17-jdk pypy3 python-is-python3

echo "setup complete"
echo "version check"

g++ --version && javac --version && python --version

