## apko symlink permission issue

My goal is to build a base image which contains a symlink from
`/opt/default.properties` to `/mnt/config/default.properties`
with `644` permissions and owned by `65532`.

While I can get the `/mnt/config/default.properties` file with the right permissions, I can't seem to get `/opt/default.properties` to match.

## Run
Build and run the example image:
```sh
./run.sh
```

```sh
1ba18578e9b9:/# ls -al /opt/
total 8
drwxr-xr-x    2 65532    65532         4096 Jul  8 00:25 .
drwxr-xr-x    1 root     root          4096 Jul 17 04:10 ..
lrwxrwxrwx    1 root     root            30 Jul  8 00:25 default.properties -> /mnt/config/default.properties

1ba18578e9b9:/# ls -al /mnt/config/
total 8
drw-r--r--    2 65532    65532         4096 Jan  1  1970 .
drw-r--r--    3 root     root          4096 Jan  1  1970 ..
-rw-r--r--    1 65332    65332            0 Jan  1  1970 default.properties
```
