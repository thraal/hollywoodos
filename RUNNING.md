# Running HollywoodOS

## Basic Usage

```bash
python run.py [--config CONFIG] [--plugins PLUGINS]
```

- `--config`: path to `config.yaml` (default: `config.yaml`)
- `--plugins`: comma-separated list of plugins to load (e.g., system_monitor,log_scroll)

## Example

```bash
python run.py --config config.yaml.example --plugins system_monitor,log_scroll
```

## Troubleshooting

- Increase verbosity with `-v` or `-vv` flags.
- To save logs to a file:
  ```bash
  python run.py > hollywoodos.log 2>&1
  ```
