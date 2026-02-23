# Lenovo Power Control (Linux)

A lightweight, native graphical utility to toggle the "Conservation Mode" (80% battery charge limit) on Lenovo Ideapad laptops running Linux.

## The Hardware Problem
By default, the Linux kernel generic battery drivers do not always successfully bind to the ACPI signatures of newer Lenovo motherboards (such as the Ideapad Slim 3i with Intel 13th Gen processors). 

Because the `ideapad_laptop` module fails to bind, standard power management tools cannot see the battery threshold controls. However, the hardware switch still exists directly on the PCI bus under the VPC2004 virtual power controller node.

This application acts as a direct bridge, using `pkexec` to securely inject the ACPI status command directly into the motherboard firmware via `/sys/devices/pci0000:00/0000:00:1f.0/PNP0C09:00/VPC2004:00/conservation_mode`.

## Features
* **Direct Firmware Access:** Bypasses failing generic kernel modules.
* **Native Security:** Uses PolicyKit (`pkexec`) for secure, native OS password prompts.
* **Custom UI:** Borderless window design with absolute-coordinate center-screen mapping.

## Developer
Developed by Md Shoaib Mahmud.
[Visit shoaib.pro.bd](http://shoaib.pro.bd)