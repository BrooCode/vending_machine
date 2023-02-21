#!/home/ubuntu/
cd internship

docker stop app2
echo "y" |docker system prune -a
docker build -t app2 .
docker run -d -p 5050:5050 --name app2 app2
