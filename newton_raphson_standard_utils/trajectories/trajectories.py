"""
Trajectory Generation for NMPC
================================

This module provides JIT-compiled trajectory generation functions adapted from px4_ros_com_py.
Each trajectory returns both position and velocity (via automatic differentiation)
to enable generation of full 9D reference trajectories for the MPC horizon.

Key Features:
- JAX JIT compilation for performance
- Automatic velocity computation via jacfwd
- Linear interpolation for horizon generation
- Consistent interface with TrajContext

Design:
- Trajectories return (pos, vel) tuples
- pos: [x, y, z, yaw] (4D)
- vel: [vx, vy, vz, yaw_rate] (4D) computed via automatic differentiation
- Full 9D reference generated via linear extrapolation
"""


import jax
from jax import jacfwd
import jax.numpy as jnp
from basic_clean_offboard_utils.jax_utils import jit


import numpy as np
from dataclasses import dataclass
from typing import Tuple, Optional, Union
from enum import StrEnum



@dataclass(frozen=True)
class TrajContext:
    """Context object containing trajectory parameters."""
    sim: bool
    hover_mode: Optional[int] = None
    spin: Optional[bool] = None
    double_speed: Optional[bool] = None
    short: Optional[bool] = None


class TrajectoryType(StrEnum):
    """Enumeration of available trajectories."""
    HOVER = "hover"
    YAW_ONLY = "yaw_only"
    CIRCLE_HORIZONTAL = "circle_horz"
    CIRCLE_VERTICAL = "circle_vert"
    FIG8_HORIZONTAL = "fig8_horz"
    FIG8_VERTICAL = "fig8_vert"
    HELIX = "helix"
    SAWTOOTH = "sawtooth"
    TRIANGLE = "triangle"


# Default heights
SIM_HEIGHT = 5.0
HARDWARE_HEIGHT = 0.85

RETURN_TYPE = Tuple[jnp.ndarray, jnp.ndarray, jnp.ndarray] | Tuple[jnp.ndarray, jnp.ndarray] | jnp.ndarray


@jit(static_argnames=("ctx",))
def hover(t_traj: float, ctx: TrajContext) -> RETURN_TYPE:
    """Returns constant hover reference trajectories."""
    mode = ctx.hover_mode if ctx.hover_mode is not None else 1
    sim = ctx.sim

    hover_dict = {
        1: jnp.array([0.0, 0.0, -0.9, 0.0]),
        2: jnp.array([0.0, 0.8, -0.8, 0.0]),
        3: jnp.array([0.8, 0.0, -0.8, 0.0]),
        4: jnp.array([0.8, 0.8, -0.8, 0.0]),
        5: jnp.array([0.0, 0.0, -10.0, 0.0]),
        6: jnp.array([1.0, 1.0, -4.0, 0.0]),
        7: jnp.array([0.0, 10.0, -5.0, 0.0]),
        8: jnp.array([1.0, 1.0, -3.0, 0.0]),
    }

    if mode not in hover_dict:
        raise ValueError(f"hover_dict #{mode} not found")

    if not sim and mode > 4:
        raise RuntimeError("hover modes 5+ not available for hardware")

    pos = hover_dict[mode]
    # vel =jnp.zeros(4)  # Stationary
    # accel = jnp.zeros(4)  # Stationary
    return pos #, vel , accel


@jit(static_argnames=("ctx",))
def yawing_only(t_traj: float, ctx: TrajContext) -> RETURN_TYPE:
    """Returns stationary yawing reference trajectory."""
    height = HARDWARE_HEIGHT if not ctx.sim else SIM_HEIGHT
    spin_period = 20.0

    if ctx.double_speed:
        spin_period /= 2.0

    def get_trajectory(t: float) -> jnp.ndarray:
        x = 0.0
        y = 0.0
        z = -height
        yaw = t / (spin_period / (2 * jnp.pi))
        return jnp.array([x, y, z, yaw], dtype=jnp.float64)

    pos = get_trajectory(t_traj)
    # vel =jacfwd(get_trajectory)(t_traj)
    # accel = jacfwd(jacfwd(get_trajectory))(t_traj)

    return pos #, vel , accel


@jit(static_argnames=("ctx",))
def circle_horizontal(t_traj: float, ctx: TrajContext) -> RETURN_TYPE:
    """Returns a horizontal circle trajectory."""
    radius = 0.6
    period_pos = 13.0
    height = HARDWARE_HEIGHT if not ctx.sim else SIM_HEIGHT
    period_spin = 20.0

    omega_spin = 2 * jnp.pi / period_spin if ctx.spin else 0.0
    if ctx.double_speed:
        period_pos /= 2.0
    omega_pos = 2 * jnp.pi / period_pos

    def get_trajectory(t: float) -> jnp.ndarray:
        x = radius * jnp.cos(omega_pos * t)
        y = radius * jnp.sin(omega_pos * t)
        z = -height
        yaw = omega_spin * t
        return jnp.array([x, y, z, yaw], dtype=jnp.float64)

    pos = get_trajectory(t_traj)
    # vel =jacfwd(get_trajectory)(t_traj)
    # accel = jacfwd(jacfwd(get_trajectory))(t_traj)

    return pos #, vel , accel


@jit(static_argnames=("ctx",))
def circle_vertical(t_traj: float, ctx: TrajContext) -> RETURN_TYPE:
    """Returns a vertical circle trajectory."""
    radius = 0.35
    period_pos = 13.0
    height = HARDWARE_HEIGHT if not ctx.sim else SIM_HEIGHT
    period_spin = 20.0

    omega_spin = 2 * jnp.pi / period_spin if ctx.spin else 0.0
    if ctx.double_speed:
        period_pos /= 2.0
    omega_pos = 2 * jnp.pi / period_pos

    def get_trajectory(t: float) -> jnp.ndarray:
        x = radius * jnp.cos(omega_pos * t)
        y = 0.0
        z = -radius * jnp.sin(omega_pos * t) - height
        yaw = omega_spin * t
        return jnp.array([x, y, z, yaw], dtype=jnp.float64)

    pos = get_trajectory(t_traj)
    # vel =jacfwd(get_trajectory)(t_traj)
    # accel = jacfwd(jacfwd(get_trajectory))(t_traj)

    return pos #, vel , accel


@jit(static_argnames=("ctx",))
def fig8_horizontal(t_traj: float, ctx: TrajContext) -> RETURN_TYPE:
    """Returns a horizontal figure-8 trajectory."""
    radius = 0.35
    period_pos = 13.0
    height = HARDWARE_HEIGHT if not ctx.sim else SIM_HEIGHT
    period_spin = 20.0

    omega_spin = 2 * jnp.pi / period_spin if ctx.spin else 0.0
    if ctx.double_speed:
        period_pos /= 2.0
    omega_pos = 2 * jnp.pi / period_pos

    def get_trajectory(t: float) -> jnp.ndarray:
        x = radius * jnp.sin(2 * omega_pos * t)
        y = radius * jnp.sin(omega_pos * t)
        z = -height
        yaw = omega_spin * t
        return jnp.array([x, y, z, yaw], dtype=jnp.float64)

    pos = get_trajectory(t_traj)
    # vel =jacfwd(get_trajectory)(t_traj)
    # accel = jacfwd(jacfwd(get_trajectory))(t_traj)

    return pos #, vel , accel


@jit(static_argnames=("ctx",))
def fig8_vertical(t_traj: float, ctx: TrajContext) -> RETURN_TYPE:
    """Returns a vertical figure-8 trajectory."""
    radius = 0.35
    period_pos = 13.0
    height = HARDWARE_HEIGHT if not ctx.sim else SIM_HEIGHT
    period_spin = 20.0

    omega_spin = 2 * jnp.pi / period_spin if ctx.spin else 0.0
    if ctx.double_speed:
        period_pos /= 2.0
    omega_pos = 2 * jnp.pi / period_pos

    def get_trajectory(t: float) -> jnp.ndarray:
        x = 0.0

        yz1 = radius * jnp.sin(omega_pos * t)
        yz2 = radius * jnp.sin(2 * omega_pos * t)
        y = jnp.where(ctx.short, yz1, yz2)  # type: ignore
        z = jnp.where(ctx.short, -yz2 - height, -yz1 - height) # type: ignore

        yaw = omega_spin * t
        return jnp.array([x, y, z, yaw], dtype=jnp.float64)

    pos = get_trajectory(t_traj)
    # vel =jacfwd(get_trajectory)(t_traj)
    # accel = jacfwd(jacfwd(get_trajectory))(t_traj)

    return pos #, vel , accel


@jit(static_argnames=("ctx",))
def helix(t_traj: float, ctx: TrajContext) -> RETURN_TYPE:
    """Returns a helix trajectory that spirals up and down."""
    z0 = HARDWARE_HEIGHT if not ctx.sim else 2.0
    z_max = 2.6 if not ctx.sim else SIM_HEIGHT
    radius = 0.6
    num_turns = 3
    cycle_time = 30.0
    period_spin = 20.0

    omega_spin = 2 * jnp.pi / period_spin if ctx.spin else 0.0

    if ctx.double_speed:
        cycle_time /= 2.0

    def get_trajectory(t: float) -> jnp.ndarray:
        t_cycle = t % cycle_time
        T_half = cycle_time / 2.0

        # Use jnp.where for differentiability instead of if/else
        # Going up branch
        z_up = z0 + (z_max - z0) * (t_cycle / T_half)
        progress_up = (z_up - z0) / (z_max - z0)

        # Going down branch
        t_down = t_cycle - T_half
        z_down = z_max - (z_max - z0) * (t_down / T_half)
        progress_down = (z_down - z0) / (z_max - z0)

        # Select based on condition using jnp.where for differentiability
        z = jnp.where(t_cycle <= T_half, z_up, z_down)
        progress = jnp.where(t_cycle <= T_half, progress_up, progress_down)

        # Angle is based on progress through the cycle
        theta = 2 * jnp.pi * num_turns * progress
        x = radius * jnp.cos(theta)
        y = radius * jnp.sin(theta)
        yaw = omega_spin * t

        return jnp.array([x, y, -z, yaw], dtype=jnp.float64)

    pos = get_trajectory(t_traj)
    # vel =jacfwd(get_trajectory)(t_traj)
    # accel = jacfwd(jacfwd(get_trajectory))(t_traj)

    return pos #, vel , accel


@jit(static_argnames=("ctx",))
def sawtooth(t_traj: float, ctx: TrajContext) -> RETURN_TYPE:
    """Returns a sawtooth pattern reference trajectory."""
    height = HARDWARE_HEIGHT if not ctx.sim else SIM_HEIGHT
    flight_time = 60.0
    num_repeats = 2 if ctx.double_speed else 1
    period_spin = 20.0

    omega_spin = 2 * jnp.pi / period_spin if ctx.spin else 0.0

    # Waypoints
    points = jnp.array([
        [0.0, 0.0], [0.0, 0.4], [0.4, -0.4], [0.4, 0.4], [0.4, -0.4],
        [0.0, 0.4], [0.0, -0.4], [-0.4, 0.4], [-0.4, -0.4],
        [-0.4, 0.4], [0.0, -0.4], [0.0, 0.0]
    ], dtype=jnp.float64)

    def get_trajectory(t: float) -> jnp.ndarray:
        # Adjust flight time based on number of repetitions
        adjusted_flight_time = flight_time / num_repeats
        num_segments = len(points) - 1
        T_seg = adjusted_flight_time / num_segments

        # Calculate time within current cycle
        cycle_time = t % (num_segments * T_seg)

        # Determine segment index (continuous)
        segment_idx = jnp.floor(cycle_time / T_seg)
        segment_idx = jnp.clip(segment_idx, 0, num_segments - 1).astype(int)

        # Time within the current segment
        local_time = cycle_time - segment_idx * T_seg

        # Linear interpolation
        start_point = points[segment_idx]
        end_point = points[(segment_idx + 1) % len(points)]

        alpha = local_time / T_seg
        x = start_point[0] + (end_point[0] - start_point[0]) * alpha
        y = start_point[1] + (end_point[1] - start_point[1]) * alpha
        z = -height
        yaw = omega_spin * t

        return jnp.array([x, y, z, yaw], dtype=jnp.float64)

    pos = get_trajectory(t_traj)
    # vel =jacfwd(get_trajectory)(t_traj)
    # accel = jacfwd(jacfwd(get_trajectory))(t_traj)

    return pos #, vel , accel


@jit(static_argnames=("ctx",))
def triangle(t_traj: float, ctx: TrajContext) -> RETURN_TYPE:
    """Returns an equilateral triangle reference trajectory."""
    height = HARDWARE_HEIGHT if not ctx.sim else SIM_HEIGHT
    side_length = 0.6
    flight_time = 60.0
    num_repeats = 2 if ctx.double_speed else 1
    period_spin = 20.0

    omega_spin = 2 * jnp.pi / period_spin if ctx.spin else 0.0

    # Triangle vertices
    h = jnp.sqrt(side_length**2 - (side_length/2)**2)
    points = jnp.array([
        [0.0, h/2],
        [side_length/2, -h/2],
        [-side_length/2, -h/2]
    ], dtype=jnp.float64)

    def get_trajectory(t: float) -> jnp.ndarray:
        # Calculate segment time
        T_seg = flight_time / (3 * num_repeats)

        # Calculate time within current cycle
        cycle_time = t % (3 * T_seg)

        # Determine segment index
        segment_idx = jnp.floor(cycle_time / T_seg)
        segment_idx = jnp.clip(segment_idx, 0, 2).astype(int)

        # Time within the current segment
        local_time = cycle_time - segment_idx * T_seg

        # Linear interpolation
        start_point = points[segment_idx]
        end_point = points[(segment_idx + 1) % 3]

        alpha = local_time / T_seg
        x = start_point[0] + (end_point[0] - start_point[0]) * alpha
        y = start_point[1] + (end_point[1] - start_point[1]) * alpha
        z = -height
        yaw = omega_spin * t

        return jnp.array([x, y, z, yaw], dtype=jnp.float64)

    pos = get_trajectory(t_traj)
    # vel =jacfwd(get_trajectory)(t_traj)
    # accel = jacfwd(jacfwd(get_trajectory))(t_traj)

    return pos #, vel , accel


# Trajectory registry
TRAJ_REGISTRY = {
    TrajectoryType.HOVER: hover,
    TrajectoryType.YAW_ONLY: yawing_only,
    TrajectoryType.CIRCLE_HORIZONTAL: circle_horizontal,
    TrajectoryType.CIRCLE_VERTICAL: circle_vertical,
    TrajectoryType.FIG8_HORIZONTAL: fig8_horizontal,
    TrajectoryType.FIG8_VERTICAL: fig8_vertical,
    TrajectoryType.HELIX: helix,
    TrajectoryType.SAWTOOTH: sawtooth,
    TrajectoryType.TRIANGLE: triangle,
}


def generate_reference_trajectory(
    traj_func,
    t_start: float,
    horizon: float,
    num_steps: int,
    ctx
) -> RETURN_TYPE:
    """
    Generate full 9D reference trajectory for an MPC horizon.

    Args:
        traj_func: Trajectory function that returns (pos, vel) where each is
                   jnp.ndarray of shape (4,) in the order [x, y, z, yaw] and
                   [vx, vy, vz, yaw_rate].
        t_start:  Starting time for trajectory (seconds).
        horizon:  Prediction horizon length (seconds).
        num_steps: Number of discretization steps (>=1).
        ctx:      Trajectory context (passed as the static arg to traj_func).

    Returns:
        refs: numpy array of shape (9, num_steps) with rows:
              [x, y, z, vx, vy, vz, roll, pitch, yaw],
              with roll = pitch = 0.0.
    """
    if num_steps <= 0:
        raise ValueError("num_steps must be >= 1")

    # Sample times (inclusive of both ends when num_steps > 1)
    if num_steps == 1:
        t_samples = jnp.array([t_start], dtype=jnp.float64)
    else:
        t_samples = jnp.linspace(t_start, t_start + horizon, num_steps, dtype=jnp.float64)

    # Map a single time to the 9D reference state
    def one_sample(t: jnp.float64) -> RETURN_TYPE: # type: ignore
        # pos, vel, accel = traj_func(t, ctx)   # pos: [x, y, z, yaw], vel: [vx, vy, vz, yaw_rate]
        pos = traj_func(t, ctx)   # pos: [x, y, z, yaw], vel: [vx, vy, vz, yaw_rate]
        # pos = pos.astype(jnp.float64)
        # vel = vel.astype(jnp.float64)
        # accel = accel.astype(jnp.float64)

        # x, y, z, yaw = pos
        # vx, vy, vz, yaw_rate = vel
        # ax, ay, az, yaw_accel = accel

        # roll, pitch are zeros (float64)
        return pos

    # Vectorize over all sample times; ctx stays constant (static) for your jitted traj funcs
    pos_jax = jax.vmap(one_sample)(t_samples)         # shape: (num_steps, 12)
    print(f"Generated trajectory: {pos_jax}")
    return pos_jax