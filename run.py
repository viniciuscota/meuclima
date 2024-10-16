from aplication import create_app, db  # Caminho atualizado
from aplication.models import User  # Caminho atualizado

app = create_app()

# Criando o banco de dados dentro do contexto da aplicação
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=False)
