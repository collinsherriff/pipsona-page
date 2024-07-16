import numpy as np

persona_scores = {
    "Patient Planner": [3, 5, 4, 2, 1],
    "The Bandwagoner": [4, 4, 3, 2, 3],
    "The Overtrader": [3, 3, 4, 4, 5],
    "PVP Player": [2, 2, 4, 1, 3],
    "Bet and Forgetter": [5, 3, 4, 4, 2],
    "Volatility Seeker": [4, 2, 5, 3, 4]
}

def calculate_percentage_match(ocean_score, persona_scores):
    # Normalize ocean_score to 1-5 scale if necessary
    ocean_score = np.array([min(5, max(1, score)) for score in ocean_score])
    
    # Calculate the Euclidean distance to each persona's score
    distances = {}
    for persona, scores in persona_scores.items():
        distances[persona] = np.linalg.norm(ocean_score - np.array(scores))
    

    min_distance = min(distances.values())
    

    percentage_matches = {}
    total_inverse_distance = sum(1/d for d in distances.values())
    for persona, distance in distances.items():
        inverse_distance = 1 / distance if distance != 0 else float('inf')
        percentage_matches[persona] = (inverse_distance / total_inverse_distance) * 100
    
    return percentage_matches

# USE THIS HEREE
ocean_score = [3, 2, 4, 2, 4]
percentage_matches = calculate_percentage_match(ocean_score, persona_scores)
print(f"The percentage match for OCEAN score {ocean_score} is:")
for persona, percentage in percentage_matches.items():
    print(f"{persona}: {percentage:.2f}%")
