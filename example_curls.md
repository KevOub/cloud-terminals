```bash
(venv) kevin@localhost ~/D/c/p/cloud-terminals> curl -X POST -d "container-name=levels" localhost:5000/build/dockerfile        
levels%                                                                                                                              /0.9s
```
POST to /build/dockerfile -> CONTAINER_NAME

```bash
(venv) kevin@localhost ~/D/c/p/cloud-terminals> curl -X POST -d "container-name=levels&container-user=0&container-shellp=login" localhost:5000/run/dockerfile
levels
43965
1aa8a5b7a8cbfd26a6b594e0bbf08df6fcdef0542ca21501480af68065e3e9c5%                                                                    /0.5s
```
POST to /run/dockerfile -> CONTAINER_NAME, PORT, CONTAINER_ID

```bash
(venv) kevin@localhost ~/D/c/p/cloud-terminals> curl -X POST -d "container-id=97b96d2a28a96275c961020895fc2e6a102c0682be714f0ab357a001b9d47140" localhost:5000/data/dockerfile
// docker inspect.
```
POST to /data/dockerfile -> a bunch of data regarding that image

```bash
(venv) kevin@localhost ~/D/c/p/cloud-terminals> curl -X POST -d "container-id=97b96d2a28a96275c961020895fc2e6a102c0682be714f0ab357a001b9d47140" localhost:5000/stop/dockerfile
97b96d2a28a96275c961020895fc2e6a102c0682be714f0ab357a001b9d47140%                                                                    /0.2s
```
POST to /stop/dockerfile -> runs `docker stop CONTAINER_ID`
