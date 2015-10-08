# knob
A Django application that performs remote configurations on multiple devices, distributing the operations using python multiprocessing library.

## Current version
* supports both Telnet and SSH
* A wizard that accepts common credentials, a list of IPs, and a list of commands to be executed on every device on the list.
* Sends a log email to the system admin, indicating both the errors and success operations.
* Providing an option to use a full Python environment. That makes it easy to perform more complex operations like doing regex operations and conditional decisions on the output.

## Future work
* Accepts CSV file(s) as input.

* Better documentation :)
