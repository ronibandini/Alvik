Arduino Alvik Autocharge prototype

Note: Alvik is not charging while on, so I'm solving this issue.

Roni Bandini, March 2025

I decided to modify the Arduino Alvik to install a basic self-charging system without adding any sensors beyond those that come factory-installed.

The goal is for Alvik to autonomously navigate a space using its distance sensor to avoid obstacles. When the battery falls below a defined threshold, it will follow a line leading to the charger, dock with it, recharge, and then continue its path.

To avoid obstacles, Alvik uses alvik.get_distance().
To detect the line leading to the charger, it uses alvik.get_line_sensors().
For final docking detection, it uses alvik.get_color_label().

The charging system uses a 5V/1A wireless charger with “resonant magnetic coupling” technology. This charger accepts 12V DC input and provides 5V DC output. Although the manufacturer claims the charging distance can reach up to 10mm, in practice, the receiver must be almost directly on top of the transmitter.

Two wires are soldered to the VIN and GND pins of the ESP32. Alternatively, the female connectors on the side of the ESP32 can be used, as these map directly to the power input pins. However, soldering provides more mechanical stability.

Tutorial https://bandini.medium.com/arduino-alvik-self-charging-a5c1ba0fb876
3d Parts https://cults3d.com/en/3d-model/gadget/alvik-autocharge

