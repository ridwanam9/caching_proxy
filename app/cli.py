import argparse

import httpx
import uvicorn

import app.server


def main():
    parser = argparse.ArgumentParser(
        description="A simple caching proxy server"
    )

    parser.add_argument(
        "--port",
        type=int,
        default=3000,
        help="Port where the proxy server will run"
    )

    parser.add_argument(
        "--origin",
        help="Origin server URL"
    )

    parser.add_argument(
        "--clear-cache",
        action="store_true",
        help="Clear the cache"
    )

    args = parser.parse_args()

    if args.clear_cache:
        url = f"http://127.0.0.1:{args.port}/clear-cache"

        try:
            response = httpx.delete(url)

            if response.status_code == 200:
                print("Cache cleared")
            else:
                print("Failed to clear cache")

        except httpx.ConnectError:
            print("Unable to connect to caching proxy.")
            print("Make sure the server is running.")

        return
    
    if args.origin is None:
        parser.error("--origin is required")

    app.server.origin = args.origin

    uvicorn.run(
        "app.server:app",
        host="127.0.0.1",
        port=args.port
    )


if __name__ == "__main__":
    main()