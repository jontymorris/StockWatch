from datetime import datetime, timedelta


def log(message, error=False):
    ''' Outputs time and message to console and log '''

    # format the message
    now = get_nz_time()
    date = f'{now.day}/{now.month}/{now.year}'
    timestamp = f'[{now.hour+1}:{now.minute}] [{date}]'
    line = f'{timestamp} {message}'

    # console and log
    print(line)
    with open('logs.txt', 'a') as handle:
        handle.write(line + '\n')

    # stop the program?
    if error:
        exit(error)


def get_fund_ids(portfolio):
    ''' Get the investments from the portfolio '''

    investments = []
    for company in portfolio:
        investments.append(company['fund_id'])

    return investments


def get_code_from_id(fund_id, companies):
    ''' Returns correct NZX code for company '''

    for company in companies:
        if company['id'] == fund_id:
            return company['code'] + '.NZ'

    return fund_id


def get_nz_time():
    ''' Returns NZ datetime object '''

    return datetime.utcnow() + timedelta(hours=12)


def dividends_soon(dividend_months):
    ''' Check if dividends are coming up '''

    for month in dividend_months.split(', '):
        if is_month_close(month.lower()):
            return True

    return False


def is_month_close(month):
    ''' Decide if the month is close to now '''

    month_number = datetime.strptime(month[:3], '%b').month
    current_month = get_nz_time().month

    has_month_passed = current_month >= (month_number - 1)
    is_close_enough = current_month <= (month_number + 1)

    if not has_month_passed and is_close_enough:
        return True

    return False
