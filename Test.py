


def store_once_data(func):
    data_dict={}
    def inner(data,site):
        try:
            if data_dict[site]!=data:
                data_dict[site]=data
                func(data)
        except KeyError:
            data_dict[site]=data
            func(data)
        #data_dict.setdefault(site)
    return inner

print_difference= store_once_data(print)

        

