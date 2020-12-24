package ev3.java;

import ev3dev.actuators.lego.motors.EV3LargeRegulatedMotor;
import ev3dev.sensors.ev3.EV3ColorSensor;
import ev3dev.sensors.ev3.EV3TouchSensor;
import ev3dev.sensors.ev3.EV3UltrasonicSensor;
import lejos.hardware.port.MotorPort;
import lejos.hardware.port.SensorPort;
import lejos.robotics.SampleProvider;
import lejos.utility.Delay;

public class MotorTouchEx {
    public static void main(final String[] args){
        final EV3LargeRegulatedMotor motorRight = new EV3LargeRegulatedMotor(MotorPort.A);
        final EV3LargeRegulatedMotor motorLeft = new EV3LargeRegulatedMotor(MotorPort.B);
        final EV3UltrasonicSensor ultraSonic = new EV3UltrasonicSensor(SensorPort.S2);
        final EV3ColorSensor color = new EV3ColorSensor(SensorPort.S1);
        Runtime.getRuntime().addShutdownHook(new Thread(new Runnable() {
            public void run() { 
                System.out.println("Emergency Motor Stop"); 
                motorRight.stop();
                motorLeft.stop();
                ultraSonic.disable();
            }
        }));
        motorLeft.brake(); //Defining the Stop mode
        motorRight.brake();
        
        SampleProvider sp_us = ultraSonic.getDistanceMode();
        SampleProvider sp_color = color.getColorIDMode();
        //SampleProvider sp = new EV3TouchSensor(SensorPort.S1).getTouchMode();
        float sample_us[] = new float[sp_us.sampleSize()];
        float sample_color[] = new float[sp_color.sampleSize()];
        while(true) {
            sp_us.fetchSample(sample_us, 0);
            sp_color.fetchSample(sample_color, 0);
            System.out.println((int)sample_us[0] + "\t" + (int)sample_color[0]);
            if ((int)sample_us[0] > 30) {                
                motorLeft.setSpeed(((int)sample_us[0]-27)*4);
                motorRight.setSpeed(((int)sample_us[0]-27)*4);
                motorRight.forward();
                motorLeft.forward();
                Delay.msDelay(500);
                continue;
            }
            motorRight.stop();
            motorLeft.stop();
            Delay.msDelay(20);
        }
//        Delay.msDelay(2000);
//        System.out.println("Stop motors");
//        motorLeft.stop();
//        motorRight.stop();
//        System.out.println("Go Backward with the motors");
//        motorLeft.backward();
//        motorRight.backward();
//        Delay.msDelay(2000);
//        System.out.println("Normal Motor Stop");
//        System.out.println("Checking Battery");
//        System.out.println("Votage: " + Battery.getInstance().getVoltage());
//        System.exit(0);
    }
}