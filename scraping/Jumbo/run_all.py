import subprocess

def main():
    print("Running link_collector.py...")
    subprocess.run(["python", "link_collector.py"], check=True)

    print("Running scraper.py...")
    subprocess.run(["python", "scraper.py"], check=True)

if __name__ == "__main__":
    main()
