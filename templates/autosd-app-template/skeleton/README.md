# ${{values.component_id}}

${{values.description}}

## About this example

This example project demonstrates how AutoSD effectively constrains the memory
usage in the QM partition, while avoiding interferences outside of it.

The example includes performance monitoring features both embedded in the image,
and as external containers that can be brought up using compose.

## Architecture

This demo features two containerized agents that communicate
between each other through a UNIX socket at `/run/ipc/ffi_server.socket`.

<div align="center">
    <img src="./docs/img/diagram.png" />
</div>


### Listener agent

On the one hand, we have a listener agent that will remain actively
listening on `/run/ipc/ffi_server.socket`. The container resides in the
outside the qm partition.

The agent merely listens and prints the received memory dump data.
It shall not lose any message, be interrupted, or killed by the supervisor.

### Malicious agent

On the other hand, we have an agent in the QM partition that connects to the
listener outside that partition. It consumes chunks of memory, and sends
its latest memory consumption data through the UNIX socket.

Memory consumption of this service is limited to 50% of the available memory.
