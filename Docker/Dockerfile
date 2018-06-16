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
    vim python python-pip libncurses-dev libz-dev

# setup llvm 6.0
RUN apt-get -y install wget apt-utils software-properties-common python-software-properties
RUN wget -O - https://apt.llvm.org/llvm-snapshot.gpg.key | apt-key add -
RUN echo "deb http://apt.llvm.org/xenial/ llvm-toolchain-xenial-6.0 main" >> /etc/apt/sources.list

# COPY sources.list /etc/apt/sources.list

# Setup packages.
RUN apt-get update && apt-get -y install llvm-6.0 llvm-6.0-dev llvm-6.0-runtime \
    clang-6.0
    
RUN ln -s /usr/bin/clang++-6.0 /usr/bin/clang++ 
RUN ln -s /usr/bin/clang-6.0 /usr/bin/clang
RUN ln -s /usr/include/llvm-6.0/llvm/ /usr/include/llvm
RUN ln -s /usr/include/llvm-c-6.0/llvm-c/ /usr/include/llvm-c

# get sources
RUN git clone https://github.com/Mithrilwoodrat/naivecompiler.git -b llvm-6.0 /opt/naivecompiler

WORKDIR /opt/naivecompiler

RUN pip install -r requirements.txt

# build backend
RUN sh build.sh
RUN chmod +x test.sh