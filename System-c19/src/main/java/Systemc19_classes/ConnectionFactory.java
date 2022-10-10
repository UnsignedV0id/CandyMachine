package Systemc19_classes;

import java.sql.Connection;
import java.sql.DriverManager;
import javax.swing.JOptionPane;

public class ConnectionFactory {
    
    private static final String USUARIO = "root";
    private static final String SENHA = "1524";
    private static final String HOST = "localhost";
    private static final String PORT = "3306";
    private static final String DB = "systemc19_db";

    public static Connection getConnection() 
    {
        try
        {
            Connection c = DriverManager.getConnection("jdbc:mysql://" + HOST + ":" + PORT + "/" + 
            DB + "?useTimezone=true&serverTimezone=America/Sao_Paulo", USUARIO, SENHA );
            return c;
        }
        catch(Exception e )
        {
            e.printStackTrace();
            JOptionPane.showMessageDialog(null, "Erro de conexão ao DB");
            return null;
        }
    }    
}
