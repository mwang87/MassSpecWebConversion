build:
	docker build -t conversion .

clean:
	docker rm conversion |:

development: clean
	docker run -it -p 5050:5009 --name conversion conversion /app/run_dev_server.sh
	#docker run -it -p 5050:5009 -v $(PWD)/output:/output --name conversion conversion /app/run_dev_server.sh

server: clean
	docker run -d -p 5050:5000 -v $(PWD)/output:/output --name conversion conversion /app/run_server.sh

interactive: clean
	docker run -it -p 5050:5000 -v $(PWD)/output:/output --name conversion conversion /app/run_server.sh

bash: clean
	docker run -it -p 5050:5000 -v $(PWD)/output:/output --name conversion conversion bash

attach:
	docker exec -i -t conversion /bin/bash
