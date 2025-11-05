# Clean PX4 Offboard Node


### Features:
- Clean and modular code structure for easy understanding and maintenance.
- Command line arguments for flexible configuration.
- Nice and easy logging of energy consumption using PyJoules.
- Nice and easy logging of control data using [my custom ROS2 Logger](https://github.com/evannsm/ROS2Logger).

### PyJoules Set Up:
1. Install PyJoules:
   ```bash
   pip install pyJoules
   ```

2. Replace the csv handler with mine from github, [see my repo](https://github.com/evannsm/pyjoules-csv-handler).
3. Give permissions to run pyJoules:
   ```bash
   sudo chmod -R a+r /sys/class/powercap/intel-rapl
   ```