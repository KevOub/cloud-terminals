
# The commands used to build

## Build
`docker build . -t $CONTAINER:latest --build-arg MYPORT=8081`

### Run
`docker run --env MYPORT=8082 --rm -it -p $PORT:$PORT CONTAINER:test ttyd -p $PORT $SHELL`

### Stop
`docker stop $CONTAINER`