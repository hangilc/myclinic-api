from server_app import run
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=18080)
    args = parser.parse_args()
    run(args.port)
