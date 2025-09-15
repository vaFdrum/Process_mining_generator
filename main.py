import argparse
import json
import random
from datetime import datetime, timedelta
from .logger import get_logger
from .case_generator import CaseGenerator
from .csv_writer import CSVWriter
from .config import CONFIG_20GB, CONFIG_30GB, CONFIG_50GB, CONFIG_CUSTOM
from .utils import distribute_processes

CONFIGS = {
    "20GB": CONFIG_20GB,
    "30GB": CONFIG_30GB,
    "50GB": CONFIG_50GB,
    "custom": CONFIG_CUSTOM,
}

def parse_arguments():
    parser = argparse.ArgumentParser(description="Process Mining Generator")
    parser.add_argument("--config", type=str, default="custom", choices=CONFIGS.keys())
    parser.add_argument("--cases", type=int, default=100, help="Total number of cases to generate")
    parser.add_argument("--output", type=str, help="Custom output directory (overrides config)")
    return parser.parse_args()

def main():
    args = parse_arguments()
    logger = get_logger()
    cfg = CONFIGS[args.config]
    if args.output:
        cfg = dict(cfg)
        cfg['output_dir'] = args.output

    logger.info(f"Using config: {args.config}")
    total_cases = args.cases
    distribution = distribute_processes(cfg['process_distribution'], total_cases)
    generator = CaseGenerator(start_case_id=1, logger=logger)
    writer = CSVWriter(logger=logger)

    start_time = datetime.fromisoformat(cfg.get('start_date', '2022-01-01'))
    out_path = cfg.get('output_dir', './dataset') + '/events.csv'
    logger.info(f"Generating {total_cases} cases -> {out_path}")

    logger.start_progress(total_cases)
    for process_name, count in distribution.items():
        if count == 0:
            continue
        events = generator.generate_batch(process_name, count, start_time)
        writer.write(events, out_path, append=True)
        logger.update_progress(count)
    logger.close_progress()
    logger.info("Generation complete.")

if __name__ == '__main__':
    main()
