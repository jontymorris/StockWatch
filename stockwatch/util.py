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
        exit(error)

def get_code_from_id(fund_id, companies):
    ''' Returns correct NZX code for company '''
    for company in companies:
        if company['id'] == fund_id:
            return company['code'] + '.NZ'
    
    return fund_id

def get_nz_time():
    ''' Returns NZ datetime object '''
    return datetime.utcnow() + timedelta(hours=12)

def dividends_soon(dividends):
    ''' Check if dividends are coming up '''
    if dividends != '':
        for month in dividends.split(', '):
            if is_month_close(month.lower()):
                return True
                
    return False

def is_month_close(month):
    ''' Decide if the month is close to now '''
    month_number = datetime.strptime(month[:3], '%b').month
    current_month = get_nz_time().month
    
    if current_month >= (month_number - 1) and current_month <= (month_number + 1):
        return True

    return False
