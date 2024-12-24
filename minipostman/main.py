import sys

from request import Request


def main():
    if len(sys.argv) < 2:
        raise Exception("Usage: make request REQUEST_NAME [ENV_NAME]")

    request_name = sys.argv[1]

    env = sys.argv[2] if len(sys.argv) > 2 else None

    Request.new_request("requests.yaml", request_name, env).send()


if __name__ == "__main__":
    main()
