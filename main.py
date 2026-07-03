import random
# Grid size
GRID_SIZE = 5
# Health points
health = 20

Q = {}
actions = ["UP", "DOWN", "LEFT", "RIGHT"]

# Positions
agent_pos = [0, 0]
food_pos = [4, 4]
demon_pos = [3, 4]


def move_agent(position, action):
    x, y = position

    if action == "UP":
        x -= 1
    elif action == "DOWN":
        x += 1
    elif action == "LEFT":
        y -= 1
    elif action == "RIGHT":
        y += 1

    # Boundary check
    x = max(0, min(x, GRID_SIZE - 1))
    y = max(0, min(y, GRID_SIZE - 1))

    return [x, y]


def get_reward(agent):
    if agent == food_pos:
        return 10, "WIN"
    elif agent == demon_pos:
        return -10, "LOSE"
    else:
        return -1, "CONTINUE"

def get_q(state, action):
    return Q.get((state, action), 0)

def choose_action(state):
    if random.random() < 0.3:
        return random.choice(actions)  # explore
    else:
        q_values = [get_q(state, a) for a in actions]
        max_q = max(q_values)
        return actions[q_values.index(max_q)]
    
def update_q(state, action, reward, next_state):
    alpha = 0.1
    gamma = 0.9

    current_q = get_q(state, action)

    next_qs = [get_q(next_state, a) for a in actions]
    max_next_q = max(next_qs)

    new_q = current_q + alpha * (reward + gamma * max_next_q - current_q)

    Q[(state, action)] = new_q
    
# Game loop
while True:
    print("\nAgent position:", agent_pos)

    state = tuple(agent_pos)

    action = choose_action(state)
    print("Agent chose:", action)

    agent_pos = move_agent(agent_pos, action)

    reward, status = get_reward(agent_pos)

    health += reward
    print("Reward:", reward, "| Health:", health)

    next_state = tuple(agent_pos)

    update_q(state, action, reward, next_state)

    if status == "WIN":
        print("🎉 Agent reached food! You WIN!")
        break
    elif health <= 0:
        print("💀 Agent died due to no health!")
        break
    elif status == "LOSE":
        print("💀 Agent met demon! You LOSE!")
        break