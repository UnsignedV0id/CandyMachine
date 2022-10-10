package Systemc19_classes;

public class Usuario {
    
    private int id;
    private String usuario, senha;
    private boolean tagAdm;
    
  	// ADM 
	// -CADASTRA DEMAIS ATENDENTES
	// -CADASTRA PESSOAS (tmb classe) A SEREM VACINADAS
	// -REMOVE USUARIOS DA DB
	// -GERA RELATORIOS DE VACINAÇÃO


	// ATENDENTE
	// -VISUALIZA FILA DE VACINA NA ORDEM DESCRITA P PROJETO

    public Usuario(int id, String usuario, String senha, boolean tagAdm) {
        this.id = id;
        this.usuario = usuario;
        this.senha = senha;
        this.tagAdm = tagAdm;
    }

    public String getUsuario() {
        return usuario;
    }

    public boolean isTagAdm() {
        return tagAdm;
    }
    

    
}
