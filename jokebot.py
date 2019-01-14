clearimport time, csv, sys, requests, json, re

# deliver jokes
def deliver(prompt, punch):
    print(prompt)
    time.sleep(2)
    print(punch)

# read user input
def read_user():
    user_input = input("enter 'next' for next joke or 'quit' to exit program: ")
    if user_input == "next":
        return True
    elif user_input == "quit":
        return False
    else:
        print("i don't understand. please try again")
        return read_user()



# 1. data source: csv file
def read_csv(file_name):
    with open(file_name, "r") as f:
        reader = csv.reader(f)
        jokes = list(reader)
    return jokebot(jokes)



# 2. data source: reddit
# gets list of reddit posts from /r/dadjokes; need to use non-default user-agent (too many requests)
def get_jokes():
    r = requests.get("https://www.reddit.com/r/dadjokes.json", headers={'User-agent': 'your bot 0.1'})
    return r.json()["data"]["children"]

# filter jokes
def filter_jokes(jokes):
    jokes = list(filter(lambda x: x["data"]["over_18"] == False, jokes))
    jokes = list(filter(lambda x: len(re.findall(r"^Why|^What|^How", x["data"]["title"])) != 0, jokes))
    return jokes

# extract titles and bodies
def extract_jokes(jokes):
    jokes_lst = []
    for i in range(len(jokes)):
        prompt = jokes[i]["data"]["title"]
        punch = jokes[i]["data"]["selftext"]
        jokes_lst += [[prompt, punch]]
    return jokes_lst

# get, filter, & extract
def read_reddit():
    raw_jokes = get_jokes()
    filtered_jokes = filter_jokes(raw_jokes)
    extracted_jokes = extract_jokes(filtered_jokes)
    return jokebot(extracted_jokes)



# execute jokebot
def jokebot(jokes_lst):
    num_of_jokes = len(jokes_lst)
    for i in range(num_of_jokes):
        if read_user(): # user entered "next"
            prompt = jokes_lst[i][0]
            punch = jokes_lst[i][1]
            deliver(prompt, punch)
            continue
        else: # user entered "quit"
            break

if __name__ == "__main__":
    if len(sys.argv) > 2:
        # error
        print("error: please choose one csv file to read from")
    elif len(sys.argv) == 2:
        # use csv file as data source
        read_csv(sys.argv[1])
    else:
        # use reddit as data source
        read_reddit()
