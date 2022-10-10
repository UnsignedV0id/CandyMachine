/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package Systemc19_classes;

import java.sql.Date;
import java.text.SimpleDateFormat;
import java.util.Arrays;

public class GerenciadorDeData {
        
    public static double[] gerarRelatorio( String dataInicio, String dataFim)
    {
        //convert as strings para formato data
        SimpleDateFormat formatData = new SimpleDateFormat("dd-MM-yyyy");
        Date inicio = null;
        Date fim = null;
        try
        {
            java.util.Date javDatInico = formatData.parse(dataInicio);
            java.util.Date javDatFim = formatData.parse(dataFim);
            inicio = new java.sql.Date(javDatInico.getTime()) ;
            fim = new java.sql.Date(javDatFim.getTime())  ;
            
        } catch (Exception e) {
            e.printStackTrace();
        }
        
        //calcula dias passados       
        double diasPassados = ((fim.getTime() / (1000*60*60*24)) - (inicio.getTime() / (1000*60*60*24)));
        
        System.out.println("inter de dias: " + diasPassados);
        if(diasPassados < 0){return null;} else if (diasPassados == 0){diasPassados++;}// TODO MENSANGEM CASO ERRO DE USUARIO
        
        //obtem total de idades no intervalo da datas passadas
        //variaveis de idade correspondem com a ordem  I II III IV do pdf de descriçao do projeto
        int idades[] = DAO.contarIdades(inicio.toString(), fim.toString());
        
        //gera array medias para ser retornado
        //variaveis de idade correspondem com a ordem  I II III IV do pdf de descriçao do projeto
        double medias[] = {idades[0] / diasPassados, idades[1] / diasPassados, idades[2] / diasPassados , idades[3] / diasPassados};
        
        System.out.println(Arrays.toString(medias));
        
        return medias;
        
    }
       
    public static boolean checarSeNum(String str) {

    try {
        Double num = Double.parseDouble(str);
        return true;
    } catch (NumberFormatException e) {
        return false;
    }

    }  
    
}
