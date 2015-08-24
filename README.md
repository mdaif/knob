# knob
A Django application that performs remote configurations on multiple devices, distributing the operations using celery workers

## Current version
* supports Telnet
* A wizard that accepts common credentials, a list of IPs, and a list of commands to be excuted on every device on the list.
* Sends a log email to the system admin, indicating both the errors and success operations.

## Future work
* Support for both Telnet and SSH
* Accepts CSV file(s) as input.
* Providing an interface that accepts python DSL in order to perform regex, loops and conditions.
* Better documentation :)
