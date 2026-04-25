#!/usr/bin/env python3
import gi
import subprocess
import threading
import webbrowser
import os
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib

HW_PATH = "/sys/devices/pci0000:00/0000:00:1f.0/PNP0C09:00/VPC2004:00/conservation_mode"

class PowerDashboard(Gtk.Window):
    def __init__(self):
        super().__init__(title="Lenovo Power Intel")
        self.set_default_size(450, 580)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_decorated(False)
        self.set_keep_above(True)

        # Apply CSS
        self.load_css()
        self.get_style_context().add_class("glass-window")

        self.build_ui()
        self.start_telemetry_loop()
        
        # Explicitly initialize the switch state after building the UI
        GLib.idle_add(self.initialize_switch_state)

    def load_css(self):
        css_provider = Gtk.CssProvider()
        try:
            css_provider.load_from_path('glass_theme.css')
            Gtk.StyleContext.add_provider_for_screen(
                Gdk.Screen.get_default(),
                css_provider,
                Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
            )
        except Exception as e:
            print(f"CSS Error: {e}")

    def on_drag_press(self, widget, event):
        # Allows moving the undecorated window
        if event.button == 1:
            self.begin_move_drag(event.button, event.x_root, event.y_root, event.time)

    def build_ui(self):
        main_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add(main_vbox)

        # --- Draggable Header ---
        header_event = Gtk.EventBox()
        header_event.connect("button-press-event", self.on_drag_press)
        header_event.set_name("header-box")
        
        hbox_header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        hbox_header.set_margin_start(15)
        hbox_header.set_margin_end(15)
        
        title = Gtk.Label(label="⚡ LENOVO POWER CONTROL")
        title.set_name("title-label")
        
        close_btn = Gtk.Button(label="✕")
        close_btn.set_relief(Gtk.ReliefStyle.NONE)
        close_btn.connect("clicked", Gtk.main_quit)
        
        hbox_header.pack_start(title, False, False, 0)
        hbox_header.pack_end(close_btn, False, False, 0)
        header_event.add(hbox_header)
        main_vbox.pack_start(header_event, False, False, 0)

        # --- Telemetry Data (Scrollable) ---
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_margin_start(20)
        scrolled.set_margin_end(20)
        scrolled.set_margin_top(15)
        main_vbox.pack_start(scrolled, True, True, 0)

        self.grid = Gtk.Grid(row_spacing=12, column_spacing=20)
        self.grid.set_halign(Gtk.Align.CENTER)
        self.grid.set_name("data-grid")
        scrolled.add(self.grid)

        self.labels = {}
        keys = [
            "vendor", "model", "serial", "updated", "state", 
            "energy", "energy-full", "voltage", "charge-cycles", 
            "percentage", "capacity", "technology"
        ]
        
        for i, key in enumerate(keys):
            lbl_key = Gtk.Label(label=key.upper())
            lbl_key.set_halign(Gtk.Align.END)
            lbl_key.get_style_context().add_class("data-key")
            
            lbl_val = Gtk.Label(label="--")
            lbl_val.set_halign(Gtk.Align.START)
            lbl_val.get_style_context().add_class("data-value")
            
            self.grid.attach(lbl_key, 0, i, 1, 1)
            self.grid.attach(lbl_val, 1, i, 1, 1)
            self.labels[key] = lbl_val

        # --- Hardware Switch for Conservation Mode ---
        toggle_hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        toggle_hbox.set_halign(Gtk.Align.CENTER)
        toggle_hbox.set_name("toggle-container")
        main_vbox.pack_start(toggle_hbox, False, False, 0)

        self.status_lbl = Gtk.Label(label="CONSERVATION MODE:")
        self.status_lbl.set_name("toggle-label")
        toggle_hbox.pack_start(self.status_lbl, False, False, 0)

        # Replacing Gtk.Button with Gtk.Switch
        self.hw_switch = Gtk.Switch()
        # Ensure the switch is initialized as "fetching"
        self.hw_switch.set_active(False)
        self.hw_switch.connect("state-set", self.on_switch_state_set)
        toggle_hbox.pack_start(self.hw_switch, False, False, 0)

        # --- Developer Footer ---
        dev_event = Gtk.EventBox()
        dev_lbl = Gtk.Label(label="SYSTEM ARCHITECT: Mr Shoaib Mahmud | shoaib.yzz.me")
        dev_lbl.set_name("dev-info")
        dev_event.add(dev_lbl)
        dev_event.connect("button-press-event", lambda w, e: webbrowser.open("https://shoaib.yzz.me"))
        main_vbox.pack_end(dev_event, False, False, 0)

    def get_system_data(self):
        try:
            cmd = "upower -i /org/freedesktop/UPower/devices/battery_BAT0"
            out = subprocess.check_output(cmd, shell=True).decode()
            data = {}
            for line in out.splitlines():
                if ':' in line:
                    k, v = line.split(':', 1)
                    data[k.strip()] = v.strip()
            return data
        except:
            return {}

    def fetch_data_thread(self):
        data = self.get_system_data()
        GLib.idle_add(self.update_telemetry, data)

    def start_telemetry_loop(self):
        threading.Thread(target=self.fetch_data_thread, daemon=True).start()
        GLib.timeout_add_seconds(5, self.trigger_thread) # Reduced update frequency to 5 seconds

    def trigger_thread(self):
        threading.Thread(target=self.fetch_data_thread, daemon=True).start()
        return True

    def initialize_switch_state(self):
        # Reads the initial hardware state to set the switch correctly
        try:
            if not os.path.exists(HW_PATH):
                raise FileNotFoundError(f"Hardware node not found at {HW_PATH}")
            with open(HW_PATH, 'r') as f:
                status = f.read().strip()
            
            ctx = self.hw_switch.get_style_context()
            ctx.remove_class("active")
            ctx.remove_class("inactive")

            if status == "1":
                self.hw_switch.set_active(True)
                ctx.add_class("active")
                self.status_lbl.set_label("CONSERVATION MODE (ON):")
            elif status == "0":
                self.hw_switch.set_active(False)
                ctx.add_class("inactive")
                self.status_lbl.set_label("CONSERVATION MODE (OFF):")
            else:
                raise ValueError(f"Invalid hardware status: {status}")
        except Exception as e:
            print(f"Initialization Error: {e}")
            self.hw_switch.set_sensitive(False) # Disable the switch on error
            self.status_lbl.set_label("ACPI FIRMWARE ERROR")

    def update_telemetry(self, data):
        # Updates the data grid only, does not touch the switch state
        for key, lbl in self.labels.items():
            lbl.set_label(data.get(key, "N/A"))

    def on_switch_state_set(self, switch, state):
        # Connected to the 'state-set' signal of Gtk.Switch
        # This function handles the logic for toggling the hardware setting
        
        # Block updates from the telemetry loop while toggling
        switch.set_sensitive(False)

        def toggle_thread():
            try:
                # Based on the user's intended new state
                new = "1" if state else "0"
                # Using pkexec to write to the protected sysfs node
                subprocess.run(f'pkexec sh -c "echo {new} > {HW_PATH}"', shell=True, check=True)
                
                # Verify the change by reading back
                with open(HW_PATH, 'r') as f:
                    verified = f.read().strip()
                
                if verified != new:
                    raise ValueError("Hardware state does not match set value.")

                # Success: Update the UI on the main thread
                GLib.idle_add(self.toggle_success_callback, switch, state)
            except subprocess.CalledProcessError:
                # The user likely cancelled the pkexec prompt
                print("Hardware Error: Permission Denied")
                GLib.idle_add(self.toggle_failure_callback, switch, not state)
            except Exception as e:
                print(f"Hardware Error: {e}")
                GLib.idle_add(self.toggle_failure_callback, switch, not state)

        threading.Thread(target=toggle_thread, daemon=True).start()
        return True # Indicates we've handled the signal

    def toggle_success_callback(self, switch, state):
        ctx = switch.get_style_context()
        ctx.remove_class("active")
        ctx.remove_class("inactive")

        if state:
            ctx.add_class("active")
            self.status_lbl.set_label("CONSERVATION MODE (ON):")
        else:
            ctx.add_class("inactive")
            self.status_lbl.set_label("CONSERVATION MODE (OFF):")
        
        switch.set_sensitive(True)

    def toggle_failure_callback(self, switch, reverse_state):
        # If toggling failed, revert the switch to its previous known good state
        switch.set_active(reverse_state)
        switch.set_sensitive(True)
        # Force a telemetry update to re-sync
        self.fetch_data_thread()

if __name__ == "__main__":
    # Standard GTK3 execution block
    app = PowerDashboard()
    app.show_all()
    Gtk.main()