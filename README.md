# Tracker-UAV

Tracker-UAV is a ROS 2 workspace for a PX4-based UAV tracking setup with Gazebo integration.

The current repository contains a workspace-style source tree under `src/` and includes the following primary code components:

- `px4-ros2-interface-lib`
  - PX4 companion computer interface library for ROS 2
  - Provides mode and setpoint support for interacting with PX4 via uORB messages
- `px4_msgs`
  - ROS 2 message definitions for PX4 uORB topics
  - Required to translate PX4 internal messages into ROS 2 interfaces
- `ros_gz`
  - ROS 2 / Gazebo bridge packages
  - Provides simulator integration, image transport, topics, and demos
- `vision_opencv`
  - ROS 2 OpenCV bridge packages
  - Includes `cv_bridge`, `image_geometry`, and other vision utilities

## Repository structure

- `src/`
  - The ROS 2 workspace source directory containing the main packages
- `build/`
  - Workspace build artifacts
- `install/`
  - Installed workspace output
- `log/`
  - Build and runtime logs

## Requirements

- Ubuntu 22.04 (recommended)
- ROS 2 Humble (or compatible ROS 2 distro)
- Gazebo / Gazebo Garden or Fortress depending on your `ros_gz` configuration
- `colcon` build tool
- `rosdep`

## Setup

1. Source your ROS 2 distribution:

```bash
source /opt/ros/humble/setup.bash
```

2. Install dependencies for the workspace:

```bash
cd /home/jagdeesh/tracker
rosdep install -r --from-paths src --ignore-src -y
```

3. Build the workspace:

```bash
colcon build --symlink-install
```

4. Source the workspace after building:

```bash
source install/setup.bash
```

## Run simulation

After the workspace is built and sourced, you can start the Gazebo / ROS 2 bridge and demo simulation using the packages included under `src/ros_gz`.

1. Start Ignition Gazebo with the ROS 2 bridge:

```bash
ros2 launch ros_ign_gazebo ign_gazebo.launch.py
```

2. Run one of the demo bridges to connect Gazebo sensors to ROS 2 topics. For example, to bridge a camera topic:

```bash
ros2 launch ros_gz_sim_demos/image_bridge.launch.py
```

3. Optionally launch other demo nodes such as the TF bridge, robot description publisher, or a camera demo:

```bash
ros2 launch ros_gz_sim_demos/tf_bridge.launch.py
ros2 launch ros_gz_sim_demos/robot_description_publisher.launch.py
ros2 launch ros_gz_sim_demos/camera.launch.py
```

4. Start your PX4 companion computer node or tracking node once the simulator is running. This repository includes `px4-ros2-interface-lib` for PX4 setpoint and mode integration.

5. Verify the ROS 2 topics and bridge operation using:

```bash
ros2 topic list
ros2 node list
```

## Usage

This workspace is primarily intended to support PX4 + ROS 2 integration and simulator workflows.

- Use `px4_msgs` to provide ROS 2 equivalents of PX4 uORB messages.
- Use `px4-ros2-interface-lib` to implement companion computer modes and send PX4 setpoints.
- Use `ros_gz` packages to connect ROS 2 nodes with Gazebo simulator topics.
- Use `vision_opencv` for image processing and OpenCV interoperability.

## How it works

The overall tracking system follows a typical UAV search and land workflow:

1. Search
   - A camera stream is bridged from Gazebo to ROS 2 via `ros_gz`.
   - Vision processing runs in ROS 2 using `vision_opencv` and detects the target vehicle or landing marker.
   - The target detection may use image features, fiducial markers, or a custom object detector.

2. Track
   - The tracking node estimates the target position in the drone frame.
   - It publishes a relative target pose or velocity commands to PX4 using `px4_msgs`.
   - The drone follows the target by keeping the vehicle centered in the camera view.

3. Align
   - Once the target is found, the flight controller aligns the UAV with the target direction.
   - Alignment includes lateral positioning, heading correction, and matching target motion.
   - The alignment phase prepares the drone for a stable landing approach.

4. Land on moving vehicle
   - When the target is aligned and stable, the system begins a controlled descent.
   - The drone reduces altitude while maintaining the relative position over the moving vehicle.
   - Landing completes when the drone is centered above the landing zone and close enough to the vehicle.

## Typical runtime flow

A full experiment usually works like this:

1. Start the ROS 2 workspace and source `install/setup.bash`.
2. Launch the Gazebo simulator and the `ros_gz` bridge.
3. Start PX4 or a PX4-compatible simulator with the companion computer integration.
4. Run the vision/tracking node that subscribes to camera images and publishes control setpoints.
5. Enable the PX4 guided or custom landing mode to execute the landing.

## Notes

- The repository currently contains generated workspace artifacts in `build/`, `install/`, and `log/`.
- The root `.gitignore` is configured to ignore build, install, log, and log files.

## License

The repository components are subject to the licenses of the individual packages contained in `src/`. See each package directory for license details.
