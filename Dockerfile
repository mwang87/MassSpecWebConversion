FROM chambm/pwiz-skyline-i-agree-to-the-vendor-licenses:3.0.19056-6b6b0a2b4

MAINTAINER Mingxun Wang "mwang87@gmail.com"

RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential

RUN pip install ftputil
RUN pip install flask
RUN pip install gunicorn
RUN pip install requests

RUN apt-get install -y r-base-core
RUN apt-get install -y libcurl4-openssl-dev
RUN apt-get install -y libnetcdf-dev
RUN apt-get install -y libssl-dev
RUN R -e "install.packages('remotes', repos = 'http://cran.us.r-project.org')"
RUN R -e "install.packages('data.table', repos = 'http://cran.us.r-project.org')"
RUN R -e "install.packages('ggplot2', repos = 'http://cran.us.r-project.org')"
RUN apt-get install -y libgomp1
RUN R -e "install.packages('mzR', repos = 'http://cran.us.r-project.org')"
RUN R -e "install.packages('shiny', repos = 'http://cran.us.r-project.org')"
RUN R -e "install.packages('dplyr', repos = 'http://cran.us.r-project.org')"
RUN R -e "remotes::install_github('chasemc/mzPlotter')"
RUN apt-get install -y pandoc

#RUN useradd mingxun
#USER mingxun

COPY . /app
WORKDIR /app
