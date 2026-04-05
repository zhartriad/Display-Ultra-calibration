#!/usr/bin/env python3
import gi
import subprocess
import json
import os
import sys  

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

CONFIG_PATH = os.path.expanduser("~/.config/cachy-display/config.json")

def apply_saved_boot_config():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, 'r') as f:
                config = json.load(f)
            for monitor, p in config.items():
                b, r, g, bl, s = (p.get("bright", 1.0), p.get("r", 1.0),
                                  p.get("g", 1.0), p.get("b", 1.0),
                                  p.get("sat", 1.0))

                subprocess.run(["xrandr", "--output", monitor, "--brightness", f"{b:.2f}",
                                "--gamma", f"{r:.2f}:{g:.2f}:{bl:.2f}"], check=False)

                subprocess.run(["vibrant-cli", monitor, f"{s:.1f}"], stderr=subprocess.DEVNULL, check=False)
            print("Configurações aplicadas com sucesso pelo BY ZHAR Boot!")
        except Exception as e:
            print(f"Erro ao aplicar boot config: {e}")

class CachyDisplayUltra(Gtk.Window):
    def __init__(self):
        super().__init__(title="Cachy Display Ultra BY ZHAR")
        self.set_default_size(700, 500)
        self.set_border_width(15)
        self.apply_custom_style()
        self.current_config = self.load_config()

        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        self.add(main_box)

        self.monitor_combo = Gtk.ComboBoxText()
        self.populate_monitors()
        self.monitor_combo.connect("changed", self.on_monitor_changed)
        main_box.pack_start(self.monitor_combo, False, False, 0)

        notebook = Gtk.Notebook()
        main_box.pack_start(notebook, True, True, 0)

        tab1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        tab1.set_border_width(10)
        self.bright = self.create_slider(tab1, "Brilho Total", 0.2, 2.0, 1.0)
        self.sat = self.create_slider(tab1, "Saturação", 0.0, 4.0, 1.0)
        notebook.append_page(tab1, Gtk.Label(label="Principal"))

        tab2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        tab2.set_border_width(10)
        self.gamma_r = self.create_slider(tab2, "Canal Vermelho (R)", 0.5, 2.0, 1.0)
        self.gamma_g = self.create_slider(tab2, "Canal Verde (G)", 0.5, 2.0, 1.0)
        self.gamma_b = self.create_slider(tab2, "Canal Azul (B)", 0.5, 2.0, 1.0)
        notebook.append_page(tab2, Gtk.Label(label="Canais RGB"))

        tab3 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        tab3.set_border_width(10)
        flowbox = Gtk.FlowBox()
        flowbox.set_max_children_per_line(3)
        tab3.pack_start(flowbox, False, False, 0)

        profiles = {
            "Padrão": (1.0, 1.0, 1.0, 1.0, 1.0),
            "AMOLED Deep": (0.8, 1.8, 1.2, 1.0, 0.9),
            "OLED Vivid": (1.0, 1.6, 1.1, 1.1, 1.1),
            "Nano LED": (1.0, 2.5, 1.2, 1.2, 1.2),
            "Filtro Azul": (0.9, 1.0, 1.1, 1.0, 0.6)
        }

        for name, vals in profiles.items():
            btn = Gtk.Button(label=name)
            btn.connect("clicked", self.apply_profile, vals)
            flowbox.add(btn)
        notebook.append_page(tab3, Gtk.Label(label="Perfis"))

        btn_zhar = Gtk.Button(label="BY ZHAR")
        btn_zhar.get_style_context().add_class("zhar-button")
        btn_zhar.connect("clicked", self.show_about_dialog)
        main_box.pack_start(btn_zhar, False, False, 5)

        actions = Gtk.ActionBar()
        main_box.pack_end(actions, False, False, 0)
        btn_save = Gtk.Button(label="Salvar como Padrão")
        btn_save.connect("clicked", self.save_settings)
        actions.pack_start(btn_save)

        self.on_monitor_changed(self.monitor_combo)
        self.show_all()

    def show_about_dialog(self, btn):
        dialog = Gtk.Window(title="Sobre o Projeto")
        dialog.set_transient_for(self)
        dialog.set_modal(True)
        dialog.set_default_size(400, 300)
        dialog.set_keep_above(True)
        
        ctx = dialog.get_style_context()
        provider = Gtk.CssProvider()
        provider.load_from_data(b"window { background-color: rgba(0,0,0,0.8); color: white; } label { font-size: 13px; }")
        ctx.add_provider(provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        box.set_border_width(20)
        dialog.add(box)

        text = ("Este programa nasceu da colaboração entre Zhar e Gemini.\n\n"
                "O intuito é fornecer controle da configuração da tela de forma facil "
                "CachyOS, permitindo ajustes que o sistema padrão não oferece.\n\n"
                "Desenvolvido com foco em performance e estética.")
        
        lbl = Gtk.Label(label=text)
        lbl.set_line_wrap(True)
        lbl.set_justify(Gtk.Justification.CENTER)
        box.pack_start(lbl, True, True, 0)

        btn_close = Gtk.Button(label="Fechar")
        btn_close.connect("clicked", lambda w: dialog.destroy())
        box.pack_end(btn_close, False, False, 0)
        dialog.show_all()

    def apply_custom_style(self):
        screen = Gdk.Screen.get_default()
        provider = Gtk.CssProvider()
        img_path = "/usr/share/cachy-display/background.jpg"
        style = f"""
            window {{
                background-image: linear-gradient(rgba(30, 30, 30, 0.5), rgba(30, 30, 30, 0.5)),
                                  url('file://{img_path}');
                background-repeat: no-repeat;
                background-position: center;
                background-size: cover;
            }}
            notebook, box, grid {{ background-color: transparent; }}
            label {{ color: white; text-shadow: 1px 1px 3px black; }}
            .zhar-button {{
                background: rgba(255, 0, 0, 0.2);
                color: #ff3333;
                border: 1px solid #ff0000;
                font-weight: bold;
                border-radius: 8px;
            }}
            .zhar-button:hover {{ background: rgba(255, 0, 0, 0.4); color: white; }}
            notebook stack {{ background-color: rgba(0, 0, 0, 0.2); border-radius: 10px; }}
            scale contents {{ background-color: rgba(255, 255, 255, 0.1); }}
        """
        provider.load_from_data(style.encode())
        Gtk.StyleContext.add_provider_for_screen(screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    def create_slider(self, container, label, low, high, default):
        lbl = Gtk.Label(label=label, xalign=0)
        adj = Gtk.Adjustment(value=default, lower=low, upper=high, step_increment=0.01)
        scale = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=adj)
        scale.set_digits(2)
        scale.connect("value-changed", self.apply_hardware)
        container.pack_start(lbl, False, False, 0)
        container.pack_start(scale, False, False, 0)
        return scale

    def apply_hardware(self, *args):
        m = self.monitor_combo.get_active_text()
        if not m: return
        b, r, g, bl, s = (self.bright.get_value(), self.gamma_r.get_value(),
                          self.gamma_g.get_value(), self.gamma_b.get_value(),
                          self.sat.get_value())
        subprocess.run(["xrandr", "--output", m, "--brightness", f"{b:.2f}",
                        "--gamma", f"{r:.2f}:{g:.2f}:{bl:.2f}"], check=False)
        subprocess.run(["vibrant-cli", m, f"{s:.1f}"], stderr=subprocess.DEVNULL, check=False)

    def apply_profile(self, btn, vals):
        b, s, r, g, bl = vals
        sliders = [self.bright, self.sat, self.gamma_r, self.gamma_g, self.gamma_b]
        for sld in sliders: sld.handler_block_by_func(self.apply_hardware)
        self.bright.set_value(b); self.sat.set_value(s)
        self.gamma_r.set_value(r); self.gamma_g.set_value(g); self.gamma_b.set_value(bl)
        for sld in sliders: sld.handler_unblock_by_func(self.apply_hardware)
        self.apply_hardware()

    def load_config(self):
        if os.path.exists(CONFIG_PATH):
            try:
                with open(CONFIG_PATH, 'r') as f: return json.load(f)
            except: return {}
        return {}

    def save_settings(self, btn):
        m = self.monitor_combo.get_active_text()
        if not m: return
        os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
        config = self.load_config()
        config[m] = {
            "bright": self.bright.get_value(), "sat": self.sat.get_value(),
            "r": self.gamma_r.get_value(), "g": self.gamma_g.get_value(), "b": self.gamma_b.get_value()
        }
        with open(CONFIG_PATH, 'w') as f: json.dump(config, f, indent=4)

    def on_monitor_changed(self, combo):
        m = combo.get_active_text()
        if not m: return
        config = self.load_config()
        if m in config:
            p = config[m]
            sliders = [self.bright, self.sat, self.gamma_r, self.gamma_g, self.gamma_b]
            for sld in sliders: sld.handler_block_by_func(self.apply_hardware)
            self.bright.set_value(p.get("bright", 1.0))
            self.sat.set_value(p.get("sat", 1.0))
            self.gamma_r.set_value(p.get("r", 1.0))
            self.gamma_g.set_value(p.get("g", 1.0))
            self.gamma_b.set_value(p.get("b", 1.0))
            for sld in sliders: sld.handler_unblock_by_func(self.apply_hardware)
            self.apply_hardware()

    def populate_monitors(self):
        try:
            out = subprocess.check_output("xrandr --query | grep ' connected' | cut -d' ' -f1", shell=True).decode()
            for m in out.strip().split('\n'):
                if m.strip(): self.monitor_combo.append_text(m.strip())
            self.monitor_combo.set_active(0)
        except:
            self.monitor_combo.append_text("eDP-1"); self.monitor_combo.set_active(0)

if __name__ == "__main__":

    if len(sys.argv) > 1 and sys.argv[1] == "--apply":
        apply_saved_boot_config()
    else:

        win = CachyDisplayUltra()
        win.connect("destroy", Gtk.main_quit)
        Gtk.main()
