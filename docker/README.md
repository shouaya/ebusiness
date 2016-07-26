docker

---

# build

```sh
docker build --tag ebusinessdocker/sales .
```

# run

```sh
docker run -d -p 8080:80 --name sales --restart=always ebusinessdocker/sales
```
