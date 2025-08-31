from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
import os

# Add the directory containing campus_navigator.py to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from campus_navigator_backend import CampusNavigator

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests
navigator = CampusNavigator()

@app.route('/api/shortest-path', methods=['POST'])
def shortest_path():
    data = request.json
    success, result, distance = navigator.find_shortest_path(
        data['start'], data['end']
    )
    
    if success:
        # Extract path from result string
        # "Shortest path A -> B: A -> C -> B (distance=X)"
        path_part = result.split(': ')[1].split(' (distance=')[0]
        path = path_part.split(' -> ')
        
        return jsonify({
            'success': True,
            'path': path,
            'distance': distance,
            'formatted': result
        })
    
    return jsonify({'success': False, 'error': result})

@app.route('/api/locations')
def get_locations():
    return jsonify(navigator.get_locations())

@app.route('/api/search/<location>')
def search_location(location):
    found = navigator.search_location(location)
    return jsonify({'found': found, 'query': location})

@app.route('/api/algorithm', methods=['POST'])
def run_algorithm():
    data = request.json
    algorithm = data['algorithm']
    start = data.get('start')
    destination = data.get('destination')  # For BFS path finding
    
    try:
        if algorithm == 'bfs':
            if destination and destination.strip():
                # BFS with destination - get both order and path
                success, result = navigator.bfs_traversal(start, destination)
            else:
                # BFS without destination - just traversal order
                success, result = navigator.bfs_traversal(start)
            
            return jsonify({
                'success': success, 
                'result': result, 
                'title': 'BFS Result'
            })
            
        elif algorithm == 'dfs':
            success, result = navigator.dfs_traversal(start)
            return jsonify({
                'success': success, 
                'result': result, 
                'title': 'DFS Result'
            })
            
        elif algorithm == 'mst':
            success, result = navigator.get_minimum_spanning_tree()
            return jsonify({
                'success': success, 
                'result': result, 
                'title': 'MST Result'
            })
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')