# Run the jobs

* To run the jobs in the background, use the `screen` tool to iniate a detachable screen with `$ screen`, to name the screen session `$ screen -S <session name>`.
* To kill the session, run `$ screen -XS <session id> quit`, for the session ID's `$ screen -ls`.

* To run the jobs in the background, use the tool "no hangup" `$ nohup`
```
$ nohup bash <path/to/shell script> > output.log 2>&1 &
```

* Graph runner - https://github.com/snap-contrib/cwl-snap-graph-runner