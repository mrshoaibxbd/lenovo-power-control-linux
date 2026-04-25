# ⚡ Lenovo Power Control (Linux)

A native, highly optimized GTK3 monitoring dashboard and ACPI firmware bridge for Lenovo hardware (e.g., Ideapad Slim 3i).

Standard Linux kernel drivers (`ideapad_laptop`) often fail to bind to the specific ACPI signatures of newer Lenovo motherboards. This utility acts as a direct bridge to the hardware's `VPC2004` node, allowing users to toggle **Conservation Mode** (limiting battery charge to 80% to vastly extend lithium-ion cell longevity) without relying on generic drivers.

### 🚀 v1.4.2 Architectural Upgrades
* **Engine Rebuild:** Fully refactored from Tkinter to native Python GTK3 bindings (`PyGObject`) for hardware-composited rendering and stability.
* **Tactical Glassmorphism:** Implemented a solid dark-mode gradient UI utilizing GTK CSS.
* **Advanced Telemetry:** Integrated `upower` daemon parsing via background threading to display real-time voltage, charge cycles, and energy metrics without UI freezing.
* **Native Integration:** Bundled as a system-wide Debian (`.deb`) package with custom icons and PolicyKit (`pkexec`) security escalation.

### 🛠️ Dependencies
This utility requires the following Linux bridging tools:
```bash
sudo apt install python3-gi upower policykit-1
# Installation 
Download the compiled .deb package from the Releases page and install it natively

sudo dpkg -i lenovo-power-control_1.4.2_amd64.deb
sudo apt-get install -f # Resolves any missing dependencies automatically
