test ci-test: test_services validate_elasticsearch_running validate_gandalf_running
	@PYTHONPATH=.:$$PYTHONPATH coverage run --branch `which nosetests` -vv --with-yanc -s tests/
	@coverage report -m

test_services: drop redis mongo gandalf

tox:
	@PYTHONPATH=.:$$PYTHONPATH PATH=$$PATH:~/.pythonbrew/pythons/Python-2.6.*/bin/:~/.pythonbrew/pythons/Python-2.7.*/bin/:~/.pythonbrew/pythons/Python-3.0.*/bin/:~/.pythonbrew/pythons/Python-3.1.*/bin/:~/.pythonbrew/pythons/Python-3.2.3/bin/:~/.pythonbrew/pythons/Python-3.3.0/bin/ tox

tox26:
	@PYTHONPATH=.:$$PYTHONPATH PATH=$$PATH:~/.pythonbrew/pythons/Python-2.6.*/bin/:~/.pythonbrew/pythons/Python-2.7.*/bin/:~/.pythonbrew/pythons/Python-3.0.*/bin/:~/.pythonbrew/pythons/Python-3.1.*/bin/:~/.pythonbrew/pythons/Python-3.2.3/bin/:~/.pythonbrew/pythons/Python-3.3.0/bin/ tox -e py26

tox27:
	@PYTHONPATH=.:$$PYTHONPATH PATH=$$PATH:~/.pythonbrew/pythons/Python-2.6.*/bin/:~/.pythonbrew/pythons/Python-2.7.*/bin/:~/.pythonbrew/pythons/Python-3.0.*/bin/:~/.pythonbrew/pythons/Python-3.1.*/bin/:~/.pythonbrew/pythons/Python-3.2.3/bin/:~/.pythonbrew/pythons/Python-3.3.0/bin/ tox -e py27

tox33:
	@PYTHONPATH=.:$$PYTHONPATH PATH=$$PATH:~/.pythonbrew/pythons/Python-2.6.*/bin/:~/.pythonbrew/pythons/Python-2.7.*/bin/:~/.pythonbrew/pythons/Python-3.0.*/bin/:~/.pythonbrew/pythons/Python-3.1.*/bin/:~/.pythonbrew/pythons/Python-3.2.3/bin/:~/.pythonbrew/pythons/Python-3.3.0/bin/ tox -e py33

toxpypy:
	@PYTHONPATH=.:$$PYTHONPATH PATH=$$PATH:~/.pythonbrew/pythons/Python-2.6.*/bin/:~/.pythonbrew/pythons/Python-2.7.*/bin/:~/.pythonbrew/pythons/Python-3.0.*/bin/:~/.pythonbrew/pythons/Python-3.1.*/bin/:~/.pythonbrew/pythons/Python-3.2.3/bin/:~/.pythonbrew/pythons/Python-3.3.0/bin/ tox -e pypy

setup:
	@pip install -e .\[tests\]

run:
	@PYTHONPATH=.:./tests/:$$PYTHONPATH python tests/sandbox/server.py --port 4444 --workers 1 --bind 0.0.0.0 --conf ./tests/sandbox/config/local.conf -vvv --debug

validate_elasticsearch_running:
	@if [ "`curl -sv http://localhost:9200/ 2>&1 | grep 'Connection refused'`" != "" ]; then echo "\nERROR:\n\nElasticSearch must be running. Please make sure you can run it before running cow tests.\n" && exit 1; fi

validate_gandalf_running:
	@if [ "`curl -sv http://localhost:8001/ 2>&1 | grep 'Connection refused'`" != "" ]; then echo "\nERROR:\n\nGandalf must be running. Please make sure you can run it before running cow tests.\n" && exit 1; fi

kill_redis:
	-redis-cli -p 7575 shutdown

redis: kill_redis
	redis-server ./redis.conf; sleep 1
	redis-cli -p 7575 info > /dev/null

kill_elasticsearch:
	-@pkill -F elasticsearch.pid

elasticsearch: kill_elasticsearch
	@elasticsearch -d -p elasticsearch.pid

kill_mongo:
	@ps aux | awk '(/mongod.+test/ && $$0 !~ /awk/){ system("kill -9 "$$2) }'
	@rm -rf /tmp/cow_test/mongodata

mongo: kill_mongo
	@rm -rf /tmp/cow_test/mongotestdata && mkdir -p /tmp/cow_test/mongotestdata
	@mongod --dbpath /tmp/cow_test/mongotestdata --logpath /tmp/cow_test/mongotestdata/mongotestlog --port 4445 --quiet --smallfiles --oplogSize 128 &

drop:
	@mysql -u root -e "DROP DATABASE IF EXISTS test_cow; CREATE DATABASE IF NOT EXISTS test_cow"

gandalf: kill_gandalf
	@gandalf-server -config="./gandalf.conf" &

kill_gandalf:
	@-ps aux | egrep -i 'gandalf-server.+conf' | egrep -v egrep | awk '{ print $$2 }' | xargs kill -9
