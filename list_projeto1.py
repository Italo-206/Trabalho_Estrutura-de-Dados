import sys

class Paciente:
    def __init__(self, nome, idade, prioridade):
        self.nome = nome
        self.idade = idade
        self.prioridade = prioridade   # 2 = Prioritário, 1 = Normal
        self.prev = None
        self.next = None
        
    def __str__(self):
        tipo = "(P)" if self.prioridade == 2 else "(N)"
        return f"{self.nome} {tipo}"

class ListaDuplamenteEncadeada:
    def __init__(self):
        self.head = None
        self.tail = None
    
    def medir_memoria(self):
        # Calcula o consumo de memória dos nós (simples, pode ser ampliado).
        total = 0
        atual = self.head
        while atual:
            total += sys.getsizeof(atual)
            total += sys.getsizeof(atual.nome)
            total += sys.getsizeof(atual.idade)
            total += sys.getsizeof(atual.prioridade)
            atual = atual.next
        return total
    
    def contar_prioritarios_normais(self):
        p = 0
        n = 0
        atual = self.head
        while atual:
            if atual.prioridade == 2:
                p += 1
            else:
                n += 1
            atual = atual.next
        return p, n

    def adicionar(self, nome, idade, prioridade):
        memoria_antes = self.medir_memoria()
        novo = Paciente(nome, idade, prioridade)
        # Inserir paciente prioritário
        if prioridade == 2:
            atual = self.head
            ultimo_prioritario = None
            while atual and atual.prioridade == 2:
                ultimo_prioritario = atual
                atual = atual.next
            if ultimo_prioritario is None:
                # Nenhum prioritário no início
                novo.next = self.head
                if self.head:
                    self.head.prev = novo
                self.head = novo
                if self.tail is None:
                    self.tail = novo
            else:
                # Inserir após o último prioritário
                novo.next = ultimo_prioritario.next
                novo.prev = ultimo_prioritario
                if ultimo_prioritario.next:
                    ultimo_prioritario.next.prev = novo
                else:
                    self.tail = novo
                ultimo_prioritario.next = novo
        else:
            # Paciente normal vai ao fim
            if self.tail is None:
                self.head = self.tail = novo
            else:
                self.tail.next = novo
                novo.prev = self.tail
                self.tail = novo
        memoria_depois = self.medir_memoria()
        print(f"[ADD] Memória antes: {memoria_antes} bytes, depois: {memoria_depois} bytes, diferença: {memoria_depois - memoria_antes} bytes.")

    def remover(self):
        memoria_antes = self.medir_memoria()
        if self.head is None:
            print("Fila vazia.")
            return
        # Alternância: se houver >=1 prioritário para cada 7 normais,
        # alternar prioridade e normal
        p, n = self.contar_prioritarios_normais()
        alternancia = p >= n / 7 if n != 0 else False   # evita divisão por zero
        
        # Contador para alternância (método simples: alternar em cada chamada)
        proximo = self.head
        if alternancia:
            # procurar primeiro paciente normal
            atual = self.head
            while atual and atual.prioridade == 2:
                atual = atual.next
            if atual:
                proximo = atual
        # Remove paciente
        if proximo.prev:
            proximo.prev.next = proximo.next
        else:
            self.head = proximo.next
        if proximo.next:
            proximo.next.prev = proximo.prev
        else:
            self.tail = proximo.prev
        print(f"[REMOVE] Paciente atendido: {proximo}")
        if self.head:
            print(f"Próximo da fila: {self.head}")
        else:
            print("Fila vazia após remoção.")
        memoria_depois = self.medir_memoria()
        print(f"[REMOVE] Memória antes: {memoria_antes} bytes, depois: {memoria_depois} bytes, diferença: {memoria_depois - memoria_antes} bytes.")

    def alterar(self, nome, novo_nome=None, nova_idade=None, nova_prioridade=None):
        memoria_antes = self.medir_memoria()
        atual = self.head
        while atual:
            if atual.nome == nome:
                if novo_nome: atual.nome = novo_nome
                if nova_idade: atual.idade = nova_idade
                if nova_prioridade: 
                    # Remover e adicionar novamente para garantir a ordem
                    # Passo 1: remover nó atual
                    if atual.prev:
                        atual.prev.next = atual.next
                    else:
                        self.head = atual.next
                    if atual.next:
                        atual.next.prev = atual.prev
                    else:
                        self.tail = atual.prev
                    # Passo 2: atualizar prioridade e reinserir
                    nome, idade = atual.nome, atual.idade
                    prioridade = nova_prioridade
                    self.adicionar(nome, idade, prioridade)
                    return  # como já reinseriu, não precisa seguir
                print(f"[EDIT] Paciente {nome} alterado.")
                memoria_depois = self.medir_memoria()
                print(f"[EDIT] Memória antes: {memoria_antes} bytes, depois: {memoria_depois} bytes, diferença: {memoria_depois-memoria_antes} bytes.")
                return
            atual = atual.next
        print(f"[EDIT] Paciente {nome} não encontrado.")

    def exibir(self, invertido=False):
        pacientes = []
        if not invertido:
            atual = self.head
            while atual:
                pacientes.append(str(atual))
                atual = atual.next
        else:
            atual = self.tail
            while atual:
                pacientes.append(str(atual))
                atual = atual.prev
        fila = " --> ".join(pacientes)
        print("Fila atual:")
        print(fila if fila else "[ Fila Vazia ]")
    
    def inicializar_10(self):
        # Alterna entre prioritários e normais
        nomes = [
            ("João", 44, 2),
            ("Maria", 30, 1),
            ("Carlos", 28, 1),
            ("Ana", 78, 2),
            ("Luciano", 56, 1),
            ("Sandra", 34, 2),
            ("Rafael", 42, 1),
            ("Lívia", 66, 2),
            ("Beto", 41, 1),
            ("Paula", 21, 2)
        ]
        for nome, idade, prioridade in nomes:
            self.adicionar(nome, idade, prioridade)

#                     INTERATIVO 

def main():
    print("SIMULAÇÃO DE FILA DE ATENDIMENTO MÉDICO")
    fila = ListaDuplamenteEncadeada()
    fila.inicializar_10()
    print("\nFila inicial carregada.")
    fila.exibir()
    while True:
        print("\nComandos disponíveis:")
        print("add NOME IDADE PRIORIDADE(P/N) | assist | edit NOME [NOVO_NOME] [NOVA_IDADE] [NOVA_PRIORIDADE(P/N)] | mostrar | invertida | sair")
        cmd = input("Digite comando: ").strip()
        partes = cmd.split()
        if len(partes) == 0: continue
        if partes[0] == 'add' and len(partes) == 4:
            nome = partes[1]
            idade = int(partes[2])
            prioridade = 2 if partes[3].upper().startswith("P") else 1
            fila.adicionar(nome, idade, prioridade)
            fila.exibir()
        elif partes[0] == 'assist':
            fila.remover()
            fila.exibir()
        elif partes[0] == 'edit' and len(partes) >= 2:
            nome = partes[1]
            novo_nome = None
            nova_idade = None
            nova_prioridade = None
            if len(partes) >= 3:
                novo_nome = partes[2] if partes[2] != '-' else None
            if len(partes) >= 4:
                nova_idade = int(partes[3]) if partes[3] != '-' else None
            if len(partes) >= 5:
                np = partes[4].upper()
                if np.startswith('P'):
                    nova_prioridade = 2
                elif np.startswith('N'):
                    nova_prioridade = 1
            fila.alterar(nome, novo_nome, nova_idade, nova_prioridade)
            fila.exibir()
        elif partes[0] == 'mostrar':
            fila.exibir()
        elif partes[0] == 'invertida':
            fila.exibir(invertido=True)
        elif partes[0] == 'sair':
            break
        else:
            print("Comando não reconhecido.")

if __name__ == "__main__":
    main()
