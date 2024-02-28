sudo docker image build -t flaskpy:v01 .
sudo docker container run -p 5000:5000 --rm -it flaskpy:v01
