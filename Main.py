#pip install pyserial obd
import obd
import serial.tools.list_ports

def list_ports():
    print("Available ports:")
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        print(f"{p.device}: {p.description}") 
def connect_to_obd(port=None):
    try:
        if port:
            connection = obd.OBD(port)  # Connect to the specified port
        else:
            connection = obd.OBD()  # Automatically find the port

        if connection.status() == obd.OBDStatus.CAR_CONNECTED:
            print("Successfully connected to the car")
            return connection
        else:
            print(f"Failed to connect to the car: {connection.status()}")
            return None
    except Exception as e:
        print(f"An error occurred while connecting to OBD-II: {e}")
        return None 
def read_engine_rpm(connection):
    try:
        cmd = obd.commands.RPM
        response = connection.query(cmd)
        if response.value is not None:
            print("Engine RPM:", response.value.magnitude)
        else:
            print("Failed to read RPM:", response.status())
    except Exception as e:
        print(f"An error occurred while reading RPM: {e}") 
def read_dtc(connection):
    try:
        cmd = obd.commands.GET_DTC
        response = connection.query(cmd)
        if response.value is not None:
            dtcs = response.value
            if dtcs:
                for code in dtcs:
                    print(f"DTC: {code[0]}, Description: {code[1]}")
            else:
                print("No DTCs found")
        else:
            print("Failed to read DTCs:", response.status())
    except Exception as e:
        print(f"An error occurred while reading DTCs: {e}")

def main():
    list_ports()
    port = input("Enter the port to connect to (or leave blank to auto-detect): ").strip()
    connection = connect_to_obd(port if port else None)
    if connection:
        read_engine_rpm(connection)
        read_dtc(connection)
    else:
        print("Could not establish a connection to the OBD-II interface.")

if __name__ == "__main__":
    main() 
