import argparse
import uvicorn
import app.server
import httpx

def main():
    parser = argparse.ArgumentParser(
        description="A simple caching proxy server"
    )

    parser.add_argument(
        "--port",
        type=int,
        # required=True,
        help="Port where the proxy server will run"
    )

    parser.add_argument(
        "--origin",
        # required=True,
        help="Origin server URL"
    )
    parser.add_argument(
        "--clear-cache",
        action="store_true",
        help="Clear the cache"
    )


    args = parser.parse_args()

    if args.clear_cache:
        response = httpx.delete("http://127.0.0.1:3000/clear-cache")
        if response.status_code == 200:
            print("Cache cleared")
        else:
            print("Failed to clear cache")
        return
    
    if args.port is None or args.origin is None:
        parser.error("--port and --origin are required")

    app.server.origin = args.origin

    uvicorn.run(
        "app.server:app",
        host="127.0.0.1",
        port=args.port
    )
    
    
    print(f"Port: {args.port}")
    print(f"Origin: {args.origin}")

if __name__ == "__main__":
    main()