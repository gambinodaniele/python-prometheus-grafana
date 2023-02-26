https://nordicapis.com/how-to-monitor-rest-apis-using-prometheus-and-grafana/

# Prometheus Setup (basic = only prometheus service) #
creare docker-composer.yml file:
-------------------------------------
version: "3"  
services:  
  prometheus:
    image: prom/prometheus:latest
    ports:
    - 9090:9090
-------------------------------------

# Start, Stop, Delete Containers
$docker-compose up
docker-compose down
docker-compose rm

# Test - Web Console #
https://localhost:9090 

# Test - View metrics (related only to prometheus service => 'job_name: prometheus')
# by default scrape_interval: 15s and scrape_timeout: 10s
https://localhost:9090/metrics

# Updating Volume Path for Prometheus #
Add the below line "volumes: ..." at the end of docker-composer.yml:
docker-composer.yml
-------------------------------------
version: "3"  
services:
 prometheus:
      image: prom/prometheus:latest
      ports:
      - 9090:9090
      volumes:
      - "./prometheus.yml:/etc/prometheus/prometheus.yml"
------------------------------------

# Create a new file 'prometheus.yml'
prometheus.yml
-------------------------------------
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: prometheus
    static_configs:
      - targets: ["172.24.55.140:9090"]   
      # - targets: ["localhost:9090"]   
-------------------------------------
WARNING: use $ipconfig to retrieve the local ip (es. '172.24.55.140')

# Creating a Flask App
Create dir ./flask_api
Create inside ./flask_api the file:
    - Dockerfile (to install modules Flask and flask_prometheus_metrics and app image)
    - app.py 

# Add Flask App to docker-composer.yml file
-------------------
app:
      container_name: app
      build: ./flask_api/.
      ports:
      - "5000:5000"
      volumes:
      - "./flask_api/app.py:/app.py"
-------------------

# Client test
curl -X POST http://localhost:5000/post -d "{\"text\": \"daniele\"}"
curl -X GET http://localhost:5000/

# metrics
http://localhost:9090/metrics //prometheus
http://localhost:5000/metrics //app

app_request_latency_seconds_count{endpoint="/post",method="POST"} 
