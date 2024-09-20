class Block:
    def __init__(self, block_id, instructions, successors):
        self.block_id = block_id
        self.instructions = instructions
        self.successors = successors
        self.def_set = set()
        self.use_set = set()
        self.in_set = set()
        self.out_set = set()


    def calculate_def_use(self):
        assigned_vars = set()
        for instr in self.instructions:
            # Parse the left-hand side of an assignment
            var = instr.split('=')[0].strip()
            assigned_vars.add(var)
            # Use variables on the right-hand side
            for token in instr.split('=')[1].split():
                if token.isalpha() and token not in assigned_vars:
                    self.use_set.add(token)
            self.def_set.add(var)


def liveness_analysis(blocks):
    # Inicializa os conjuntos IN e OUT para todos os blocos
    for block in blocks:
        block.calculate_def_use()

    changed = True
    while changed:
        changed = False
        for block in blocks:
            # Calcula OUT[B] como a união de IN de seus sucessores
            new_out = set()
            for succ_id in block.successors:
                # Verifica se o sucessor existe na lista de blocos
                succ_block = next(
                    (b for b in blocks if b.block_id == succ_id), None)
                if succ_block:
                    new_out.update(succ_block.in_set)

            if new_out != block.out_set:
                block.out_set = new_out
                changed = True

            # Calcula IN[B] como UseB ∪ (OUT[B] - DefB)
            new_in = block.use_set.union(block.out_set - block.def_set)
            if new_in != block.in_set:
                block.in_set = new_in
                changed = True

    # Exibe os conjuntos IN e OUT para cada bloco
    for block in blocks:
        print(f"Block {block.block_id}")
        print(f"IN[{block.block_id}] = {block.in_set}")
        print(f"OUT[{block.block_id}] = {block.out_set}")
        print()


# Exemplo de uso
blocks = [
    Block(1, ['a = a + c', 'b = 4 - a'], [2]),
    Block(2, ['b = 20 * c'], [3]),
    # Sucessor 0 indica que não há sucessores
    Block(3, ['d = a + b', 'b = 0'], [0])
]

liveness_analysis(blocks)
