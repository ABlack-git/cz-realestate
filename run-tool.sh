set -e
unset http_proxy
unset https_proxy
# Workaround for cron, won't work on other systems
export PATH=/usr/local/Caskroom/miniconda/base/condabin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin

CONTAINER_NAME=cz-realestate-mongo
PROJECT_NAME=cz_realestate

function clean_up() {
  echo "Stopping docker container(s)"
  # add if CID is not empty
  docker-compose -f docker/docker-compose.yml -p ${PROJECT_NAME} stop
}
trap clean_up EXIT

## create/update env
if [[ ! -d .venv ]]; then
  echo "Creating virtual environment"
  make create-env
#else
#  echo "Updating conda environment"
#  make update-env
fi

## activate env
echo "Activating virtual environment environment"
source .venv/bin/activate
echo "Using virtualenv ${VIRTUAL_ENV}"
echo "Using python from $(which python)"

## start docker
CID=$(docker ps -q -f status=running -f name=${CONTAINER_NAME})
if [[ -z ${CID} ]]; then
  echo "Launching docker container"
  docker-compose -f docker/docker-compose.yml -p ${PROJECT_NAME} up -d
  echo "I will sleep for 10 seconds now"
  sleep 10
  echo "Resuming"
  CID=$(docker ps -q -f status=running -f name=${CONTAINER_NAME})
  echo "Docker container was started with ID ${CID}"
else
  echo "Docker container ${CONTAINER_NAME} was running with ID ${CID}"
fi

## start tool
echo "Starting tool"
if [[ ! -d logs ]]; then
  echo "Creating logs directory in ${PWD}"
  mkdir logs
fi

LOGFILE_PATH="$(pwd)/logs/$(date +'%Y-%m-%d-%H%M')-log.txt"
echo "LOGFILE_PATH: ${LOGFILE_PATH}"

cd cz_realestate
scrapy crawl bezrealitky_prague_rents -L INFO --logfile="${LOGFILE_PATH}"
cd ..

clean_up
