import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()

# Визначення станцій та ваг для з'єднань (умовні ваги)
stations = {
    "Red Line": [("Akademmistechko", "Sviatoshyn", 3), ("Sviatoshyn", "Nyvky", 2), ("Nyvky", "Vokzalna", 5), 
                 ("Vokzalna", "Teatralna", 4), ("Teatralna", "Khreshchatyk", 1), ("Khreshchatyk", "Dnipro", 6), 
                 ("Dnipro", "Livoberezhna", 4)],
    "Blue Line": [("Heroiv Dnipra", "Minska", 3), ("Minska", "Obolon", 2), ("Obolon", "Pochaina", 4), 
                  ("Pochaina", "Maidan Nezalezhnosti", 5), ("Maidan Nezalezhnosti", "Ploshcha Lva Tolstoho", 2), 
                  ("Ploshcha Lva Tolstoho", "Olimpiiska", 3), ("Olimpiiska", "Lybidska", 4)],
    "Green Line": [("Syrets", "Lukianivska", 3), ("Lukianivska", "Zoloti Vorota", 2), ("Zoloti Vorota", "Palats Sportu", 4), 
                   ("Palats Sportu", "Pecherska", 2), ("Pecherska", "Druzhby Narodiv", 3), ("Druzhby Narodiv", "Vydubychi", 4), 
                   ("Vydubychi", "Osokorky", 6)]
}

# Додавання станцій та з'єднань з вагами
for line, line_stations in stations.items():
    for station1, station2, weight in line_stations:
        G.add_edge(station1, station2, weight=weight, line=line)

# Додавання пересадочних станцій (перетинів) з вагами
interchanges = [
    ("Teatralna", "Zoloti Vorota", 1),  # Червона та Зелена лінії
    ("Khreshchatyk", "Maidan Nezalezhnosti", 1),  # Червона та Синя лінії
    ("Ploshcha Lva Tolstoho", "Palats Sportu", 1)  # Синя та Зелена лінії
]
for station1, station2, weight in interchanges:
    G.add_edge(station1, station2, weight=weight, line="Transfer")

# Візуалізація графа з вагами ребер
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=500, font_size=8, font_weight="bold", edge_color="gray")
nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): d["weight"] for u, v, d in G.edges(data=True)}, font_size=8)
plt.title("Kyiv Metro Network with Weights")
plt.show()

# Реалізація алгоритму Дейкстри для знаходження найкоротшого шляху
def dijkstra_shortest_path(graph, start, goal):
    return nx.dijkstra_path(graph, start, goal, weight="weight")

# Приклад: Знаходимо найкоротший шлях з "Akademmistechko" до "Osokorky"
start_station = "Akademmistechko"
goal_station = "Osokorky"
shortest_path = dijkstra_shortest_path(G, start_station, goal_station)
shortest_path_length = nx.dijkstra_path_length(G, start_station, goal_station, weight="weight")

print("Shortest path from", start_station, "to", goal_station, ":", shortest_path)
print("Shortest path length (total weight):", shortest_path_length)
