# nagios-datacentre-checks

Nagios checks for environmental and power monitoring that might be useful in a datacentre.

## check_onewire_temperatures

<pre>
usage: check_onewire_temperatures [-h] [--low-warning DEGREES]
                                  [--low-critical DEGREES]
                                  [--high-warning DEGREES]
                                  [--high-critical DEGREES] [--owfs-path PATH]

Check that no one-wire sensors in the given owfs path are over or under the
threshold temperatures. Michael Fincham &lt;michael.fincham@catalyst.net.nz&gt;.

optional arguments:
  -h, --help            show this help message and exit
  --low-warning DEGREES
                        temperature in degrees Celsius for low-warning state,
                        defaults to 10
  --low-critical DEGREES
                        temperature in degrees Celsius for low-critical state,
                        defaults to 0
  --high-warning DEGREES
                        temperature in degrees Celsius for high-warning state,
                        defaults to 35
  --high-critical DEGREES
                        temperature in degrees Celsius for high-critical
                        state, defaults to 40
  --owfs-path PATH      path to owfs filesystem, defaults to /srv/owfs
</pre>

## check_onewire_buses

Requirements: check_onewire_temperatures

<pre>
usage: check_onewire_buses [-h] [--owfs-path PATH]
                           [--expected-bus-count COUNT]

Check that at least one one-wire temperature sensor responds on each bus of
the given owfs path. Michael Fincham &lt;michael.fincham@catalyst.net.nz&gt;.

optional arguments:
  -h, --help            show this help message and exit
  --owfs-path PATH      path to owfs filesystem, defaults to /srv/owfs
  --expected-bus-count COUNT
                        expected number of buses to find, defaults to 2
</pre>

## check_ups

Requirements: [snimpy](https://pypi.python.org/pypi/snimpy)

`/etc/ups-monitoring.conf` must exist and be filled with values provided by your UPS vendor and local power operator. The plugin will not return useful results until this is done.

<pre>
usage: check_ups [-h] [--configuration-file FILE]
                 {alarms,temperature,input,output}

Check various aspects of an SNMP UPS. Michael Fincham
&lt;michael.fincham@catalyst.net.nz&gt;.

positional arguments:
  {alarms,temperature,input,output}
                        which check to run

optional arguments:
  -h, --help            show this help message and exit
  --configuration-file FILE
                        path to configuration file, defaults to /etc/ups-
                        monitoring.conf
</pre>
