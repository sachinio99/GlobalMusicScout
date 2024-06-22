from pathlib import Path 
import argparse 



def main():
    parser = argparse.ArgumentParser(description="CLI for getting params for API Call")
    parser.add_argument("user_location")
    args = parser.parse_args()
    print(args.user_location)








if __name__ == "__main__":
    main()