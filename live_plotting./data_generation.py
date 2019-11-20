import csv
import random
import time

def generate_data(sleep_time=5, filename="data.csv", fields={"x": 0, "y1": 500, "y2": 500}):
    field_names = fields.keys()
    x, y1, y2 = fields["x"], fields["y1"], fields["y2"]

    # write file header
    with open(filename, 'w') as f:  # context manager
        csv_writer = csv.DictWriter(f, fieldnames=field_names)
        csv_writer.writeheader()
    
    # add data as long as the code is running
    while True:
        with open('data.csv', 'a') as f:
            csv_writer = csv.DictWriter(f, fieldnames=field_names)

            data = {
                    "x": x,
                    "y1": y1,
                    "y2": y2
                    }

            csv_writer.writerow(data)
            print("New row:", *data.values())

            x += 1
            y1 += random.randint(-3, 11)
            y2 += random.randint(-11, 3)

        time.sleep(sleep_time)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="data saving parameters")

    parser.add_argument("--x_start", type=int, dest="x", default=0,
                        help="Starting value of the x variable.")
    parser.add_argument("--y1_start", type=int, dest="y1", default=500,
                        help="Starting value of the y1 variable.")
    parser.add_argument("--y2_start", type=int, dest="y2", default=500,
                        help="Starting value of the y2 variable.")
    parser.add_argument("--sleep_time", type=int, dest="sleep_time", default=5,
                        help="Sleeping time between each data line addtion (in seconds).") 
    parser.add_argument("--save_path", type=str, dest="save_path", default="data.csv",
                        help="Path to file in which the data shall be saved.")                       

    args = parser.parse_args()
    fields = {"x": args.x, "y1": args.y1, "y2": args.y2}

    generate_data(args.sleep_time, args.save_path, fields)    


