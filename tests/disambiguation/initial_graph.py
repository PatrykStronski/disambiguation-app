import sys
sys.path.append('../src/disambiguation/')
from InitialGraphClass import InitialGraph

def test_should_restart():
    init_graph = InitialGraph(None, 0, 0, 0, None)
    ret = init_graph.should_restart()
    assert ret == True or ret == False

def test_extract_strong_relations():
    init_graph = InitialGraph(None, 0, 5, 0, None)
    init_graph.node_visit_counts = [
        { "node1": "n1", "node2": "n2", "relation": "::owl:SameAs", "count": 3 },
        { "node1": "n2", "node2": "n3", "relation": "::owl:SameAs", "count": 6 },
        { "node1": "n5", "node2": "n4", "relation": "::owl:SameAs", "count": 5 },
        { "node1": "n6", "node2": "n7", "relation": "::owl:SameAs", "count": 10 },
        { "node1": "n18", "node2": "n7", "relation": "::owl:SameAs", "count": 4 },
    ]
    ret = init_graph.extract_strong_relations()
    assert len(ret) == 3
    assert { "node1": "n2", "node2": "n3", "relation": "::owl:SameAs" } in ret
    assert { "node1": "n5", "node2": "n4", "relation": "::owl:SameAs" } in ret
    assert { "node1": "n6", "node2": "n7", "relation": "::owl:SameAs" } in ret
