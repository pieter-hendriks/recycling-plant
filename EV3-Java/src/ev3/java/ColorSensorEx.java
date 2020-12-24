package ev3.java;

import ev3dev.sensors.ev3.EV3ColorSensor;
import lejos.hardware.port.SensorPort;
import lejos.robotics.SampleProvider;
import lejos.utility.Delay;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class ColorSensorEx {
    public static Logger LOGGER = LoggerFactory.getLogger(ColorSensorEx.class);
    //private static EV3ColorSensor color1 = new EV3ColorSensor(SensorPort.S3);
    public static void main(String[] args) {
	SampleProvider sp = new EV3ColorSensor(SensorPort.S3).getColorIDMode();
	float[] sample = new float[sp.sampleSize()];
        for (int i = 0; i < 100; i++) {
            sp.fetchSample(sample, 0);
            LOGGER.info("N={} Sample={}", i, (float) sample[0]);
            Delay.msDelay(500);
        }
    }
}