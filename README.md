MX Robot Library
================

This library was written to interface with the Irelec Isara2 robot and provides a Python interface to the command and control layers provided by Irelec.

While not currently in use, this will be deployed to the MX3 beamline at the Australian Synchrotron during hot commisioning.

This library is heavilly customised for the MX3 beamline, as each Irelec robot is unique, different options may be present or disabled and firmware may be customised for your specific beamline.

While we welcome questions and suggestions, please understand that we are currently very busy with MX3 as we near first light.

This library while fully functional per MX3's needs, may not be suitable for your beamlines specific needs, as this library does not integrate with either EPICS or Tango.

We currently consider this library as being a beta product, as it has not been rigorously tested on an active beamline and we do not currently recommed using this library in a production environment.

Examples on how to use this library can be found in [mx_robot_library/examples](https://github.com/AustralianSynchrotron/mx-robot-library/tree/main/examples).

The MX Robot Library is provided as opensource software, released under [GPL v3.0](https://github.com/AustralianSynchrotron/mx-robot-library/blob/main/LICENSE).
