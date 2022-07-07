all: database-install database-deploy

release=$(shell lsb_release -cs)

database-install:
	echo "Install Redis"
	echo "Release = $(release)"
	curl -fsSL https://packages.redis.io/gpg | sudo gpg --batch --yes --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg
	echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(release) main" | sudo tee /etc/apt/sources.list.d/redis.list
	sudo apt-get -y update
	sudo apt-get -y upgrade
	sudo apt-get install python3 redis git
	pip3 install flask
	pip3 install redis
	sudo mkdir /opt/nuoj-database/
	sudo git clone https://github.com/ntut-xuan/NuOJ-Database.git /opt/nuoj-database/
	sudo chmod -R 647 /opt/nuoj-database/*
	sudo cp /opt/nuoj-database/nuoj-database.service /etc/systemd/system/
	sudo chmod 647 /etc/systemd/system/nuoj-database.service
	sudo systemctl daemon-reload
	sudo systemctl enable nuoj-database
	sudo systemctl start nuoj-database

database-deploy:
	sudo python3 /opt/nuoj-database/setup_database.py