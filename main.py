import random

# 定义扑克牌的花色和面值
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']

values = ['02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14']

# 11 => Jack
# 12 => Queen
# 13 => King
# 14 => Ace

# 生成一副扑克牌
deck = [{'value': value, 'suit': suit} for value in values for suit in suits]

# 定义牌型的名称和级别
hand_rankings = {
    'High Card': 0,
    'One Pair': 1,
    'Two Pair': 2,
    'Three of a Kind': 3,
    'Straight': 4,
    'Flush': 5,
    'Full House': 6,
    'Four of a Kind': 7,
    'Straight Flush': 8,
    'Royal Flush': 9,
}

# 定义玩家类
class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.hand_rank = None

# 发牌函数
def deal_cards(num_players, num_community_cards):
    random.shuffle(deck)
    players = [Player(f"Player {i+1}") for i in range(num_players)]
    community_cards = []

    # 每名玩家发两张底牌
    for _ in range(2):
        for player in players:
            player.hand.append(deck.pop())

    # 发五张公共牌
    for _ in range(num_community_cards):
        community_cards.append(deck.pop())

    return players, community_cards

def deep_copy_list(list1):
  """Creates a deep copy of the given list.

  Args:
    list1: A list.

  Returns:
    A deep copy of the given list.
  """

  new_list = []
  for item in list1:
    if isinstance(item, list):
      new_list.append(deep_copy_list(item))
    else:
      new_list.append(item)

  return new_list

# 评估牌型函数
def evaluate_hand(player,community_cards):
    all_cards = []
    copy_community_cards = deep_copy_list(community_cards)
    while player.hand:
        all_cards.append(player.hand.pop())
    while copy_community_cards:
        all_cards.append(copy_community_cards.pop())

    all_values = [card['value'] for card in all_cards]
    all_suits = [card['suit'] for card in all_cards]

    sorted_values = sorted(all_values,reverse=True)
    sorted_values = [int(item) for item in sorted_values]

    # 判断是否为同花
    is_flush = all_suits.count(all_suits[0]) == 5
    if is_flush == True:
        max_value = max(sorted_values)
    # 判断是否为顺子
    
    is_straight = max(sorted_values) - min(sorted_values) == 4
    if is_straight == True:
        max_value = max(sorted_values)


    # 计算每个面值的数量
    value_counts_temp = {value: all_values.count(value) for value in set(all_values)}
    value_counts = {}
    for key in sorted(value_counts_temp, reverse=True):
        value_counts[key] = value_counts_temp[key]

    # print('value_counts:',value_counts);

    # 找出最常见的面值和次数
    max_count = max(value_counts.values())
    max_value = int([value for value, count in value_counts.items() if count == max_count][0])

    # print('max_count',max_count);
    # print('max_value', max_value);

    # 评估牌型
    if is_straight and is_flush and '14' in all_values and '13' in all_values:
        return {'hand': 'Royal Flush', 'rank': hand_rankings['Royal Flush'], 'values': sorted_values, 'compare_values': max_value}
    elif is_straight and is_flush:
        return {'hand': 'Straight Flush', 'rank': hand_rankings['Straight Flush'], 'values': sorted_values, 'compare_values': max_value}
    elif max_count == 4:
        return {'hand': 'Four of a Kind', 'rank': hand_rankings['Four of a Kind'], 'values': sorted_values, 'compare_values': max_value}
    elif max_count == 3 and len(value_counts) == 2:
        return {'hand': 'Full House', 'rank': hand_rankings['Full House'], 'values': sorted_values, 'compare_values':max_value}
    elif is_flush:
        return {'hand': 'Flush', 'rank': hand_rankings['Flush'], 'values': sorted_values, 'compare_values': max_value}
    elif is_straight:
        return {'hand': 'Straight', 'rank': hand_rankings['Straight'], 'values': sorted_values, 'compare_values': max_value}
    elif max_count == 3:
        return {'hand': 'Three of a Kind', 'rank': hand_rankings['Three of a Kind'], 'values': sorted_values, 'compare_values': max_value}
    elif max_count == 2 and len(value_counts) == 3:
        return {'hand': 'Two Pair', 'rank': hand_rankings['Two Pair'], 'values': sorted_values, 'compare_values': max_value}
    elif max_count == 2:
        return {'hand': 'One Pair', 'rank': hand_rankings['One Pair'], 'values': sorted_values, 'compare_values': max_value}
    else:
        return {'hand': 'High Card', 'rank': hand_rankings['High Card'], 'values': sorted_values, 'compare_values': max_value}

# 在main函数中比较牌型
def main():
    num_players = 8
    num_community_cards = 5

    players, community_cards = deal_cards(num_players, num_community_cards)

    for item in community_cards:
        print(item)

    for player in players:
        print('name:',player.name,'hand:',player.hand)

    # 计算每位玩家的 hand rank
    for player in players:
        player.hand_rank = evaluate_hand(player,community_cards)
        # print(player.hand_rank)

    # 找到所有玩家中最高级别的牌型
    max_rank = max(player.hand_rank['rank'] for player in players)

    # 从具有最高级别的牌型的玩家中找出胜者
    winning_players = [player for player in players if player.hand_rank['rank'] == max_rank]

    print('winner_players',len(winning_players))

    if len(winning_players) == 1:
        winning_player = winning_players[0]
        winning_hand = winning_player.hand_rank['hand']
        print(f"\n{winning_player.name} wins with a {winning_hand}!")

    else:
        # 如果有多名玩家拥有相同级别的牌型，比较它们的牌面大小

        for player in winning_players:
            print(player.hand_rank)
        # 根据牌面大小找出胜者或宣布平局
        max_values = [player.hand_rank['compare_values'] for player in winning_players]
        max_values = sorted(max_values,reverse=True)[0]
        
        winning_players = [player for player in winning_players if player.hand_rank['compare_values'] == max_values]

        if len(winning_players) == 1:
            winning_player = winning_players[0]
            winning_hand = winning_player.hand_rank['hand']
            print(f"\n{winning_player.name} wins with a {winning_hand}!")
        else:
            print("It's a tie!")

if __name__ == "__main__":
    main()