from flask import Flask
from flask_login import LoginManager
from Router.router_oculos import oculos_bp
from Router.router_vendas import venda_bp
from Router.router_auth import auth_bp
from Models.Usuario import Usuario

app = Flask(__name__)

# Configuração da chave secreta para sessões
app.config['SECRET_KEY'] = 'sua-chave-secreta-super-segura-aqui-mude-em-producao'

# Configuração do Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login_view'
login_manager.login_message = 'Por favor, faça login para acessar esta página.'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    """Carrega o usuário a partir do ID armazenado na sessão"""
    # O ID está no formato "user:123" ou "adm:456"
    if ':' not in user_id:
        return None
    
    tipo, id_num = user_id.split(':', 1)
    is_adm = (tipo == 'adm')
    
    usuario_dict = Usuario.buscar_por_id(int(id_num), is_adm=is_adm)
    
    if usuario_dict:
        return Usuario.criar_usuario_objeto(usuario_dict, is_adm=is_adm)
    
    return None

# Registro dos blueprints
app.register_blueprint(oculos_bp)
app.register_blueprint(venda_bp)
app.register_blueprint(auth_bp)

if __name__ == '__main__':
    app.run(debug=True)
