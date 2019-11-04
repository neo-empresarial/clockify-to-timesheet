import requests
import pandas
import datetime
from datetime import date
import pprint
import os

# Set global variables from .env file
V1_API_URL = "https://api.clockify.me/api/v1"
WORKSPACE_ID = os.getenv("CLOCKIFY_WORKSPACE_ID")
HEADERS = {"X-Api-Key": os.getenv("CLOCKIFY_API_KEY")}

def responses_of_url():
    '''Initial responses of url  '''
    url = "{}/workspace/{}/users".format(V1_API_URL, WORKSPACE_ID)
    responses = requests.get(url, headers=HEADERS).json()
    return responses

def gets_time_sunday():
    ''' Get the last week range ''' 
    today = datetime.date.today()
    monday = today - datetime.timedelta(days=today.weekday(), weeks=1)
    sunday = monday + datetime.timedelta(days=6)
    sunday = sunday.strftime("%Y-%m-%dT23:59:59Z")
    return sunday

def gets_time_monday():
    ''' Get the last week range ''' 
    today = datetime.date.today()
    monday = today - datetime.timedelta(days=today.weekday(), weeks=1)
    monday = monday.strftime("%Y-%m-%dT01:00:00Z")
    return monday

def taking_all_url_members(responses,sunday,monday):
    ''' Takes the url of each member by id's '''
    users = {}
    for response in responses_of_url():
        users[response['id']] = response['name']
    for user_id in users.keys():
        url_timeentry = "{}/workspaces/{}/user/{}/time-entries?start={}&end={}&hydrated={}".format(V1_API_URL, WORKSPACE_ID, user_id ,monday,sunday,True)
        print(url_timeentry)
        timeentries_member = requests.get(url_timeentry, headers=HEADERS).json()
    return timeentries_member

def feeding_data_frame_with_timeentry(timeentries_member):
    '''Takes the time entries and create dictionarys to input in the data frame'''  
    dados_frame = pandas.DataFrame(columns = ['project_name','client_name','task_name','user_name','description','duration'])
    dic_entry = {}
    for time_entry in taking_all_url_members(timeentries_member):
        try:
            client_name = time_entry['tags'][0]['name']
        except IndexError:
            continue
        end = time_entry['timeInterval']['end']
        end = datetime.datetime.strptime(end, '%Y-%m-%dT%H:%M:%SZ')
        start = time_entry['timeInterval']['start']
        start = datetime.datetime.strptime(start, '%Y-%m-%dT%H:%M:%SZ')            
        duration = ((end-start).total_seconds())/3600
        dic_entry['project_name'] = time_entry['project']['name']
        dic_entry['client_name'] = client_name
        dic_entry['task_name'] = time_entry['task']['name']
        dic_entry['user_name'] = users[time_entry['userId']]
        dic_entry['description'] = time_entry['description']
        dic_entry['duration'] = duration
        dados_frame = dados_frame.append(dic_entry , ignore_index=True)

        print(dados_frame)


def Organize_Data_Frame_create_excel (dados_frame):
    '''' Organize D.Frame and create a Excel'''
                
    dados_frame['Horas-aulas'] = dados_frame['duration']*1.2
    dados_frame.loc[dados_frame['project_name'] == 'Feriado',['client_name','task_name']] = 'Feriado'
    dados_frame.loc[dados_frame['project_name'] == 'Falta Justificada',['client_name', 'task_name']] = 'Falta Justificada'
    dados_frame_2 = pandas.DataFrame(columns = ['project_name','client_name','task_name','user_name','description','duration','Horas-aula'])
    dados_frame_2 = dados_frame.loc[dados_frame['task_name'] == 'Outros -> comente!',['user_name','project_name','task_name','client_name','Horas-aula','description']].copy()
    dados_frame_2 = dados_frame_2.groupby(['user_name','project_name','client_name','task_name','Horas-aula','description'],as_index=False).sum()
    dados_frame.drop(dados_frame[dados_frame['task_name'] == 'Outros -> comente!'].index, axis=0,inplace=True)
    del dados_frame ['duration']
    dados_frame = dados_frame.groupby(['user_name','project_name','client_name','task_name'], as_index=False).sum()
    dados_frame['description'] = ''
    dados_frame.loc[dados_frame['task_name'] == 'Feriado', ['task_name']] = ''
    dados_frame.loc[dados_frame['task_name'] == 'Falta Justificada', ['task_name']] = ''
    timesheet_df = pandas.concat([dados_frame[['user_name','project_name','task_name','client_name','Horas-aulas','description']], dados_frame_2])
    timesheet_df.sort_values(by = ['user_name','project_name'], inplace=True)
    timesheet_df.to_excel('NewTimesheet.xlsx', sheet_name = 'Timesheet',index = False, float_format = "%.2f")

    print("DONE!")

    return dados_frame and timesheet_df


def taking_timesheet_data():
    ''' Reading Timesheet and changing for a D.Frame'''
    Time_sheet_2019 = pandas.read_excel (r'~/Documents/NEO/clockify-to-timesheet/NewTimesheet.xlsx')
    df = pandas.DataFrame(Time_sheet_2019, columns = ['user_name','project_name','task_name','client_name','Horas-aulas','description'])
    return df

def feeding_timesheet(df):    
    """Now Timesheet is geting ready"""
    if ((df.user_name == dados_frame.user_name).bool and (df.client_name == dados_frame.client_name).bool and (df.project_name == dados_frame.project_name).bool and (df.task_name == dados_frame.task_name).bool) :
        df['semana {} - {}'.format(monday,friday)] = dados_frame['Horas-aulas']
        dados_frame['eliminar'] = 'x'
        dados_frame.drop(dados_frame[dados_frame['eliminar'] == 'x'].index, axis = 0,inplace=True)
        df = pandas.concat([df, dados_frame])
    return (df, dados_frme) 

responses_of_url()
gets_time_monday()
gets_time_sunday()
taking_all_url_members(gets_time_monday,gets_time_sunday,responses_of_url)
feeding_data_frame_with_timeentry(taking_all_url_members)
Organize_Data_Frame_create_excel(feeding_data_frame_with_timeentry)
taking_timesheet_data()
feeding_data_frame_with_timeentry(taking_timesheet_data,Organize_Data_Frame_create_excel)

print("Esse é df:\n", feeding_timesheet())
print(" Esse é dados frame : \n ", )
