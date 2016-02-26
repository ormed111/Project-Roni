from HQ import HeadQuarters as HQ

def main():
    hostname = raw_input("victim name: ",)
    hq = HQ(hostname)
    hq.run()
    raw_input()

if __name__ == "__main__":
    main()
