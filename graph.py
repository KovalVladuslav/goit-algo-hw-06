import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()

# Станції та з'єднання між ними для кожної лінії київського метро
stations = {
    "Red Line": ["Akademmistechko", "Sviatoshyn", "Nyvky", "Vokzalna", "Teatralna", "Khreshchatyk", "Dnipro", "Livoberezhna"],
    "Blue Line": ["Heroiv Dnipra", "Minska", "Obolon", "Pochaina", "Maidan Nezalezhnosti", "Ploshcha Lva Tolstoho", "Olimpiiska", "Lybidska"],
    "Green Line": ["Syrets", "Lukianivska", "Zoloti Vorota", "Palats Sportu", "Pecherska", "Druzhby Narodiv", "Vydubychi", "Osokorky"]
}

# Додаємо станції та з'єднання для кожної лінії
for line, line_stations in stations.items():
    for i in range(len(line_stations) - 1):
        G.add_edge(line_stations[i], line_stations[i + 1], line=line)  # Додаємо станції та зв'язки між ними

# Додаємо пересадочні вузли (перетини між лініями метро)
interchanges = [
    ("Teatralna", "Zoloti Vorota"),  # Червона та Зелена лінії
    ("Khreshchatyk", "Maidan Nezalezhnosti"),  # Червона та Синя лінії
    ("Ploshcha Lva Tolstoho", "Palats Sportu")  # Синя та Зелена лінії
]

# Створюємо пересадочні з'єднання між лініями
for station1, station2 in interchanges:
    G.add_edge(station1, station2, line="Transfer")

# Візуалізація графа
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G, seed=42)  # Визначаємо розташування вузлів
nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=500, font_size=8, font_weight="bold", edge_color="gray")
nx.draw_networkx_edges(G, pos, edgelist=[(station1, station2) for station1, station2 in interchanges], edge_color="red", width=2)  # Виділяємо пересадки червоним кольором
plt.title("Kyiv Metro Network with Interchanges")
plt.show()

# Аналіз основних характеристик графа
num_nodes = G.number_of_nodes()
num_edges = G.number_of_edges()
degrees = dict(G.degree())

print("Кількість вузлів (станцій):", num_nodes)
print("Кількість ребер (з'єднань):", num_edges)
print("Ступінь кожної вершини (кількість з'єднань для кожної станції):", degrees)

# Функція для пошуку шляху за допомогою DFS
def dfs_path(graph, start, goal, path=None):
    if path is None:
        path = [start]
    if start == goal:
        return path
    for neighbor in graph.neighbors(start):
        if neighbor not in path:
            result = dfs_path(graph, neighbor, goal, path + [neighbor])
            if result:
                return result
    return None

# Функція для пошуку шляху за допомогою BFS
def bfs_path(graph, start, goal):
    queue = [(start, [start])]
    while queue:
        (vertex, path) = queue.pop(0)
        for neighbor in graph.neighbors(vertex):
            if neighbor not in path:
                if neighbor == goal:
                    return path + [neighbor]
                queue.append((neighbor, path + [neighbor]))
    return None

# Вихідні дані для тестування
start_station = "Akademmistechko"
goal_station = "Osokorky"

# Пошук шляхів за допомогою DFS та BFS
dfs_result = dfs_path(G, start_station, goal_station)
bfs_result = bfs_path(G, start_station, goal_station)

print("DFS Path:", dfs_result)
print("BFS Path:", bfs_result)

if dfs_result and bfs_result:
    print("Порівняння:")
    print("DFS прагне досліджувати один шлях глибоко перед поверненням назад, що може призвести до довших та менш прямих маршрутів.")
    print("BFS досліджує рівень за рівнем, тому зазвичай знаходить найкоротший шлях у невзваженому графі, як ця мережа метро.")
else:
    print("Не вдалося знайти.")
