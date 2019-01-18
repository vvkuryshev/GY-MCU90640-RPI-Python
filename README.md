# GY-MCU90640-RPI-Python
The script to connect the thermal image module GY-MCU90640 to Raspberry Pi.

![Alt text](https://github.com/vvkuryshev/GY-MCU90640-RPI-Python/blob/master/Termovision_github.jpg?raw=true "Title")
The module GY-MCU90640 is based on a MLX90640 sensor, but additionally contains a microcontroller STM32F103 to simplify working with MLX90640.

The protocol of interaction with the module is contained in the file "GY_MCU9064 user manual v1.pdf". I apologize for the quality of the translation, this is an automatic translation from Chinese into English with the Google Translator.

The resulting images and the scheme of connecting the module to the Raspberry Pi are shown in the image above. The main.py script is tested for RPI 3 B + and RPI Zero W.

Description of the connection process is on https://habr.com/ru/post/435946/. Unfortunately, only in Russian, but you can also use Google Translator)
