from datetime import datetime, timedelta

def log(message, error=False):
    ''' Outputs time and message to console and log '''
    # format the message
    now = get_nz_time()
    timestamp = f'[{now.hour+1}:{now.minute}] [{now.day}/{now.month}/{now.year}]'
    line = f'{timestamp} {message}'

    # console and log
    print(line)
    with open('logs.txt', 'a') as handle:
        handle.write(line + '\n')
    
    # stop the program?
    if error:
        exit(-1)

def get_code_from_id(fund_id, companies):
    ''' Returns correct NZX code for company '''
    for company in companies:
        if company['id'] == fund_id:
            return company['code'] + '.NZ'
    
    return fund_id

def get_nz_time():
    ''' Returns NZ datetime object '''
    return datetime.utcnow() + timedelta(hours=12)
