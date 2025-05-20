import json
import csv
import glob


def flatten_json(y, prefix=''):
    out = {}
    if isinstance(y, dict):
        for k, v in y.items():
            out.update(flatten_json(v, f"{prefix}{k}_"))
    elif isinstance(y, list):
        for i, v in enumerate(y):
            out.update(flatten_json(v, f"{prefix}{i}_"))
    else:
        out[prefix[:-1]] = y
    return out


def main():
    json_files = glob.glob('data/**/*.json', recursive=True)
    for file_path in json_files:
        with open(file_path, 'r') as f:
            data = json.load(f)
        flat = flatten_json(data)
        csv_path = file_path.replace('.json', '.csv')
        with open(csv_path, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=flat.keys())
            writer.writeheader()
            writer.writerow(flat)


if __name__ == "__main__":
    main()
