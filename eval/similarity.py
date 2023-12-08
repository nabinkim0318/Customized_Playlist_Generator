def calculate_average_rank(data):
    
    rank_sums = {}
    for group in data:
        for rank, item in enumerate(group, start=1):
            if item not in rank_sums:
                rank_sums[item] = 0
            rank_sums[item] += rank

    average_ranks = {item: total_rank / len(data) for item, total_rank in rank_sums.items()}
    return average_ranks

data_points = [
    ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
    ['2', '3', '1', '5', '4', '7', '6', '9', '8', '10'],
    ['3', '1', '2', '4', '5', '8', '6', '7', '9', '10'],
]

# Calculate average ranks
average_ranks = calculate_average_rank(data_points)
average_ranks

