FROM apache/airflow:3.1.0-python3.10

# ----------------------------------------------------
# 1. Dependências de sistema (como ROOT)
# ----------------------------------------------------
USER root

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        openjdk-17-jdk \
        python3-dev \
        curl \
        wget \
        build-essential \
        cmake \
        libsnappy-dev \
        liblz4-dev \
        libzstd-dev \
        libbz2-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# ----------------------------------------------------
# 2. Spark
# ----------------------------------------------------
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV SPARK_VERSION=3.5.7
ENV HADOOP_VERSION=3
ENV SPARK_HOME=/opt/spark
ENV PATH=$SPARK_HOME/bin:$PATH

RUN wget -q https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz && \
    tar -xzf spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz -C /opt && \
    mv /opt/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} /opt/spark && \
    rm spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz

# ----------------------------------------------------
# 3. VOLTA PARA AIRFLOW (NUNCA MAIS ROOT)
# ----------------------------------------------------
USER airflow

# ----------------------------------------------------
# 4. Pacotes Python (OBRIGATORIAMENTE como airflow)
# ----------------------------------------------------
RUN pip install --no-cache-dir \
    pyspark \
    pandas \
    numpy \
    pyarrow==15.0.2 \
    scikit-learn \
    apache-airflow-providers-apache-spark
