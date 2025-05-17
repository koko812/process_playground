FROM ubuntu

RUN apt update && \
    apt install -y \
        libfuse2 \
        python3 \
        python3-pip \
        vim && \
    pip3 install fusepy --break-system-packages

# デフォルトで入れるとラク
WORKDIR /mnt/test
 
