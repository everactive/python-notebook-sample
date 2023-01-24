#!/bin/bash

echo "Everactive ENV+ EvalKit Exploration Notebook (Dockerized)"
echo ""

# Pull Everactive API credentials if available as environs.
CLIENT_ID="${EVERACTIVE_CLIENT_ID:-''}"
CLIENT_SECRET="${EVERACTIVE_CLIENT_SECRET:-''}"

# Start a Docker container with the current repo directory mounted as a volume.
echo "Starting Docker container..."
CONTAINER_ID=`docker run -it -d --rm \
    --name everactive-envplus-sample-notebook \
    -p 8888:8888 \
    --env EVERACTIVE_CLIENT_ID=${CLIENT_ID} \
    --env EVERACTIVE_CLIENT_SECRET=${CLIENT_SECRET} \
    -v $PWD:/repo \
everactive-envplus bash` > /dev/null

# Install notebook dependencies via the poetry and create an ipykernel for the
# Jupyterlab notebook.
echo "Installing dependencies with poetry..."
docker exec $CONTAINER_ID bash -c 'cd /repo; poetry install' > /dev/null 2>&1

echo "Creating ipykernel for notebook use..."
docker exec $CONTAINER_ID bash -c 'cd /repo; poetry run python -m ipykernel install --user --name=everactive-envplus' > /dev/null 2>&1

# Start Jupyterlab.
echo "Starting JupyterLab..."
docker exec $CONTAINER_ID bash -c 'cd /repo; jupyter lab --ip=0.0.0.0 --no-browser --allow-root &' > /dev/null 2>&1

# Pull out running notebook token and display localhost URL for user.
RUNNING_LAB="$(docker exec $CONTAINER_ID bash -c 'jupyter lab list 2>&1')"
RUNNING_LAB=$(echo $RUNNING_LAB | tr '\n' ' ')

TOKEN_REGEX=".*token=([[:alnum:]]+)[[:space:]]+"
echo ""

if [[ $RUNNING_LAB =~ $TOKEN_REGEX ]]
then
    echo "Copy and and paste this URL into your web browser to access JupyterLab:"
    echo "http://127.0.0.1:8888/lab?token=${BASH_REMATCH[1]}"
else
    echo "Could not get JupyterLab localhost URL."
fi

echo ""
read -p "Press ENTER to stop JupyterLab and stop the Docker container."

# Stop the Docker container.
echo ""
echo "Stopping JupyterLab and Docker container..."
docker container stop $CONTAINER_ID  > /dev/null

echo "Done."