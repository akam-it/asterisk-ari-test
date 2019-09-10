# Building container
docker build -t test-task github.com/akam-it/asterisk-ari-test

# Starting container
docker run --rm --network=host --name test-task -d test-task

# How to
After container is running, connect to asterisk ip with following credentials:
100:Do7eifoz
200:Do7eifoz
300:Do7eifoz

Try to call to 300, 200 should ringing.
