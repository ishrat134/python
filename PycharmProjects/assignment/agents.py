import pandas as pd


def agentAvailibility(agentData, selection_mode, selection_role):
    agents = []
    df = pd.DataFrame(agentData)
    if selection_mode == "all_available":
        df1 = df[(df['is_available'] == "True")]
        i = 0
        df3 = pd.DataFrame()
        for roles in df1['Roles']:
            result = all(elem in roles for elem in selection_role)
            if result:
                df2 = df1.iloc[i]
                df3 = df3.append(df2, ignore_index=True)
            i = i + 1
        agents = df3.Name.tolist()
        return agents

    if selection_mode == "least busy":
        df1 = df[(df['is_available'] == "True")]
        i = 0
        df3 = pd.DataFrame()
        for roles in df1['Roles']:
            result = all(elem in roles for elem in selection_role)
            if result:
                df2 = df1.iloc[i]
                df3 = df3.append(df2, ignore_index=True)
            i = i + 1

        df4 = df3[df3.available_since == df3.available_since.max()]
        agents = df4.Name.tolist()
        return agents

    if selection_mode == "random":
        df1 = df[(df['is_available'] == "True")]
        i = 0
        df3 = pd.DataFrame()
        for roles in df1['Roles']:
            result = all(elem in roles for elem in selection_role)
            if result:
                df2 = df1.iloc[i]
                df3 = df3.append(df2, ignore_index=True)
            i = i + 1
        df4 = df3.sample()
        agents = df4.Name.tolist()
        return agents







