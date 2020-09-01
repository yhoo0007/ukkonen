import sys
import inspect


def get_edges(node, edges):
    '''
    Returns a list of edges of the given tree.
    '''
    for edge in filter(lambda e: e is not None, node.edges):
        edges.append(
            (node, edge, edge.start, edge.end.n) \
                if hasattr(edge.end, 'n') else \
                    (node, edge, edge.start, edge.end)
        )
        get_edges(edge, edges)
    return edges


def get_suffix_links(node, links, include_leaf_links=False):
    '''
    Returns a list suffix links of the given tree.
    '''
    edges = list(filter(lambda e: e is not None, node.edges))
    if node.link and (len(edges) > 0 or include_leaf_links):
        links.append((node, node.link))
    for edge in edges:
        get_suffix_links(edge, links)
    return links


def draw_tree(root, string, title='Suffix Tree'):
    '''
    Draws the tree using networkx and matplotlib.
    '''
    import matplotlib.pyplot as plt
    import networkx as nx

    plt.figure(title)
    g = nx.Graph()

    # draw nodes and edges
    edges = get_edges(root, [])
    g.add_edges_from(
        [(src, dst) for src, dst, _, _ in edges]
    )
    
    pos = nx.spring_layout(g, k=0.1)
    nx.draw(g, pos, with_labels=True)

    nx.draw_networkx_edge_labels(
        g,
        pos,
        edge_labels={
            (src, dst): f'{start},{end} {string[start:end+1]}'
        for src, dst, start, end in edges})

    # draw suffix links
    suffix_links = get_suffix_links(root, [])
    ax = plt.gca()
    for suffix_link in suffix_links:
        ax.annotate(
            '',
            xy=pos[suffix_link[1]],
            xycoords='data',
            xytext=pos[suffix_link[0]],
            textcoords='data',
            arrowprops=dict(
                arrowstyle='->',
                color='r',
                shrinkA=9,
                shrinkB=9,
                patchA=None,
                patchB=None,
                connectionstyle='arc3,rad=-0.3'
            )
        )
    plt.show()


def get_size(obj, seen=None):
    '''
    Returns the size of an object in bytes.
    Source: https://github.com/bosswissam/pysize/blob/master/pysize.py
    '''
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    # Important mark as seen *before* entering recursion to gracefully handle
    # self-referential objects
    seen.add(obj_id)
    if hasattr(obj, '__dict__'):
        for cls in obj.__class__.__mro__:
            if '__dict__' in cls.__dict__:
                d = cls.__dict__['__dict__']
                if inspect.isgetsetdescriptor(d) or inspect.ismemberdescriptor(d):
                    size += get_size(obj.__dict__, seen)
                break
    if isinstance(obj, dict):
        size += sum((get_size(v, seen) for v in obj.values()))
        size += sum((get_size(k, seen) for k in obj.keys()))
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
        size += sum((get_size(i, seen) for i in obj))
        
    if hasattr(obj, '__slots__'): # can have __slots__ with __dict__
        size += sum(get_size(getattr(obj, s), seen) for s in obj.__slots__ if hasattr(obj, s))

    return size


def read_file(fp):
    '''
    Reads a file and returns its content as a string.
    '''
    lines = []
    with open(fp) as file:
        for line in file:
            lines.append(line)
    return ''.join(lines)
