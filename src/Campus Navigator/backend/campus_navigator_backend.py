#!/usr/bin/env python3
import heapq
from collections import deque
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import argparse

class DisjointSet:
    
    def __init__(self):
        self.parent = {}
        self.rank = {}
    
    def make_set(self, x):
        if x not in self.parent:
            self.parent[x] = x
            self.rank[x] = 0
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self.rank[rx] < self.rank[ry]:
            self.parent[rx] = ry
        elif self.rank[rx] > self.rank[ry]:
            self.parent[ry] = rx
        else:
            self.parent[ry] = rx
            self.rank[rx] += 1
        return True

class Graph:
   
    def __init__(self, undirected: bool = True):
        self.adj: Dict[str, List[Tuple[str, float]]] = {}
        self.undirected = undirected

    def add_node(self, u: str):
        
        self.adj.setdefault(u, [])

    def add_edge(self, u: str, v: str, w: float):
        
        self.add_node(u)
        self.add_node(v)
        self.adj[u].append((v, w))
        if self.undirected:
            self.adj[v].append((u, w))

    def nodes(self) -> List[str]:
        
        return list(self.adj.keys())

    def edges(self) -> List[Tuple[str, str, float]]:
       
        seen = set()
        es = []
        for u, nbrs in self.adj.items():
            for v, w in nbrs:
                if self.undirected:
                    key = tuple(sorted((u, v))) + (w,)
                    if key in seen:
                        continue
                    seen.add(key)
                es.append((u, v, w))
        return es

    def bfs(self, start: str) -> Tuple[List[str], Dict[str, Optional[str]]]:
        
        if start not in self.adj:
            return [], {}
        q = deque([start])
        visited = {start}
        parent: Dict[str, Optional[str]] = {start: None}
        order = []
        while q:
            u = q.popleft()
            order.append(u)
            for v, _ in self.adj[u]:
                if v not in visited:
                    visited.add(v)
                    parent[v] = u
                    q.append(v)
        return order, parent

    def dfs(self, start: str) -> List[str]:
        
        if start not in self.adj:
            return []
        stack = [start]
        visited = set()
        order = []
        while stack:
            u = stack.pop()
            if u in visited:
                continue
            visited.add(u)
            order.append(u)
            for v, _ in reversed(self.adj[u]):
                if v not in visited:
                    stack.append(v)
        return order

    def dijkstra(self, src: str, dst: str) -> Tuple[float, List[str]]:
        
        if src not in self.adj or dst not in self.adj:
            return float("inf"), []
        dist = {node: float("inf") for node in self.adj}
        prev = {node: None for node in self.adj}
        dist[src] = 0.0
        pq = [(0.0, src)]
        while pq:
            d, u = heapq.heappop(pq)
            if d > dist[u]:
                continue
            if u == dst:
                break
            for v, w in self.adj[u]:
                nd = d + w
                if nd < dist[v]:
                    dist[v] = nd
                    prev[v] = u
                    heapq.heappush(pq, (nd, v))
        if dist[dst] == float("inf"):
            return float("inf"), []
        path = []
        cur = dst
        while cur is not None:
            path.append(cur)
            cur = prev[cur]
        path.reverse()
        return dist[dst], path

    def kruskal_mst(self) -> Tuple[float, List[Tuple[str, str, float]]]:
        
        if not self.undirected:
            raise ValueError("Kruskal requires an undirected graph.")
        dsu = DisjointSet()
        for u in self.adj:
            dsu.make_set(u)
        edges = sorted(self.edges(), key=lambda e: e[2])
        mst = []
        total = 0.0
        for u, v, w in edges:
            if dsu.find(u) != dsu.find(v):
                dsu.union(u, v)
                mst.append((u, v, w))
                total += w
        return total, mst

@dataclass
class BSTNode:
   
    key: str
    left: Optional["BSTNode"] = None
    right: Optional["BSTNode"] = None

class BST:
    
    def __init__(self):
        self.root: Optional[BSTNode] = None

    def insert(self, key: str):
        
        self.root = self._insert(self.root, key)

    def _insert(self, node: Optional[BSTNode], key: str) -> BSTNode:
        if node is None:
            return BSTNode(key)
        if key < node.key:
            node.left = self._insert(node.left, key)
        elif key > node.key:
            node.right = self._insert(node.right, key)
        return node

    def search(self, key: str) -> bool:
        
        cur = self.root
        while cur:
            if key == cur.key:
                return True
            cur = cur.left if key < cur.key else cur.right
        return False

    def inorder(self) -> List[str]:
        
        out: List[str] = []
        def _in(node: Optional[BSTNode]):
            if not node:
                return
            _in(node.left)
            out.append(node.key)
            _in(node.right)
        _in(self.root)
        return out

def create_campus_graph() -> Tuple[Graph, BST]:
    
    g = Graph(undirected=True)
    edges = [
        # Ground floor B1
        ("Cafeteria", "LectureHall2", 5),
        ("LectureHall2", "LectureHall1", 5),
        ("LectureHall1", "AssistantsOffice", 3),
        ("AssistantsOffice", "LectureHall3", 6),
        ("LectureHall3", "PaymentOffice", 4),
        ("PaymentOffice", "Stairs_B1_GF", 2),
        ("Cafeteria", "Stairs_B2_GF", 2),

        # Building 2
        ("Stairs_B2_GF", "B2_GF", 1),
        ("B2_GF", "B2_F1", 10),
        ("B2_F1", "B2_F2", 10),
        ("B2_F2", "Auditorium", 2),
        ("B2_F2", "StudyArea", 5),

        # First floor B1
        ("Stairs_B1_GF", "LectureHall4", 10),
        ("LectureHall4", "LectureHall5", 2),
        ("LectureHall5", "LectureHall6", 2),

        # Second floor B1
        ("LectureHall4", "BusinessOffice", 10),
        ("BusinessOffice", "LectureHallA", 2),
        ("BusinessOffice", "LectureHallB", 2),
        ("LectureHallA", "StudyArea", 3),
        ("LectureHallB", "StudyArea", 3),
        ("BusinessOffice", "LectureHall7_10", 6),
        ("LectureHall7_10", "OutsideArea", 4),
        ("OutsideArea", "B2_F2", 8),
        ("StudyArea", "B2_F2", 5),

        # Third floor B1
        ("BusinessOffice", "Library", 15),
        ("Library", "EngineeringSection", 5),

        # Fourth floor B1
        ("Library", "ComputingOffice", 15),
        ("ComputingOffice", "ComputingLab", 3),
        ("ComputingLab", "TeachersOffices", 3),
        ("ComputingOffice", "HarrisonHall", 4),
        ("HarrisonHall", "NetEngLab", 4),
        ("NetEngLab", "Lab01", 3),
    ]
    
    
    for u, v, w in edges:
        g.add_edge(u, v, float(w))

    
    bst = BST()
    for name in g.nodes():
        bst.insert(name)
    
    return g, bst

class CampusNavigator:
    
    def __init__(self):
        self.graph, self.bst = create_campus_graph()
    
    def get_locations(self) -> List[str]:
        
        return sorted(self.graph.nodes())
    
    def find_shortest_path(self, start: str, destination: str) -> Tuple[bool, str, float]:
       
        if start not in self.graph.adj or destination not in self.graph.adj:
            return False, "Invalid start or destination location", 0.0
        
        distance, path = self.graph.dijkstra(start, destination)
        
        if not path:
            return False, "No path found between locations", 0.0
        
        path_str = " -> ".join(path)
        result = f"Shortest path {start} -> {destination}: {path_str} (distance={distance})"
        return True, result, distance
    
    def bfs_traversal(self, start: str, destination: str = None) -> Tuple[bool, str]:
       
        if start not in self.graph.adj:
            return False, "Invalid start location"
        
        order, parent = self.graph.bfs(start)
        result = f"BFS order: {' -> '.join(order)}"
        
        if destination and destination in parent:
            path = []
            cur = destination
            while cur is not None:
                path.append(cur)
                cur = parent[cur]
            path.reverse()
            result += f"\nBFS path {start} -> {destination}: {' -> '.join(path)} (unweighted hops)"
        elif destination:
            result += f"\nDestination '{destination}' not reachable from '{start}'"
        
        return True, result
    
    def dfs_traversal(self, start: str) -> Tuple[bool, str]:
        
        if start not in self.graph.adj:
            return False, "Invalid start location"
        
        order = self.graph.dfs(start)
        result = f"DFS order: {' -> '.join(order)}"
        return True, result
    
    def get_minimum_spanning_tree(self) -> Tuple[bool, str]:
       
        try:
            total, mst = self.graph.kruskal_mst()
            result = f"MST total weight: {total}\n"
            for u, v, w in mst:
                result += f"{u} -- {v} (w={w})\n"
            return True, result.strip()
        except Exception as e:
            return False, str(e)
    
    def search_location(self, location: str) -> bool:
        
        return self.bst.search(location)
    
    def get_sorted_locations(self) -> List[str]:
        
        return self.bst.inorder()


def print_menu():
    
    print("\n=== Campus Navigator ===")
    print("1) List locations")
    print("2) Shortest path (Dijkstra)")
    print("3) BFS traversal (and optional path to destination)")
    print("4) DFS traversal")
    print("5) Minimum Spanning Tree (Kruskal)")
    print("6) Search location (BST)")
    print("7) Show all locations sorted (BST inorder)")
    print("0) Exit")

def run_console_demo():
   
    navigator = CampusNavigator()
    
    print("DEMO MODE: automatic runs for screenshots.\n")
    print("1) Locations:", ", ".join(navigator.get_locations()))

    print("\n2) Dijkstra: shortest path Cafeteria -> Auditorium")
    success, result, _ = navigator.find_shortest_path("Cafeteria", "Auditorium")
    print(f"   {result}")

    print("\n3) BFS from Cafeteria:")
    success, result = navigator.bfs_traversal("Cafeteria")
    print(f"   {result}")

    print("\n4) DFS from Cafeteria:")
    success, result = navigator.dfs_traversal("Cafeteria")
    print(f"   {result}")

    print("\n5) Kruskal MST:")
    success, result = navigator.get_minimum_spanning_tree()
    print("   " + result.replace('\n', '\n   '))

    print("\n6) BST inorder (sorted locations):")
    print("   ", navigator.get_sorted_locations())

def run_console_interactive():
    
    navigator = CampusNavigator()
    
    print("Tip: Use exact location names from the list.")
    while True:
        print_menu()
        choice = input("Choose: ").strip()
        if choice == "0":
            print("Goodbye.")
            break
        elif choice == "1":
            print("Locations:", ", ".join(navigator.get_locations()))
        elif choice == "2":
            start = input("Start location: ").strip()
            dest = input("Destination location: ").strip()
            success, result, _ = navigator.find_shortest_path(start, dest)
            print(result)
        elif choice == "3":
            start = input("Start location: ").strip()
            dest = input("Destination (press Enter to skip): ").strip()
            dest = dest if dest else None
            success, result = navigator.bfs_traversal(start, dest)
            print(result)
        elif choice == "4":
            start = input("Start location: ").strip()
            success, result = navigator.dfs_traversal(start)
            print(result)
        elif choice == "5":
            success, result = navigator.get_minimum_spanning_tree()
            print(result)
        elif choice == "6":
            location = input("Location name to search: ").strip()
            found = navigator.search_location(location)
            print("Found." if found else "Not found.")
        elif choice == "7":
            print("Sorted locations:", ", ".join(navigator.get_sorted_locations()))
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--demo", action="store_true", help="Run demo output (non-interactive)")
    args = parser.parse_args()

    if args.demo:
        run_console_demo()
    else:
        run_console_interactive()