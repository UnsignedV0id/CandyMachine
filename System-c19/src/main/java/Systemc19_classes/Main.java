package Systemc19_classes;

import Systemc19_telas.TelaLogin;

public class Main {
               
        public static void main(String args[]){ 
         
            java.awt.EventQueue.invokeLater(new Runnable(){
                public void run(){
                   new TelaLogin().setVisible(true);
                }

        });

    }
    
}
