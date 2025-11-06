# Newton Raphson Standard Control Command List

Below are organized, copy-ready command templates for running `run` with all platform and trajectory combinations.

---

## Command Structure

```bash
ros2 run newton_raphson_standard run --platform <PLATFORM> --trajectory <TRAJECTORY> [OPTIONS]
```

### Required Arguments
- `--platform`: `sim` (simulation) or `hw` (hardware)
- `--trajectory`: Trajectory type (see available trajectories below)

### Optional Arguments
- `--double-speed`: Use double speed (2x) for trajectories
- `--short`: Use short variant for fig8_vert trajectory
- `--spin`: Enable spin for circle_horz and helix trajectories
- `--pyjoules`: Enable PyJoules energy monitoring
- `--log-file <FILE>`: Custom log file name without extension (default: hybrid_mpc_log)
- `--hover-mode <MODE>`: Hover mode (1-6). **REQUIRED for hover trajectory**: use 1 for hardware, 6 for simulation

**Note:** Regular speed (1x) is the default. Add `--double-speed` flag for 2x speed.

### Available Trajectories
- `hover` - Stationary hover at specified position
- `yaw_only` - Yaw rotation only
- `circle_horz` - Horizontal circular trajectory
- `circle_vert` - Vertical circular trajectory
- `fig8_horz` - Horizontal figure-8 pattern
- `fig8_vert` - Vertical figure-8 pattern
- `helix` - Helical trajectory
- `sawtooth` - Sawtooth wave pattern
- `triangle` - Triangular trajectory

---

## SIMULATION - Double Speed (No PyJoules)

```bash
ros2 run newton_raphson_standard run --platform sim --trajectory hover --double-speed --hover-mode 6 --log-file sim_nr_std_hover_2x.csv
ros2 run newton_raphson_standard run --platform sim --trajectory yaw_only --double-speed --log-file sim_nr_std_yaw_only_2x.csv
ros2 run newton_raphson_standard run --platform sim --trajectory circle_horz --double-speed --log-file sim_nr_std_circle_horz_2x.csv
ros2 run newton_raphson_standard run --platform sim --trajectory circle_horz --double-speed --spin --log-file sim_nr_std_circle_horz_2x_spin.csv
ros2 run newton_raphson_standard run --platform sim --trajectory circle_vert --double-speed --log-file sim_nr_std_circle_vert_2x.csv
ros2 run newton_raphson_standard run --platform sim --trajectory fig8_horz --double-speed --log-file sim_nr_std_fig8_horz_2x.csv
ros2 run newton_raphson_standard run --platform sim --trajectory fig8_vert --double-speed --log-file sim_nr_std_fig8_vert_2x.csv
ros2 run newton_raphson_standard run --platform sim --trajectory fig8_vert --double-speed --short --log-file sim_nr_std_fig8_vert_2x_short.csv
ros2 run newton_raphson_standard run --platform sim --trajectory helix --double-speed --log-file sim_nr_std_helix_2x.csv
ros2 run newton_raphson_standard run --platform sim --trajectory helix --double-speed --spin --log-file sim_nr_std_helix_2x_spin.csv
ros2 run newton_raphson_standard run --platform sim --trajectory sawtooth --double-speed --log-file sim_nr_std_sawtooth_2x.csv
ros2 run newton_raphson_standard run --platform sim --trajectory triangle --double-speed --log-file sim_nr_std_triangle_2x.csv
```

---

## HARDWARE - Double Speed (No PyJoules)

```bash
ros2 run newton_raphson_standard run --platform hw --trajectory hover --double-speed --hover-mode 1 --log-file hw_nr_std_hover_2x.csv
ros2 run newton_raphson_standard run --platform hw --trajectory yaw_only --double-speed --log-file hw_nr_std_yaw_only_2x.csv
ros2 run newton_raphson_standard run --platform hw --trajectory circle_horz --double-speed --log-file hw_nr_std_circle_horz_2x.csv
ros2 run newton_raphson_standard run --platform hw --trajectory circle_horz --double-speed --spin --log-file hw_nr_std_circle_horz_2x_spin.csv
ros2 run newton_raphson_standard run --platform hw --trajectory circle_vert --double-speed --log-file hw_nr_std_circle_vert_2x.csv
ros2 run newton_raphson_standard run --platform hw --trajectory fig8_horz --double-speed --log-file hw_nr_std_fig8_horz_2x.csv
ros2 run newton_raphson_standard run --platform hw --trajectory fig8_vert --double-speed --log-file hw_nr_std_fig8_vert_2x.csv
ros2 run newton_raphson_standard run --platform hw --trajectory fig8_vert --double-speed --short --log-file hw_nr_std_fig8_vert_2x_short.csv
ros2 run newton_raphson_standard run --platform hw --trajectory helix --double-speed --log-file hw_nr_std_helix_2x.csv
ros2 run newton_raphson_standard run --platform hw --trajectory helix --double-speed --spin --log-file hw_nr_std_helix_2x_spin.csv
ros2 run newton_raphson_standard run --platform hw --trajectory sawtooth --double-speed --log-file hw_nr_std_sawtooth_2x.csv
ros2 run newton_raphson_standard run --platform hw --trajectory triangle --double-speed --log-file hw_nr_std_triangle_2x.csv
```

---

## SIMULATION - Double Speed (With PyJoules)

```bash
ros2 run newton_raphson_standard run --platform sim --trajectory hover --double-speed --hover-mode 6 --pyjoules --log-file sim_nr_std_hover_2x_pyj.csv
ros2 run newton_raphson_standard run --platform sim --trajectory yaw_only --double-speed --pyjoules --log-file sim_nr_std_yaw_only_2x_pyj.csv
ros2 run newton_raphson_standard run --platform sim --trajectory circle_horz --double-speed --pyjoules --log-file sim_nr_std_circle_horz_2x_pyj.csv
ros2 run newton_raphson_standard run --platform sim --trajectory circle_horz --double-speed --spin --pyjoules --log-file sim_nr_std_circle_horz_2x_spin_pyj.csv
ros2 run newton_raphson_standard run --platform sim --trajectory circle_vert --double-speed --pyjoules --log-file sim_nr_std_circle_vert_2x_pyj.csv
ros2 run newton_raphson_standard run --platform sim --trajectory fig8_horz --double-speed --pyjoules --log-file sim_nr_std_fig8_horz_2x_pyj.csv
ros2 run newton_raphson_standard run --platform sim --trajectory fig8_vert --double-speed --pyjoules --log-file sim_nr_std_fig8_vert_2x_pyj.csv
ros2 run newton_raphson_standard run --platform sim --trajectory fig8_vert --double-speed --short --pyjoules --log-file sim_nr_std_fig8_vert_2x_short_pyj.csv
ros2 run newton_raphson_standard run --platform sim --trajectory helix --double-speed --pyjoules --log-file sim_nr_std_helix_2x_pyj.csv
ros2 run newton_raphson_standard run --platform sim --trajectory helix --double-speed --spin --pyjoules --log-file sim_nr_std_helix_2x_spin_pyj.csv
ros2 run newton_raphson_standard run --platform sim --trajectory sawtooth --double-speed --pyjoules --log-file sim_nr_std_sawtooth_2x_pyj.csv
ros2 run newton_raphson_standard run --platform sim --trajectory triangle --double-speed --pyjoules --log-file sim_nr_std_triangle_2x_pyj.csv
```

---

## HARDWARE - Double Speed (With PyJoules)

```bash
ros2 run newton_raphson_standard run --platform hw --trajectory hover --double-speed --hover-mode 1 --pyjoules --log-file hw_nr_std_hover_2x_pyj.csv
ros2 run newton_raphson_standard run --platform hw --trajectory yaw_only --double-speed --pyjoules --log-file hw_nr_std_yaw_only_2x_pyj.csv
ros2 run newton_raphson_standard run --platform hw --trajectory circle_horz --double-speed --pyjoules --log-file hw_nr_std_circle_horz_2x_pyj.csv
ros2 run newton_raphson_standard run --platform hw --trajectory circle_horz --double-speed --spin --pyjoules --log-file hw_nr_std_circle_horz_2x_spin_pyj.csv
ros2 run newton_raphson_standard run --platform hw --trajectory circle_vert --double-speed --pyjoules --log-file hw_nr_std_circle_vert_2x_pyj.csv
ros2 run newton_raphson_standard run --platform hw --trajectory fig8_horz --double-speed --pyjoules --log-file hw_nr_std_fig8_horz_2x_pyj.csv
ros2 run newton_raphson_standard run --platform hw --trajectory fig8_vert --double-speed --pyjoules --log-file hw_nr_std_fig8_vert_2x_short_pyj.csv
ros2 run newton_raphson_standard run --platform hw --trajectory fig8_vert --double-speed --short --pyjoules --log-file hw_nr_std_fig8_vert_2x_short_pyj.csv
ros2 run newton_raphson_standard run --platform hw --trajectory helix --double-speed --pyjoules --log-file hw_nr_std_helix_2x_pyj.csv
ros2 run newton_raphson_standard run --platform hw --trajectory helix --double-speed --spin --pyjoules --log-file hw_nr_std_helix_2x_spin_pyj.csv
ros2 run newton_raphson_standard run --platform hw --trajectory sawtooth --double-speed --pyjoules --log-file hw_nr_std_sawtooth_2x_pyj.csv
ros2 run newton_raphson_standard run --platform hw --trajectory triangle --double-speed --pyjoules --log-file hw_nr_std_triangle_2x_pyj.csv
```

---

## Quick Reference

### Basic Usage
```bash
# Simulation at regular speed (default)
ros2 run newton_raphson_standard run --platform sim --trajectory circle_horz

# Simulation at double speed
ros2 run newton_raphson_standard run --platform sim --trajectory circle_horz --double-speed

# Hardware with PyJoules monitoring at double speed
ros2 run newton_raphson_standard run --platform hw --trajectory fig8_vert --double-speed --pyjoules

# Custom log file
ros2 run newton_raphson_standard run --platform sim --trajectory helix --double-speed --log-file my_experiment.csv
```

### Common Combinations
```bash
# Regular speed testing
ros2 run newton_raphson_standard run --platform sim --trajectory circle_horz --log-file regular_speed_test.csv

# Double speed with energy monitoring
ros2 run newton_raphson_standard run --platform sim --trajectory circle_horz --double-speed --pyjoules --log-file energy_test.csv

# Performance testing at double speed
ros2 run newton_raphson_standard run --platform sim --trajectory fig8_vert --double-speed --log-file performance_test.csv

# Figure-8 vertical with short variant
ros2 run newton_raphson_standard run --platform sim --trajectory fig8_vert --double-speed --short --log-file fig8_short_test.csv

# Circle horizontal with spin
ros2 run newton_raphson_standard run --platform sim --trajectory circle_horz --double-speed --spin --log-file circle_spin_test.csv

# Helix with spin
ros2 run newton_raphson_standard run --platform sim --trajectory helix --double-speed --spin --log-file helix_spin_test.csv

# Hardware validation at regular speed
ros2 run newton_raphson_standard run --platform hw --trajectory hover --hover-mode 1 --pyjoules --log-file hw_validation.csv
```

---

## Notes

1. **Platform Selection**:
   - `sim`: Uses simulation parameters (mass, motor constants, etc.)
   - `hw`: Uses hardware-specific parameters

2. **Speed Options**:
   - **Default**: Regular speed (1x)
   - **With `--double-speed`**: Double speed (2x)

3. **PyJoules**:
   - Enables energy consumption monitoring
   - Useful for performance analysis and optimization

4. **Log Files**:
   - Automatically saved with `.csv` extension
   - Contains state, control, and timing data
   - Default location: workspace directory

5. **Trajectory Notes**:
   - All trajectories adapt to platform (sim vs hw heights)
   - **Hover trajectory requires `--hover-mode` flag**: use mode 1 for hardware, mode 6 for simulation
   - Speed multiplier affects trajectory execution rate

6. **Trajectory-Specific Options**:
   - `--short`: Only applicable to fig8_vert trajectory
   - `--spin`: Only applicable to circle_horz and helix trajectories
   - These options are ignored for other trajectory types
