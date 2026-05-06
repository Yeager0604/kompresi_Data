# A Huffman Tree Node
class Node:
    def __init__(self, prob, symbol, left=None, right=None):
        # Probabilitas
        self.prob = prob

        # simbol
        self.symbol = symbol

        # node kiri
        self.left = left

        # node kanan
        self.right = right

        # tree direction (0/1)
        self.code = ''



""" Fungsi pembantu untuk mencetak kode simbol dengan melakukan proses Huffman Tree"""
codes = dict()

def Calculate_Codes(node, val=''):
    # huffman untuk kode terkini
    newVal = val + str(node.code)

    if(node.left):
        Calculate_Codes(node.left, newVal)
    if(node.right):
        Calculate_Codes(node.right, newVal)

    if(not node.left and not node.right):
        codes[node.symbol] = newVal
         
    return codes        

""" Fungsi pembantu untuk mencetak kode simbol dengan melakukan proses Huffman Tree"""
def Calculate_Probability(data):
    symbols = dict()
    for element in data:
        if symbols.get(element) == None:
            symbols[element] = 1
        else: 
            symbols[element] += 1     
    return symbols

""" Fungsi pembantu untuk mendapatkan encoded"""
def Output_Encoded(data, coding):
    encoding_output = []
    for c in data:
      #  print(coding[c], end = '')
        encoding_output.append(coding[c])
        
    string = ''.join([str(item) for item in encoding_output])    
    return string
        
""" Fungsi pembantu untuk menghitung perbedaan ruang antara data terkompresi dan tidak terkompresi"""    
def Total_Gain(data, coding):
    before_compression = len(data) * 8 # total bit yang disimpan pada data sebelum di kompresi
    after_compression = 0
    symbols = coding.keys()
    for symbol in symbols:
        count = data.count(symbol)
        after_compression += count * len(coding[symbol]) #menghitung sebarapa banyak bit yang di butuhkan oleh simbol secara total 
    print("Space usage before compression (in bits):", before_compression)    
    print("Space usage after compression (in bits):",  after_compression) 


""" Fungsi pembantu untuk menghitung perbedaan ruang antara data terkompresi dan tidak terkompresi"""    
def Total_Gain(data, coding):
    before_compression = len(data) * 8 # total bit sebelum di kompresi
    after_compression = 0
    symbols = coding.keys()
    for symbol in symbols:
        count = data.count(symbol)
        after_compression += count * len(coding[symbol]) #menghitung berapa banyak bit yang dibutuhkan
    print("Space usage before compression (in bits):", before_compression)    
    print("Space usage after compression (in bits):",  after_compression)           



def Huffman_Encoding(data):
    symbol_with_probs = Calculate_Probability(data)
    symbols = symbol_with_probs.keys()
    probabilities = symbol_with_probs.values()
    print("symbols: ", symbols)
    print("probabilities: ", probabilities)
    
    nodes = []
    
    # mengubah symbol dan probabilitis kedalam huffman tree nodes 
    for symbol in symbols:
        nodes.append(Node(symbol_with_probs.get(symbol), symbol))
    
    while len(nodes) > 1:
        # mengurutkan semua nodes secara ascending berdasarkan probabilitasnya 
        nodes = sorted(nodes, key=lambda x: x.prob)
        # for node in nodes:  
        #      print(node.symbol, node.prob)
    
        # pick 2 smallest nodes
        right = nodes[0]
        left = nodes[1]
    
        left.code = 0
        right.code = 1
    
        # kombinasikan dua terkecil nodes untuk membuat node baru 
        newNode = Node(left.prob+right.prob, left.symbol+right.symbol, left, right)
    
        nodes.remove(left)
        nodes.remove(right)
        nodes.append(newNode)
            
    huffman_encoding = Calculate_Codes(nodes[0])
    print("symbols with codes", huffman_encoding)
    Total_Gain(data, huffman_encoding)
    encoded_output = Output_Encoded(data,huffman_encoding)
    return encoded_output, nodes[0]  
    
 
def Huffman_Decoding(encoded_data, huffman_tree):
    tree_head = huffman_tree
    decoded_output = []
    for x in encoded_data:
        if x == '1':
            huffman_tree = huffman_tree.right   
        elif x == '0':
            huffman_tree = huffman_tree.left
        try:
            if huffman_tree.left.symbol == None and huffman_tree.right.symbol == None:
                pass
        except AttributeError:
            decoded_output.append(huffman_tree.symbol)
            huffman_tree = tree_head
        
    string = ''.join([str(item) for item in decoded_output])
    return string        


""" Percobaan Pertama """
data = "AAAAAAABCCCCCCDDEEEEE"
print(data)
encoding, tree = Huffman_Encoding(data)
print("Encoded output", encoding)
print("Decoded Output", Huffman_Decoding(encoding,tree))

