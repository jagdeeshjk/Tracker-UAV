import os

from launch import LaunchDescription
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition

# ---------------------------------------------------------------------------
# Resolve the machine's primary non-loopback IP so that the gz_ros_bridge
# connects to the same Gazebo transport as PX4.
# ---------------------------------------------------------------------------
def _get_gz_ip():
    import subprocess, re

    try:
        pids = subprocess.check_output(["pgrep", "-f", "gz sim"], text=True).split()
        for pid in pids:
            try:
                env_raw = open(f"/proc/{pid.strip()}/environ", "rb").read()
                env_vars = dict(
                    item.split(b"=", 1)
                    for item in env_raw.split(b"\x00")
                    if b"=" in item
                )
                if b"GZ_IP" in env_vars:
                    return env_vars[b"GZ_IP"].decode()
            except Exception:
                continue
    except Exception:
        pass

    try:
        out = subprocess.check_output(
            ["gz", "topic", "-i", "-t", "/clock"], text=True, timeout=3
        )
        m = re.search(r"tcp://(\d+\.\d+\.\d+\.\d+):", out)
        if m:
            return m.group(1)
    except Exception:
        pass

    try:
        ips = subprocess.check_output(["hostname", "-I"], text=True).split()
        for ip in ips:
            if not ip.startswith("127."):
                return ip
    except Exception:
        pass

    return "127.0.0.1"


_GZ_IP   = os.environ.get("GZ_IP", _get_gz_ip())
_PX4_DIR = os.path.expanduser("~/PX4-Autopilot")
_GZ_ENV  = {
    "GZ_IP": _GZ_IP,
    "GZ_SIM_SYSTEM_PLUGIN_PATH": (
        os.environ.get("GZ_SIM_SYSTEM_PLUGIN_PATH", "")
        + f":{_PX4_DIR}/build/px4_sitl_default/src/modules/simulation/gz_plugins"
    ),
    "GZ_SIM_RESOURCE_PATH": (
        os.environ.get("GZ_SIM_RESOURCE_PATH", "")
        + f":{_PX4_DIR}/Tools/simulation/gz/models"
        + f":{_PX4_DIR}/Tools/simulation/gz/worlds"
    ),
    "GZ_SIM_SERVER_CONFIG_PATH": (
        f"{_PX4_DIR}/src/modules/simulation/gz_bridge/server.config"
    ),
}

# ---------------------------------------------------------------------------
# Launch arguments
# ---------------------------------------------------------------------------
_PX4_REMAPS = [
    ('/fmu/in/register_ext_component_request',  '/px4_1/fmu/in/register_ext_component_request'),
    ('/fmu/out/register_ext_component_reply',   '/px4_1/fmu/out/register_ext_component_reply'),
    ('/fmu/in/unregister_ext_component',        '/px4_1/fmu/in/unregister_ext_component'),
    ('/fmu/out/arming_check_request_v1',        '/px4_1/fmu/out/arming_check_request_v1'),
    ('/fmu/in/arming_check_reply_v1',           '/px4_1/fmu/in/arming_check_reply_v1'),
    ('/fmu/out/vehicle_status_v1',              '/px4_1/fmu/out/vehicle_status_v1'),
    ('/fmu/out/vehicle_control_mode',           '/px4_1/fmu/out/vehicle_control_mode'),
    ('/fmu/in/vehicle_command',                 '/px4_1/fmu/in/vehicle_command'),
    ('/fmu/out/vehicle_command_ack',            '/px4_1/fmu/out/vehicle_command_ack'),
    ('/fmu/in/mode_completed',                  '/px4_1/fmu/in/mode_completed'),
    ('/fmu/out/mode_completed',                 '/px4_1/fmu/out/mode_completed'),
    ('/fmu/in/trajectory_setpoint',             '/px4_1/fmu/in/trajectory_setpoint'),
    ('/fmu/in/offboard_control_mode',           '/px4_1/fmu/in/offboard_control_mode'),
    ('/fmu/in/config_overrides_request',        '/px4_1/fmu/in/config_overrides_request'),
    ('/fmu/out/vehicle_local_position_v1',      '/px4_1/fmu/out/vehicle_local_position_v1'),
    ('/fmu/out/vehicle_odometry',               '/px4_1/fmu/out/vehicle_odometry'),
    ('/fmu/out/vehicle_attitude',               '/px4_1/fmu/out/vehicle_attitude'),
    ('/fmu/in/vehicle_command_mode_executor',   '/px4_1/fmu/in/vehicle_command_mode_executor'),
    ('/fmu/in/config_control_setpoints',        '/px4_1/fmu/in/config_control_setpoints'),
    ('/fmu/in/message_format_request',          '/px4_1/fmu/in/message_format_request'),
    ('/fmu/out/message_format_response',        '/px4_1/fmu/out/message_format_response'),
]


def generate_launch_description():
    enable_viz_arg = DeclareLaunchArgument(
        'enable_gazebo_viz',
        default_value='true',
        description='Enable Gazebo marker visualization (simulation only)',
    )

    return LaunchDescription([
        enable_viz_arg,

        # ── gz-ROS bridge ────────────────────────────────────────────────────
        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            name='gz_ros_bridge',
            parameters=[{
                'config_file': PathJoinSubstitution(
                    [FindPackageShare('precision_land'), 'cfg', 'bridge.yaml']
                )
            }],
            additional_env=_GZ_ENV,
            output='screen',
        ),

        # ── ArUco tracker ────────────────────────────────────────────────────
        # Publishes:
        #   /target_pose          (geometry_msgs/PoseStamped)  — 3-D tag pose
        #   /target_image_track   (geometry_msgs/TwistStamped) — image-plane
        #                          motion data used by the Align state
        Node(
            package='aruco_tracker',
            executable='aruco_tracker',
            name='aruco_tracker',
            output='screen',
            parameters=[
                PathJoinSubstitution(
                    [FindPackageShare('aruco_tracker'), 'cfg', 'params.yaml']
                ),
                {
                    'image_topic':
                        '/world/default/model/x500_mono_cam_down_1'
                        '/link/camera_link/sensor/imager/image',
                    'camera_info_topic':
                        '/world/default/model/x500_mono_cam_down_1'
                        '/link/camera_link/sensor/imager/camera_info',
                },
            ],
        ),

        # ── Precision landing ────────────────────────────────────────────────
        # State flow:  Search → Align → Descend → Finished
        #
        # New Align state subscribes to /target_image_track and holds altitude
        # while centering the rover tag in the camera frame (drone nadir
        # directly above rover) before beginning the final descent.
        Node(
            package='precision_land',
            executable='precision_land',
            name='precision_land',
            output='screen',
            parameters=[
                PathJoinSubstitution(
                    [FindPackageShare('precision_land'), 'cfg', 'params.yaml']
                ),
            ],
            remappings=_PX4_REMAPS,
        ),

        # ── Gazebo visualization (sim only) ──────────────────────────────────
        Node(
            package='precision_land_viz',
            executable='tag_pose_visualizer',
            name='tag_pose_visualizer',
            output='screen',
            condition=IfCondition(LaunchConfiguration('enable_gazebo_viz')),
        ),
    ])
