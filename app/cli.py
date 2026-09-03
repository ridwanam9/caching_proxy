import argparse


def main():
    parser = argparse.ArgumentParser(
        description="A simple caching proxy server"
    )

    parser.add_argument(
        "--port",
        type=int,
        required=True,
        help="Port where the proxy server will run"
    )

    parser.add_argument(
        "--origin",
        required=True,
        help="Origin server URL"
    )

    args = parser.parse_args()

    print(f"Port: {args.port}")
    print(f"Origin: {args.origin}")


if __name__ == "__main__":
    main()