# Cloud terminal!

This is a fun project meant for cyber.org and for anyone else interested in using docker containers in the web-browser. It utilizes https://github.com/tsl0922/ttyd ( I thought about re-writing a clone of this. It *only* takes me writing a proxy in golang between the frontend javascript library and the backend golang server that must also communicate (securely) with a terminal. However, this repository does everythng that I need :). Eventually, I will update it so it is not just the API explained below. This is a flask app that gives access to Docker image creation so take caution running it. 

How do I explain this? Simple. 
First, you upload either a `Dockerfile` or a `zip` folder which looks as follows
(Example of a ZIP folder. Also present under ./example)
```
.
..
Dockerfile
app/
anyotherdirneeded/
blah/
```


# The Endpoints and what they do
($VAR means variable)


## Upload (`/upload/dockerfile`)

(flask stuff)

REQUIRES:
1) A Dockerfile or a zip (as previously mentioned) 
2) `container-name` (it stores the container with this name and is the name used to lookup the Dockerfile for building) 

## Build (`/build/dockerfile`) 

`docker build uploads/$CONTAINER/ -t $CONTAINER:latest --build-arg MYPORT=8081`

REQUIRES:
1) `container-name` that corresponds to uploaded file in `uploads/`

## Run (`/run/dockerfile`)

`docker run --env MYPORT=$PORT --rm -it -p $PORT:$PORT CONTAINER:test ttyd -p $PORT -u $USER $SHELL`

REQUIRES:
1) `container-name` for the pre-built Dockerfile
2) `container-user` (I.E., root = 0: average user = 1000, etc.)
3) `container-shell` - either root, login, etc. the thing the user is prompted with


## Stop (`/stop/dockerfile`)

`docker stop $CONTAINER`

REQUIRES:
1) `container-id` (taken from docker ps or the eventual API return I write)

# What?

This is a proof of concept before I make an API (no gui) version. AKA, send data execute command etc.
