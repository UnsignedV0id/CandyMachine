
package Systemc19_classes;

public class Pessoa {
    
    private int id, idade, prio;
    private String nome, endereco, dataVac, dataVac2;
    private boolean  tagProf;

    public Pessoa(int id, int idade,int prio, String nome, String endereco, boolean tagProf) {
        this.id = id;
        this.nome = nome;
        this.prio = prio;
        this.endereco = endereco;
        this.tagProf = tagProf;
    }

    public Pessoa(int id, int idade, int prio, String nome, String endereco, String dataVac, String dataVac2, boolean tagProf) {
        this.id = id;
        this.idade = idade;
        this.prio = prio;
        this.nome = nome;
        this.endereco = endereco;
        this.dataVac = dataVac;
        this.dataVac2 = dataVac2;
        this.tagProf = tagProf;
    }
    
    public void setId(int id) {
        this.id = id;
    }

    public void setNome(String nome) {
        this.nome = nome;
    }

    public void setEndereco(String endereco) {
        this.endereco = endereco;
    }

    public void setTagProf(boolean tagProf) {
        this.tagProf = tagProf;
    }

    public int getId() {
        return id;
    }

    public String getNome() {
        return nome;
    }

    public String getEndereco() {
        return endereco;
    }

    public int getPrio() {
        return prio;
    }
    
    public boolean isTagProf() {
        return tagProf;
    }
    //geram strings para sere, exibida no combobox
    public String gerarAssinatura() {
        String assinatura = "Nome: " + this.nome + "| Idade: " + this.idade + ""
                            + "| Endereço: " + this.endereco ;
        if(this.tagProf) {assinatura += "| ProfSaude: \u2612 ";}
        else { assinatura += "| ProfSaude: \u2610 ";} 
        
        return assinatura;
    }

    public String gerarAssinaturaData() {
        String assinatura = "Nome: " + this.nome + "| Idade: " + this.idade + ""
                            + "| Endereço: " + this.endereco ;
        
        if(this.tagProf) {assinatura += "| ProfSaude: \u2612 ";}
        else { assinatura += "| ProfSaude: \u2610 ";}
        
        assinatura += "| Vacinado nos dias: >  " + this.dataVac + " | " + this.dataVac2;
        
        return assinatura;
    }
       
    
}
