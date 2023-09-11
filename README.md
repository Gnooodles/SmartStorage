<div align="center">
  <p>
      <img width="20%" src="./img/arduino.svg">
  </p>
  <b><h1> Smart Storage </h1></b>
  <p>Automatic solutions for home pantry management using<href="https://www.arduino.cc"> Arduino</a></p>
</div>
<br>

<br>

## Vision
Our project for the Internet of Things course aims to implement a system for monitoring and automating pantry management. We have physically integrated a sensor with an Arduino system, and through communication with a PC, it will be possible to view the data directly on its screen or on a smartphone.

The system allows for the loading and unloading of products in a digital warehouse, these processes are carried out by scanning the barcodes of the products. The system enables:

- Maintaining a warehouse that represents the household pantry where food and non-food products are stored.
- Automatically populating product data through barcode scanning.
- Automatically generating and maintaining a shopping list when products are unloaded and used.
- Managing the warehouse through the dashboard in the web app.
- Accessing and updating the shopping list in the web app.


## Use cases

- Select the device operation mode, between *loading* and *unloading* modes.
- Load the product into the system by scanning its barcode using the sensor.
- Unload the product from the system by scanning the barcode using the sensor.
- Set a threshold to keep a minimum quantity of a product in the warehouse.
- Change the quantity of a product in the warehouse.
- Add products whose quantity is less than the minimum threshold to the shopping list.


## Usage
The system is contained in the `/src` directory.

Befor starting the system please make sure the dependencies are installed, run in the directory where the file `requirements.txt` live:

```bash
pip install -r requirements.txt
```

To start the system use the following command for running the bash script:

```bash
./src/app.sh
```

or if you use Python3

```bash
./src/app3.sh
```


## Technology
Hardware used for the project:

- Arduino.
- One button and two differently colored LEDs.
- GM65 scanning module for the acquisition of 1D and 2D barcodes.

Software used for the project:

- Arduino IDE for creating and uploading the .ino script responsible for button functionality, communication with the barcode scanning sensor, and serial port communication.
- Python 3.11 for building all software components.
- Git and GitHub for version control, creating a repository, and managing various branches for feature development.
- Sqlite3 library for database management through Python code.
- Streamlit library for creating the web app and user interface for system management.
- Pytest library for project unit testing.
- Pyserial library for communication between Arduino and Python.


