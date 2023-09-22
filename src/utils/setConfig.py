def select_data_folder():
    inputString=input('please enter dataFolder all lower case with no spaces:')
    if inputString=='iphone6':
        return 'iPhone6config.csv'
    if inputString=='iphone15':
        return 'iPhone15Config.csv'