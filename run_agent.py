from tools.fetch_tool import FetchTool
from tools.s3_tool import S3Tool

def main():
    print("=== TEST: uruchomienie FetchTool ===")
    fetch = FetchTool()
    print(fetch.run(tool_input=""))

    print("\n=== TEST: pobranie snapshotu z S3Tool ===")
    s3 = S3Tool()
    print(s3.run(tool_input=""))

if __name__ == "__main__":
    main()
