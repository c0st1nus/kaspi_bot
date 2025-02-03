import random
from user_agents.chrome_json import lists as chrome_list
from user_agents.firefox_json import lists as firefox_list


# Случайно достает юзер-агент из 3000 возможных вариантов.
def get_agent():
    random_number = random.randint(1, 2)

    if random_number == 1:
        agent = chrome_list

    elif random_number == 2:
        agent = firefox_list

    random_number_2 = random.randint(0, 1499)

    random_agent = agent[random_number_2]['ua']
    return random_agent


