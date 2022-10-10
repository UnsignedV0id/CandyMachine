package Systemc19_classes;

import java.sql.Connection;
import java.sql.Date;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.text.SimpleDateFormat;
import java.time.LocalDateTime;
import java.util.ArrayList;
import javax.swing.JOptionPane;

//classe para obter dados da DB


public class DAO {
    
    public static Usuario checarUsuario(String usuario, String senha ) throws Exception{
        //cria comando sql
        String sql = "SELECT * FROM usuarios_tb  WHERE usuario = ? AND senha = ?";
        
        try
        {
            Connection conexao = ConnectionFactory.getConnection();
            PreparedStatement ps = conexao.prepareStatement(sql);
            ps.setString(1, usuario);
            ps.setString(2, senha);
            ResultSet rs = ps.executeQuery(); // procura pelo usuario e senha na db
            
            while (rs.next()){
                //caso rs.next nao for false,  retorna um novo Usuario que sera usado no resto da aplicação
                int id = rs.getInt("id");
                String tempUsuario = rs.getString("usuario");
                String tempSenha = rs.getString("senha");
                boolean tagAdm = rs.getBoolean("tagAdm");
                System.out.println("Usuario " + id + " Encontrado");
                return new Usuario(id, tempUsuario, tempSenha, tagAdm);                            
            }
        }
        catch(Exception e)
        {
            e.printStackTrace();
            System.out.println("Erro ao encontrar usuario no BD");
        }
        System.out.println("Erro ao encontrar usuario");
        return null;

    }
    
    public static void cadastrarUsuario(String usuario, String senha, boolean tagAdm){
        //definir comando sql que sera utilizado
        String sql ="INSERT INTO usuarios_tb (usuario, senha, tagAdm) VALUES(?,?,?)";
        
        ConnectionFactory conexao = new ConnectionFactory();
        try (Connection  c = conexao.getConnection())    {
            //pré-compilar o comando sql
            PreparedStatement ps = c.prepareStatement(sql);
            
            //Preenche os dados da query
            ps.setString(1, usuario);
            ps.setString(2, senha);
            ps.setBoolean(3, tagAdm);
            
            //Executa o comando
            ps.execute();
            System.out.println("Novo usuario cadastrado, adm: " + tagAdm );
            
        }
        catch(Exception e){
            System.out.println("Erro ao cadastrar novo us");
            e.printStackTrace();
        }
    }
    
    //metodos aualizarUsuario usam overload para caso caixa é adm for chechada
    public static void atualizarUsuario(int id ,String novoUsuario, String novaSenham, boolean tagAdm){
        
        String sql = "UPDATE usuarios_tb SET usuario = ?, senha = ?, tagAdm = ? WHERE id = ?" ;
        ConnectionFactory conexao = new ConnectionFactory();
        
        try (Connection  c = conexao.getConnection()){
            
            PreparedStatement ps = c.prepareStatement(sql);
            ps.setString(1, novoUsuario);
            ps.setString(2, novaSenham);
            ps.setBoolean(3,tagAdm);
            ps.setInt(4, id);
            ps.execute();
        }
        catch(Exception e){
            e.printStackTrace();
            JOptionPane.showMessageDialog(null, "ERRO att");
        }
    }
    
    public static void excluirUsuario(int id){
        String sql = "DELETE FROM usuarios_tb WHERE id = ?";
        ConnectionFactory conexao = new ConnectionFactory();
        try (Connection  c = conexao.getConnection()){
            
            PreparedStatement ps = c.prepareStatement(sql);
            ps.setInt(1,id);
            ps.execute();
        }
        catch (Exception e){
            e.printStackTrace();
            JOptionPane.showMessageDialog(null,"ERRO del");
        }
    }
    
    public static void cadastrarPessoa(String nome, int idade, boolean tagProf, String endereco, int prio){
        //definir comando sql que sera utilizado
        String sql ="INSERT INTO pessoas_tb (nome, idade, tagProf, endereco, prio) VALUES(?,?,?,?,?)";
        
        ConnectionFactory conexao = new ConnectionFactory();
        try (Connection  c = conexao.getConnection())    {
            //pré-compilar o comando sql
            PreparedStatement ps = c.prepareStatement(sql);
            
            //Preenche os dados da query
            ps.setString(1, nome);
            ps.setInt(2, idade);
            ps.setBoolean(3, tagProf);
            ps.setString(4, endereco);
            ps.setInt(5,prio);
            
            //Executa o comando
            ps.execute();
            System.out.println("Nova pessoa cadastrada, nome: " + nome );
            
        }
        catch(Exception e){
            System.out.println("Erro ao cadastrar novo us");
            e.printStackTrace();
        }
    }

    public static int[] contarIdades(String dataInicio, String dataFim) {
        // ordem de retorno das idades é a mesma descrita no exercico 
        int quantIdades[] = new int[4];
        
        System.out.println(dataInicio + " " + dataFim);
        
        ConnectionFactory conexao = new ConnectionFactory();
        
        try (Connection  c = conexao.getConnection())    {
            //pré-compilar o comando sql
            String sql ="SELECT\n" +
                "  SUM( idade >= 90 ) AS idadeA,\n" +
                "  SUM(idade < 90 AND idade >= 70) AS idadeB,\n" +
                "  SUM(idade < 70 AND idade >= 50) AS idadeC,\n" +
                "  SUM(idade < 50) AS idadeD  \n" +
                "FROM pessoas_tb WHERE dataVac between " +"'"+ dataInicio +"'" + " and " + "'"+dataFim+"'";
            
            PreparedStatement ps = c.prepareStatement(sql);
            //Executa o comando
            ResultSet rs = ps.executeQuery();
            //preenche medias para retorno
            while(rs.next())
            {
                quantIdades[0] = rs.getInt("idadeA");
                quantIdades[1] = rs.getInt("idadeB");
                quantIdades[2] = rs.getInt("idadeC");
                quantIdades[3] = rs.getInt("idadeD");
            }
            
        }
        catch(Exception e){
            System.out.println("erro ao obter quantidade de idades");
            e.printStackTrace();
        }
        return quantIdades;
    }
    
    public static ArrayList<Pessoa> gerarFila(boolean segundaDose)
    {
        String sql;
        //cria comando sql
        if(!segundaDose){ sql = "SELECT * FROM pessoas_tb WHERE prio > 0 AND prio < 5 ORDER BY prio DESC";}
        else {sql = "SELECT * FROM pessoas_tb WHERE prio <= 0 ORDER BY prio ASC";}
        
        try
        {
            Connection conexao = ConnectionFactory.getConnection();
            PreparedStatement ps = conexao.prepareStatement(sql);
            ResultSet rs = ps.executeQuery(); // lista pessoas na tb e retorna em ordem de prioridade
            ArrayList<Pessoa> filaPessoas = new ArrayList<Pessoa>();
            
            while (rs.next()){
                int id = rs.getInt("id");
                int idade = rs.getInt("idade");
                int prio = rs.getInt("prio");
                String nome = rs.getString("nome");
                String endereco = rs.getString("endereco");
                boolean isProf = rs.getBoolean("tagProf");
                
                Pessoa tempPessoa = new Pessoa(id, idade,prio , nome, endereco, isProf);
                filaPessoas.add(tempPessoa);
            }
            return filaPessoas;
            
        }
        catch(Exception e)
        {
            e.printStackTrace();
            System.out.println("Erro ao encontrar usuario no BD");
        }
        
        return null;
    }

    public static void vacinar(int id, int prio, boolean segundaDose) {
        
        String sql = "UPDATE pessoas_tb SET dataVac = ?, dataVac2 = ?, prio = ? WHERE id = ?" ;
        ConnectionFactory conexao = new ConnectionFactory();
        //inserindo data mas antes convertendo para o formato do sql
        
        LocalDateTime dateTimePrimeiraVac = LocalDateTime.now();
        LocalDateTime dataTimeSegundaVac = dateTimePrimeiraVac.plusDays(10);
        java.sql.Date dataSqlPrimeira = java.sql.Date.valueOf(dateTimePrimeiraVac.toLocalDate());
        java.sql.Date dataSqlSegunda = java.sql.Date.valueOf(dataTimeSegundaVac.toLocalDate());

        try (Connection  c = conexao.getConnection()){
            
            PreparedStatement ps = c.prepareStatement(sql);
            ps.setDate(1, dataSqlPrimeira);
            ps.setDate(2, dataSqlSegunda);
            if(!segundaDose){ps.setInt(3, (prio * -1));}
            else{ps.setInt(3, 100);}
            ps.setInt(4, id);
            ps.execute();
        }
        catch(Exception e){
            e.printStackTrace();
            JOptionPane.showMessageDialog(null, "ERRO ao inserir datas vacinas");
        }
       
    }

    public static ArrayList<Pessoa> gerarListaVacinados() {
        //cria comando sql
        String sql = "SELECT * FROM pessoas_tb WHERE prio = 100  ORDER BY YEAR(dataVac) ASC, MONTH(dataVac) ASC, DAY(dataVac) ASC;";
        
        try
        {
            Connection conexao = ConnectionFactory.getConnection();
            PreparedStatement ps = conexao.prepareStatement(sql);
            ResultSet rs = ps.executeQuery(); // lista pessoas na tb e retorna em ordem de prioridade
            ArrayList<Pessoa> tabelaVacinados = new ArrayList<Pessoa>();
            SimpleDateFormat formatData = new SimpleDateFormat("dd-MM-yyyy");
            
            while (rs.next()){
                int id = rs.getInt("id");
                int idade = rs.getInt("idade");
                int prio = rs.getInt("prio");
                String nome = rs.getString("nome");
                String endereco = rs.getString("endereco");
                boolean isProf = rs.getBoolean("tagProf");
                Date dataVacTemp = rs.getDate("dataVac");
                Date dataVac2Temp = rs.getDate("dataVac2");
                
                String dataVac = formatData.format(dataVacTemp) ;
                String dataVac2 = formatData.format(dataVac2Temp) ;
                
                Pessoa tempPessoa = new Pessoa(id, idade,prio , nome, endereco, dataVac, dataVac2, isProf);
                tabelaVacinados.add(tempPessoa);
            }
            return tabelaVacinados;
            
        }
        catch(Exception e)
        {
            e.printStackTrace();
            System.out.println("Erro ao encontrar usuario no BD");
        }
        
        return null;
    }

   
    

}

