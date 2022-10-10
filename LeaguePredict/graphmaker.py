import os
import pandas as pd
import numpy as np
import plotly.express as px

path = os.getcwd()
colors = ['#bdd59b', '#f7f6e5', '#081c1f', '#23575b' , '#14383c']

loltb = pd.read_csv(path + '\loltb.csv', sep= ';')
loltb = loltb.drop(columns=["Trend"])

#? limpeza
loltb['Win %'] = loltb['Win %'].str.rstrip('%').astype('float')
loltb['Role %'] = loltb['Role %'].str.rstrip('%').astype('float')
loltb['Pick %'] = loltb['Pick %'].str.rstrip('%').astype('float')
loltb['Ban %'] = loltb['Ban %'].str.rstrip('%').astype('float')
loltb.to_csv(r""+path+'/loltbtreated.csv')
#TODO: deve ter um jeito melhor de fazer isso, mas nao achei

#! TABELAS ADICIONAIS CRIADAS PARA FACILITAR GRAFICOS
#? cria tabela com counts de cada instancia de classe por role ex: quantos ADC usaram marksman, quantos usaram mage...
classRoleCount = loltb.loc[loltb["Role"] == 'MID'].value_counts("Class").rename_axis('Class').reset_index(name='Count').assign(Role='MID')
classRoleCount = pd.concat([classRoleCount,loltb.loc[loltb["Role"] == 'TOP'].value_counts("Class").rename_axis('Class').reset_index(name='Count').assign(Role='TOP')])
classRoleCount = pd.concat([classRoleCount,loltb.loc[loltb["Role"] == 'SUPPORT'].value_counts("Class").rename_axis('Class').reset_index(name='Count').assign(Role='SUPPORT')])
classRoleCount = pd.concat([classRoleCount,loltb.loc[loltb["Role"] == 'ADC'].value_counts("Class").rename_axis('Class').reset_index(name='Count').assign(Role='ADC')])
classRoleCount = pd.concat([classRoleCount,loltb.loc[loltb["Role"] == 'JUNGLE'].value_counts("Class").rename_axis('Class').reset_index(name='Count').assign(Role='JUNGLE')])

#? tabela com a media de WR por role
#TODO
#classWrMean 


#organizando em classe pra facilitar a renderização de cada grafico, evitando ficar comentando cada grafico quando nao esta em uso
class LeagueGraphs:

    def pieClasses():
        classes = loltb['Class'].value_counts().rename_axis('Classe').reset_index(name='count')
        fig = px.pie(classes, names='Classe',values='count') 
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_traces(marker=dict(colors=colors, line=dict(color='#000000',width= 1)))
        fig.show()
        del(classes)

    def pieRoles():
        roles = loltb['Role'].value_counts().rename_axis('Role').reset_index(name='count')
        fig = px.pie(roles, names='Role',values='count') 
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_traces(marker=dict(colors=colors, line=dict(color='#000000',width= 1)))
        fig.show()
        del(roles)
    
    def histRoleClasses():
        fig = px.histogram(classRoleCount,x='Class',y='Count',barmode='group', color="Role",text_auto=True,
        color_discrete_map={'TOP':colors[0], 'MID':colors[1], 'JUNGLE':colors[2], 'SUPPORT':colors[3], 'ADC':colors[4]})#["TOP", 'MID', 'JUNGLE', 'SUPPORT', 'ADC']
        fig.update_traces(marker_line_color='black', marker_line_width=1.5)
        fig.show()

    def histWrMeanRole(roleName):
        temp = loltb.loc[loltb['Role'] == roleName].groupby(['Class']).mean().reset_index()
        temp = temp.round(2)

        fig = px.histogram(temp,x='Class',y='Win %',text_auto=True,color_discrete_sequence=[colors[3]])
        fig.update_traces(marker_line_color='black', marker_line_width=1.5)
        fig.show()
       
        del(temp)
    
    def histWrMeanRolePick(roleName):
        temp = loltb.loc[loltb['Role'] == roleName].groupby(['Class']).mean().reset_index()
        temp = temp.round(2)
        
        fig = px.histogram(temp,x='Class',y='Pick %',text_auto=True,color='Pick %',
        color_discrete_map={temp['Pick %'][0]:colors[0],
        temp['Pick %'][1]:colors[1],
        temp['Pick %'][2]:colors[2],
        temp['Pick %'][3]:colors[3],
        temp['Pick %'][3]:colors[4]}) 
        #fix horrivel, nao tenho ideia como pegar automatico as porcentagens dinamicamente sem estourar o limite do array quando valor indisponivel
        #deixa essa funçao redundante, visto que toda vez que rolename for passado não existe como dinamicamentre colorir o grafico, melhor opção seria definir uma cor solida 
        # a todas barras /shrug
        fig.update_traces(marker_line_color='black', marker_line_width=1.5)
        fig.show()
        print(temp['Pick %'][0])
        del(temp)


LeagueGraphs.histWrMeanRolePick('ADC')


