import time
from machine import Pin, I2C
import icm20948

class ICM20948Sensor:
    def __init__(self, i2c: I2C):
        self.icm = icm20948.ICM20948(i2c)

        # Configure the ICM20948
        self.icm.clock_select = icm20948.CLK_SELECT_INTERNAL
        self.icm.accelerometer_range = icm20948.RANGE_2G
        self.icm.acc_dlpf_cutoff = icm20948.FREQ_246_0
        self.icm.gyro_dlpf_cutoff = icm20948.G_FREQ_11_6
        self.icm.gyro_full_scale = icm20948.FS_250_DPS
        self.icm.gyro_enabled = icm20948.GYRO_ENABLED
        self.icm.acc_enabled = icm20948.ACC_ENABLED
        self.icm.temp_enabled = icm20948.TEMP_ENABLED

    def to_sleep(self) -> None:
        self.icm.sleep = icm20948.SLEEP_ENABLED

    def to_awake(self) -> None:
        self.icm.sleep = icm20948.SLEEP_DISABLED

    @property
    def acceleration(self) -> tuple[float, float, float]:
        return self.icm.acceleration

    @property
    def gyro(self) -> tuple[float, float, float]:
        return self.icm.gyro

    def __str__(self) -> str:
        accx, accy, accz = self.acceleration
        gyrox, gyroy, gyroz = self.gyro
        return f"{accx:.3f}:{accy:.3f}:{accz:.3f};{gyrox:.3f}:{gyroy:.3f}:{gyroz:.3f}"

if __name__ == "__main__":
    # # I2C pin ICM20948
    i2c = I2C(0, sda=Pin(0), scl=Pin(1))
    sen = ICM20948Sensor(i2c)
    sen.to_sleep()
    print(sen.icm.sleep)
    sen.to_awake()
    print(sen.icm.sleep)

    print(sen)

    while True:
        accx, accy, accz = sen.icm.acceleration
        gyrox, gyroy, gyroz = sen.icm.gyro
        print(f"x: {accx:.3f}m/s2, y: {accy:.3f}m/s2, z: {accz:.3f}m/s2")
        print(f"x: {gyrox:.3f}deg/s, y: {gyroy:.3f}deg/s, z: {gyroz:.3f}deg/s")
        print()
        time.sleep(1)
