package example.robotics.ev3.sensor;

import ev3dev.sensors.Battery;
import ev3dev.sensors.ev3.EV3TouchSensor;
import lejos.hardware.port.SensorPort;
import lejos.robotics.SampleProvider;
import lejos.utility.Delay;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class TouchSensorExample {
    public static Logger LOGGER = LoggerFactory.getLogger(TouchSensorExample.class); 
    public static void main(String[] args) {
        final SampleProvider sp = new EV3TouchSensor(SensorPort.S1).getTouchMode();
        for(int i = 0; i <= 20; i++) {
            float [] sample = new float[sp.sampleSize()];
            sp.fetchSample(sample, 0);
            int touchValue = (int) sample[0];
            LOGGER.info("Iteration: {}, Touch: {}", i, touchValue);
            Delay.msDelay(500);
        }
	LOGGER.info("Battery voltage: {}", Battery.getInstance().getVoltage());
    }
}