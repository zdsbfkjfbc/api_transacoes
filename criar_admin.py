from src.infra.database import get_db, Base, engine

# Aqui usamos o impot direto da pasta infra
from src.infra.usuario_repository import UsuarioRepository
from src.infra.models import UsuarioDB
from src.utils.security import gerar_hash

# Garante que as tabelas do banco de dados existam
Base.metadata.create_all(bind=engine)

def criar_super_usuario():
    print("🚀 Iniciando criação de usuário Admin...")

    # 1. Abre conexao com o banco de dados
    db = next(get_db())
    repo = UsuarioRepository(db)

    # 2. Dados do Admin
    cpf_admin = "123456789"
    senha_plana = "admin"

    # 3. Verifica se já existe um usuário com o CPF do Admin    
    if repo.obter_cpf(cpf_admin):
        print ("⚠️ Usuário Admin já existe. Nenhuma ação foi tomada.")
        return
    
    # 4. A mágica do Hash(Criptografia)
    # Aqui na senha "minhasenhaforte" é convertida em uma senha criptografada
    senha_criptografada = gerar_hash(senha_plana)
    print(f"🔐 Senha '{senha_plana}' virou hash {senha_criptografada}")
    
    # 5. Salva no banco 
    novo_usuario = UsuarioDB(
        nome = "Admin",
        cpf = cpf_admin,
        senha_hash = senha_criptografada
    )
    repo.criar(novo_usuario)
    print("✅ Usuário Admin criado com sucesso!")

if __name__ == "__main__":
    criar_super_usuario()