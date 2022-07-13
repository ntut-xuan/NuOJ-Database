import redis

def fliter_by_args(data_dict, args):
    if len(args) == 0:
        return list(data_dict.values())
    
    filter_list = []
    for key in data_dict.keys():
        data = data_dict[key]
        flag = True
        print(data)
        for arg_key in args.keys():
            if arg_key not in data.keys() or str(data[arg_key]) != str(args[arg_key]):
                flag = False
                continue
        if flag:
            filter_list.append(data)
    return filter_list

def test_database_connect():
    redis_db = redis.Redis(host='localhost', port=6379, decode_responses=True)
    redis_db.close()
    return True