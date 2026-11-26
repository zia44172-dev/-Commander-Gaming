
import json
import os

from kivy.app import App
from kivy.core.window import Window
from kivy.core.clipboard import Clipboard
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner

Window.clearcolor = (0.025, 0.04, 0.03, 1)

FILE = "commander_8_settings.json"

defaults = {
    "M416": {
        "Gyro": "Red Dot: 250\n3x: 180\n4x: 130\n6x: 85",
        "Non-Gyro": "Red Dot: 50\n3x: 25\n4x: 18\n6x: 10"
    },
    "AKM": {
        "Gyro": "Red Dot: 240\n3x: 170\n4x: 120\n6x: 75",
        "Non-Gyro": "Red Dot: 45\n3x: 22\n4x: 15\n6x: 8"
    },
    "M762": {
        "Gyro": "Red Dot: 250\n3x: 180\n4x: 125\n6x: 80",
        "Non-Gyro": "Red Dot: 48\n3x: 24\n4x: 16\n6x: 9"
    },
    "M24": {
        "Gyro": "3x: 180\n4x: 150\n6x: 100\n8x: 65",
        "Non-Gyro": "3x: 35\n4x: 25\n6x: 15\n8x: 10"
    }
}


class CommanderApp(App):

    def build(self):
        self.editors = {}

        main = BoxLayout(
            orientation="vertical",
            padding=12,
            spacing=10,
            size_hint_y=None
        )
        main.bind(minimum_height=main.setter("height"))

        title = Label(
            text="[b]COMMANDER GAMING 8.0[/b]\n"
                 "[color=ffff00]CUSTOM SENSITIVITY EDITOR[/color]",
            markup=True,
            font_size=22,
            size_hint_y=None,
            height=85,
            color=(0.3, 1, 0.3, 1)
        )
        main.add_widget(title)

        self.mobile = TextInput(
            hint_text="Enter Mobile Name",
            multiline=False,
            size_hint_y=None,
            height=48
        )
        main.add_widget(self.mobile)

        row = BoxLayout(
            size_hint_y=None,
            height=48,
            spacing=8
        )

        self.fps = Spinner(
            text="Select FPS",
            values=("30 FPS", "40 FPS", "60 FPS",
                    "90 FPS", "120 FPS")
        )

        self.mode = Spinner(
            text="Gyro",
            values=("Gyro", "Non-Gyro")
        )

        row.add_widget(self.fps)
        row.add_widget(self.mode)
        main.add_widget(row)

        heading = Label(
            text="[b][color=ffff00]EDIT YOUR GUN SETTINGS[/color][/b]",
            markup=True,
            size_hint_y=None,
            height=45
        )
        main.add_widget(heading)

        for gun, modes in defaults.items():
            label = Label(
                text=f"[b]{gun}[/b]",
                markup=True,
                color=(0.3, 1, 0.3, 1),
                font_size=20,
                size_hint_y=None,
                height=40
            )
            main.add_widget(label)

            self.editors[gun] = {}

            for mode_name in ("Gyro", "Non-Gyro"):
                mode_label = Label(
                    text=mode_name + " Settings",
                    size_hint_y=None,
                    height=30,
                    color=(1, 0.85, 0.1, 1)
                )
                main.add_widget(mode_label)

                editor = TextInput(
                    text=modes[mode_name],
                    multiline=True,
                    size_hint_y=None,
                    height=105,
                    font_size=15
                )

                main.add_widget(editor)
                self.editors[gun][mode_name] = editor

        self.result = Label(
            text="Edit values, then press Generate.",
            size_hint_y=None,
            height=70,
            halign="left",
            valign="top",
            color=(1, 1, 1, 1)
        )

        self.result.bind(
            width=lambda obj, w:
            setattr(obj, "text_size", (w, None))
        )

        self.result.bind(
            texture_size=lambda obj, size:
            setattr(obj, "height", size[1] + 25)
        )

        main.add_widget(self.result)

        buttons = [
            ("GENERATE SETTINGS", self.generate, (0.05, 0.5, 0.12, 1)),
            ("SAVE SETTINGS", self.save, (0.05, 0.25, 0.7, 1)),
            ("LOAD SETTINGS", self.load, (0.45, 0.1, 0.65, 1)),
            ("COPY SETTINGS", self.copy, (0.65, 0.4, 0.02, 1))
        ]

        for name, action, color in buttons:
            btn = Button(
                text=name,
                size_hint_y=None,
                height=52,
                background_normal="",
                background_color=color,
                bold=True
            )
            btn.bind(on_press=action)
            main.add_widget(btn)

        scroll = ScrollView()
        scroll.add_widget(main)

        return scroll

    def collect_settings(self):
        data = {}

        for gun in self.editors:
            data[gun] = {}

            for mode in ("Gyro", "Non-Gyro"):
                data[gun][mode] = self.editors[gun][mode].text

        return data

    def generate(self, button):
        mobile = self.mobile.text.strip()

        if not mobile:
            self.result.text = "Please enter mobile name."
            return

        if self.fps.text == "Select FPS":
            self.result.text = "Please select FPS."
            return

        output = (
            "COMMANDER GAMING 8.0\n"
            f"Mobile: {mobile}\n"
            f"FPS: {self.fps.text}\n"
            f"Mode: {self.mode.text}\n\n"
        )

        for gun, modes in self.collect_settings().items():
            output += gun + "\n"
            output += modes[self.mode.text] + "\n\n"

        self.current_text = output
        self.result.text = output

    def save(self, button):
        mobile = self.mobile.text.strip()

        if not mobile:
            self.result.text = "Enter mobile name first."
            return

        try:
            data = {}

            if os.path.exists(FILE):
                with open(FILE, "r") as f:
                    data = json.load(f)

            data[mobile] = {
                "fps": self.fps.text,
                "mode": self.mode.text,
                "guns": self.collect_settings()
            }

            with open(FILE, "w") as f:
                json.dump(data, f, indent=4)

            self.result.text = "Your custom settings saved!"

        except Exception as e:
            self.result.text = "Save error: " + str(e)

    def load(self, button):
        mobile = self.mobile.text.strip()

        try:
            with open(FILE, "r") as f:
                data = json.load(f)

            saved = data[mobile]

            self.fps.text = saved["fps"]
            self.mode.text = saved["mode"]

            for gun, modes in saved["guns"].items():
                for mode, values in modes.items():
                    self.editors[gun][mode].text = values

            self.result.text = "Custom settings loaded successfully!"

        except FileNotFoundError:
            self.result.text = "No saved settings found."
        except KeyError:
            self.result.text = "No settings saved for this mobile."
        except Exception as e:
            self.result.text = "Load error: " + str(e)

    def copy(self, button):
        if not hasattr(self, "current_text"):
            self.generate(button)

        if hasattr(self, "current_text"):
            Clipboard.copy(self.current_text)
            self.result.text = "Settings copied!"


CommanderApp().run()
      
