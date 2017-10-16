"""
quiz2!

Use path finding algorithm to find your way through dark dungeon!

Tecchnical detail wise, you will need to find path from node 7f3dc077574c013d98b2de8f735058b4
to f1f131f647621a4be7c71292e79613f9

TODO: implement BFS
TODO: implement Dijkstra utilizing the path with highest effect number
"""

import json
import codecs



# http lib import for Python 2 and 3: alternative 4
try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

GET_STATE_URL = "http://192.241.218.106:9000/getState"
STATE_TRANSITION_URL = "http://192.241.218.106:9000/state"

def get_state(room_id):
    """
    get the room by its id and its neighbor
    """
    body = {'id': room_id}
    return __json_request(GET_STATE_URL, body)

def transition_state(room_id, next_room_id):
    """
    transition from one room to another to see event detail from one room to
    the other.

    You will be able to get the weight of edge between two rooms using this method
    """
    body = {'id': room_id, 'action': next_room_id}
    return __json_request(STATE_TRANSITION_URL, body)

def __json_request(target_url, body):
    """
    private helper method to send JSON request and parse response JSON
    """
    req = Request(target_url)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    jsondata = json.dumps(body)
    jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
    req.add_header('Content-Length', len(jsondataasbytes))
    reader = codecs.getreader("utf-8")
    response = json.load(reader(urlopen(req, jsondataasbytes)))
    return response



# TODO: implement BFS
def bfs(initial_node, dest_node):

    q = [initial_node]
    # dictionary to store parents which was visited
    parents = {}
    # list to store nodes which was visited
    visited_node = [initial_node['id']]  
    # dictionary to store edge
    edges = {}
    # path to destination
    path = []

    while q:
        node = q.pop(0)
        for c in node['neighbors']:
            child = get_state(c['id'])
            edge = transition_state(node['id'], child['id'])

            if child['id'] not in visited_node:
                visited_node.append(child['id'])
                parents[child['id']] = node['id']
                edges[child['id']] = edge
                q.append(child)

            elif child['id'] == dest_node['id']:
                visited_node.append(child['id'])
                parents[child['id']] = node['id']
                edges[child['id']] = edge
                
                while dest_node['id'] in parents:
                    path.append(edges[dest_node['id']])
                    dest_node['id'] = parents[dest_node['id']]
                    path.reverse()

                print_path(path, initial_node['id'])
                
            
            


# TODO: implement Dijkstra utilizing the path with highest effect number
def dijkstra_search(initial_node, dest_node):

  
    q = []
    q.append((0, initial_node))
  
    # dictionary to store parents which was visited
    parents = {}
    # list to store nodes which was visited
    visited_node = []
    # distionary to store weight
    distance = {}
    distance[initial_node] = 0
    # dictionary to store edge
    edges = {}
    # path to destination
    path = []

    while q:
        node =get_state(q.pop()[1])
        visited_node.append(node['id'])

        # check all neighbors nodes
        for child in node['neighbors']:
            edge = transition_state(node['id'], child['id'])
            weight = distance[node['id']] + edge['event']['effect']
     
            if(child['id'] not in distance or weight > distance[child['id']]) and child['id'] not in visited_node:
                
                if child['id'] in distance:
                    q.remove((distance[child['id']], child['id']))
                
                distance[child['id']] = weight
                parents[child['id']] = node['id']
                edges[child['id']] = edge
                q.append((weight, child['id']))
        q = sorted(q, key=lambda x:x[0])

    
    while dest_node in parents:
        path.append(edges[dest_node])
        dest_node = parents[dest_node]
    path.reverse()

    print_path(path, initial_node)


# print path
def print_path(pathes, initial_node):
    previous_id = initial_node
    total = 0
    for path in pathes:
        previous_node = get_state(previous_id)
        next_id = path['id']
        total += path['event']['effect']

        print(previous_node['location']['name']+' (' + previous_id + ') : '+ path['action'] + ' ('+path['id']+') : '+ str(path['event']['effect']))
        previous_id = next_id
    print('Total hp : ' + str(total))


# main code
if __name__ == "__main__":
    # Your code starts here
    empty = '7f3dc077574c013d98b2de8f735058b4'
    dark =  'f1f131f647621a4be7c71292e79613f9'

    empty_room = get_state(empty)
    dark_room = get_state(dark)
   
   
    print('BFS Path:')
    bfs(empty_room,dark_room)
    print('\n')
    print('Dijkstra Path:')
    dijkstra_search(empty,dark)

    #print(empty_room)
    #print(transition_state(empty_room['id'], empty_room['neighbors'][0]['id']))
    
   



