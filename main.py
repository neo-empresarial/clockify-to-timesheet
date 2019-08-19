"""Script to transform clockify data in NEO's timesheet format"""
import pandas as pd

def main():
    """Control program flow"""
    clockify_df = pd.read_csv('clockify-report.csv')
    clockify_df['Horas-aulas'] = clockify_df['Duration (decimal)']*1.2

    clockify_df.loc[clockify_df['Project'] == 'Feriado', ['Tags', 'Task']] = 'Feriado'

    comments_df = clockify_df.loc[clockify_df['Task'] == 'Outros -> comente!',
                                  ['User', 'Project', 'Task', 'Tags',
                                   'Horas-aulas', 'Description']].copy()
    comments_df = comments_df.groupby(['User', 'Tags', 'Project', 'Task', 'Description'],
                                      as_index=False).sum()
    comments_df = comments_df[['User', 'Project', 'Task', 'Tags', 'Horas-aulas', 'Description']]
    clockify_df.drop(clockify_df[clockify_df['Task'] == 'Outros -> comente!'].index, axis=0,
                     inplace=True)

    grp = clockify_df.groupby(['User', 'Tags', 'Project', 'Task'], as_index=False).sum()
    grp['Description'] = ''
    grp.loc[grp['Tags'] == 'Feriado', ['Tags', 'Task']] = ''
    timesheet_df = pd.concat([grp[['User', 'Project', 'Task', 'Tags',
                                   'Horas-aulas', 'Description']], comments_df])
    timesheet_df.sort_values(by=['User', 'Project'], inplace=True)
    timesheet_df.to_csv('NewTimesheet.csv', index=False)
    timesheet_df.to_excel('NewTimesheet.xlsx', sheet_name='Timesheet',
                          index=False, float_format="%.2f")
    print("DONE!")

if __name__ == "__main__":
    main()
