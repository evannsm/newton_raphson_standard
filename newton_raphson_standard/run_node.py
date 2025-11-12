import rclpy, sys, traceback, argparse, os, inspect

from Logger import Logger  # type: ignore
from .ros2px4_node import OffboardControl

from newton_raphson_standard_utils.main_utils import BANNER
from newton_raphson_standard_utils.vehicles.platform_interface import PlatformType
from newton_raphson_standard_utils.trajectories import TrajectoryType
# from pyJoules.handler.csv_handler import CSVHandler

def create_parser():
    """Create and configure argument parser.
    
    Args:
        platform: 'sim' or 'hw'
        trajectory: Trajectory name (e.g., 'circle_horz', 'fig8_vert', etc.)
        pyjoules: Enable PyJoules energy monitoring
        double_speed: Use double speed for trajectories
        short: Use short variant for fig8_vert trajectory
        spin: Enable spin for circle_horz and helix trajectories
        log_file: Log file name (without extension)
        base_path: Base path for log file
    """
    parser = argparse.ArgumentParser(
        description='Offboard Control for Quadrotor',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
        """ + "==" * 60 + """
        Example usage:
        ros2 run newton_raphson_standard run --platform sim --trajectory hover --log-file log.log
        """ + "==" * 60 + """
        """#This gets printed when you do `ros2 run newton_raphson_standard run --help`
    )

    # Required arguments
    parser.add_argument(
        "--platform",
        type=PlatformType,
        choices=list(PlatformType),
        required=True,
        help="Platform type to use. Options: "
            + ", ".join(e.value for e in PlatformType)
            + ".",
    )

    parser.add_argument(
        '--trajectory',
        type=TrajectoryType,
        choices=list(TrajectoryType),
        required=True,
        help="Trajectory type to execute. Options: "
            + ", ".join(e.value for e in TrajectoryType)
            + ".",
    )

    parser.add_argument(
        "--hover-mode",
        type=int,
        choices=range(1, 9),  # 1–8 are the only possible values
        help="Hover mode (required when --trajectory=hover). On hardware only 1–4 are allowed.",
    )


    parser.add_argument(
        '--double-speed',
        action='store_false',
        help='Use double speed (2x) for trajectories'
    )

    parser.add_argument(
        '--short',
        action='store_true',
        help='Use short variant for fig8_vert trajectory'
    )

    parser.add_argument(
        '--spin',
        action='store_true',
        help='Enable spin for circle_horz and helix trajectories'
    )

    parser.add_argument(
        '--log-file',
        type=str,
        required=True,
        help='Log file name without extension (default: hybrid_mpc_log)'
    )

    return parser

def validate_args(args, parser: argparse.ArgumentParser) -> None:
    # Only valid/required for hover trajectory
    if args.trajectory == TrajectoryType.HOVER:
        if args.hover_mode is None:
            parser.error("--hover-mode is required when --trajectory=hover")
        # Platform-specific limits
        if args.platform == PlatformType.HARDWARE and args.hover_mode not in range(1, 5):
            parser.error("--hover-mode must be 1–4 for --platform=hw")
        if args.platform == PlatformType.SIM and args.hover_mode not in range(1, 9):
            parser.error("--hover-mode must be 1–8 for --platform=sim")
    else:
        # Disallow hover-mode when not doing hover
        if args.hover_mode is not None:
            parser.error("--hover-mode is only valid when --trajectory=hover")




def main():
    """Main entry point for the executable."""
    parser = create_parser()
    args = parser.parse_args()
    validate_args(args, parser)

    platform=args.platform
    trajectory=args.trajectory
    hover_mode=args.hover_mode
    double_speed=args.double_speed
    short=args.short
    spin=args.spin
    log_file=args.log_file
    base_path = os.path.dirname(os.path.abspath(__file__))


    # Print configuration
    print("\n" + "="*60)
    print("NMPC Offboard Control Configuration")
    print("="*60)
    print(f"Platform:      {platform.upper()}")
    print(f"Trajectory:    {trajectory.upper()}")
    print(f"Hover Mode:    {hover_mode if hover_mode is not None else 'N/A'}")
    print(f"Speed:         {'Double (2x)' if double_speed else 'Regular (1x)'}")
    print(f"Short:         {'Enabled (fig8_vert)' if short else 'Disabled'}")
    print(f"Spin:          {'Enabled (circle_horz, helix)' if spin else 'Disabled'}")
    print(f"Log File:      {log_file}")
    print("="*60 + "\n")

    rclpy.init(args=None)
    offboard_control_node = OffboardControl(
        platform_type=platform,
        trajectory=trajectory,
        hover_mode=hover_mode,
        double_speed=double_speed,
        short=short,
        spin=spin,
    )

    logger = None

    def shutdown_logging(*args):
        print("\nShutting down, triggering logging...")
        if logger:
            logger.log(offboard_control_node)
        offboard_control_node.destroy_node()
        rclpy.shutdown()

    try:
        print(f"\nInitializing Offboard Control Node")
        logger = Logger(log_file, base_path)
        rclpy.spin(offboard_control_node)
    except KeyboardInterrupt:
        print("\nKeyboard interrupt (Ctrl+C)")
    except Exception as e:
        print(f"\nError: {e}")
        traceback.print_exc()
    finally:
        print("Saving log data...")
        shutdown_logging()

        print("\nNode shut down.")


if __name__ == '__main__':
    main()
