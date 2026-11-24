from dataclasses import dataclass

@dataclass(frozen=True)
class Usuario:
    id: int
    nome: str
    email: str
    senha_hash: str
    papel: str = 'cliente'

    def publico(self):
        return {'id': self.id, 'nome': self.nome, 'email': self.email, 'papel': self.papel}