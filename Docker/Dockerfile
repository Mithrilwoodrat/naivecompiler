FROM        ubuntu:16.04
MAINTAINER  Mithrilwoodrat <mithrilwoodrat@gmail.com>

# Setup environment.
# ENV PATH /opt/llvm/bin:$PATH

# Default command on startup.
CMD bash

# community source
COPY sources.list /etc/apt/sources.list

# Setup packages.
RUN apt-get update && apt-get -y install cmake git build-essential \
    vim python python-pip llvm-3.8 llvm-3.8-dev llvm-3.8-runtime \
    clang libncurses-dev libz-dev

# get sources
RUN git clone https://github.com/Mithrilwoodrat/naivecompiler.git /opt/naivecompiler

WORKDIR /opt/naivecompiler

RUN pip install -r requirements.txt

# build backend
RUN sh build.sh
RUN chmod +x test.sh