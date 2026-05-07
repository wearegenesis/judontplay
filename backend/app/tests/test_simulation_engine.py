from app.services.simulation_engine import simulate_bracket_monte_carlo


def test_normalized_lookup_used_for_scores():
    bracket = {"A": [("YANG YUNG WEI", "D Angelo Biagio")], "B": [], "C": [], "D": []}
    scores = {"Yang Yung Wei": 200.0, "D Angelo Biagio": 20.0}
    winner, _ = simulate_bracket_monte_carlo(bracket, scores, iterations=2000, seed=7)
    assert winner.get("YANG YUNG WEI", 0) > winner.get("D Angelo Biagio", 0)


def test_probabilities_shape_and_sums():
    bracket = {
        "A": [("A1", None), ("A2", None), ("A3", None), ("A4", "A5")],
        "B": [("B1", "B2"), ("B3", "B4")],
        "C": [("C1", "C2"), ("C3", "C4")],
        "D": [("D1", "D2"), ("D3", "D4")],
    }
    scores = {"A1": 180, "A2": 120, "A3": 110, "A4": 100, "A5": 90, "B1": 170, "B2": 80, "B3": 95, "B4": 94,
              "C1": 160, "C2": 85, "C3": 90, "C4": 70, "D1": 150, "D2": 88, "D3": 80, "D4": 78}
    winner, top4 = simulate_bracket_monte_carlo(bracket, scores, iterations=5000, seed=11)
    assert winner.get("A1", 0) > winner.get("A2", 0)
    assert abs(sum(winner.values()) - 1.0) < 0.03
    assert abs(sum(top4.values()) - 4.0) < 0.05
