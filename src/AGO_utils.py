""" AGO pipeline utils """

__author__    = "Cedric Chauve"
__email__     = "cedric.chauve@sfu.ca"
__version__   = "0.99"
__status__    = "Development"

import xml.etree.ElementTree as ET
import ete3

# Auxiliary functions: I/O -------------------------------------------------------------

''' Read the last line of a file '''
def get_last_line_file(file_path, msg="missing"):
    '''
    output: (str) last line of file or msg if empty file
    '''
    with open(file_path, 'r') as f:
        lines = f.readlines()
        if len(lines) == 0: return(f'{file_path} {msg}')
        else: return(lines[-1].rstrip())

# Newick tree ---------------------------------------------------------------

''' Creates a map from node names to list of descendant extant species '''
def newick_get_leaves(tree_file):
    '''
    input: paths to a Newick tree file with internal nodes named
    output:
    - dictionary dict(str->list(str)) indexed by names of nodes in tree_file
      each list is sorted in alphabetical order
    '''
    tree = ete3.Tree(tree_file, format=1)
    leaves = defaultdict(list)
    for node in tree.traverse():
        for leaf in node:
            leaves[node.name].append(leaf.name)
        leaves[node.name].sort()
    return(leaves)

''' Creates a map from node names to children '''
def newick_get_children(tree_file):
    '''
    input: paths to a Newick tree file with internal nodes named
    output:
    - dictionary dict(str->list(str)) indexed by names of nodes in tree_file
    '''
    tree = ete3.Tree(tree_file, format=1)
    children = defaultdict(list)
    for node in tree.traverse():
        if not node.is_leaf():
            children[node.name] = [ch.name for ch in node.children]
    return(children)

# RecPhyloXML ----------------------------------------------------------------

# Statistics dictionary keys
STATS_genes = 'genes' # Number of genes
STATS_dup = 'duplications' # Number of duplications
STATS_loss = 'losses' # Number of losses
# XML tags to corresponding statistics keys
STATS_xmlkeys = {'leaf': STATS_genes, 'speciation': STATS_genes, 'duplication': STATS_dup, 'loss': STATS_loss}
STATS_keys = [STATS_genes, STATS_dup, STATS_loss]

def recPhyloXML_read_events(in_file):
    ''' 
    Read a recPhyloXML file and returns a dictionary indexed by species
    and for each containing a dictionary recording number of genes, of duplications
    and of losses with the keys STATS_genes, STATS_dup, STATS_loss
    '''

    def get_tag(node):
        ''' Returns the tag of a node without its prefix {...} '''
        return(node.tag.rpartition('}')[2])
    def get_prefix(node):
        ''' Returns the prefix of tag '''
        pref = node.tag.rpartition("}")[0]
        if len(pref)>0: return(pref+'}')
        else: return(pref)
    def get_text(node):
        ''' Returns the text associated to a node '''
        if node.text is not None: return((node.text).strip())
        else: return('')
    def get_name(node):
        ''' Returns the name of a clade node; assumption: any clade node has a name '''
        return(get_text(node.find(f'{tag_pref}name')))
    def get_species(node):
        ''' Returns the species of a eventRec node '''
        return(node.get(f'speciesLocation'))
        
    def parse_spTree(root):
        ''' 
        input: XML root node
        output: dict(species name(str) -> species name of sibling species (str/None))
        '''
        def parse_clade_recursive(node, siblings):
            ''' Assumption: node is tagged <clade> '''
            children = node.findall(f'{tag_pref}clade')
            # Updating siblings dictionary
            if len(children) == 2:
                siblings[get_name(children[0])] = get_name(children[1])
                siblings[get_name(children[1])] = get_name(children[0])
            # Recursive calls
            for child in children:
                parse_clade_recursive(child, siblings)
        siblings = {get_name(root): None}
        parse_clade_recursive(root, siblings)
        return(siblings)

    def parse_recGeneTree(root, siblings):
        ''' 
        input: XML root node
        output: dict(species name(str) -> dict(STATS_genes: int, STATS_dup: int, STATS_loss: int))
        '''
        def parse_clade_recursive(node, stats):
            # Reconciliation event (possibly more than one)
            events = node.find(f'{tag_pref}eventsRec')
            # If more than one, then speciationLoss ended by last event
            # Loop on speciationLoss events to add a loss to the sibling species
            for event in events[1:][::-1]:
                stats[siblings[get_species(event)]][STATS_loss] += 1
            # Last event
            last_event_tag,last_event_species = get_tag(events[-1]),get_species(events[-1])
            stats[last_event_species][STATS_xmlkeys[last_event_tag]] += 1
            # Recursive calls
            for child in node.findall(f'{tag_pref}clade'):
                parse_clade_recursive(child, stats)
        stats = {sp:{STATS_genes: 0, STATS_dup: 0, STATS_loss: 0} for sp in siblings.keys()}
        parse_clade_recursive(root, stats)
        return(stats)

    root = ET.parse(in_file).getroot()
    tag_pref = get_prefix(root)
    siblings = parse_spTree(
        root.find(f'{tag_pref}spTree').find(f'{tag_pref}phylogeny').find(f'{tag_pref}clade')
    )
    recStats = parse_recGeneTree(
        root.find(f'{tag_pref}recGeneTree').find(f'{tag_pref}phylogeny').find(f'{tag_pref}clade'),
        siblings
    )
    return(recStats)

''' 
Correct a (Generax) recPhyloXML file that does not follow the expected format
- label internal nodes <start_id>, <start_id+1>, ... in order of appareance 
- reformat reconciliation events <event .../> -> <event ...></event>
Returns the first unused ID (int)
'''
def recPhyloXML_format(in_file, out_file, start_id=0):
    ''' Should be done using the XML libray '''
    with open(in_file, 'r') as in_xml, \
         open(out_file, 'w') as out_xml:
        out_xml.write('<recPhylo>\n')
        current_id = start_id
        for line in in_xml.readlines()[1:]:
            line1 = line.strip()
            if line1[0]!='<': continue
            if line1 == '<name></name>':
                out_xml.write(line.replace('><', f'>{current_id}<'))
                current_id += 1
            elif line1.startswith('<speciation'):
                out_xml.write(line.replace('/>', '></speciation>'))
            elif line1.startswith('<leaf'):
                out_xml.write(line.replace('/>', '></leaf>'))
            elif line1.startswith('<duplication'):
                out_xml.write(line.replace('/>', '></duplication>'))
            elif line1.startswith('<loss'):
                out_xml.write(line.replace('/>', '></loss>'))
            elif line1.startswith('<speciationLoss'):
                out_xml.write(line.replace('/>', '></speciationLoss>'))
            else:
                out_xml.write(line)
    return(current_id)

