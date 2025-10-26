import Router.route_data as route_data

def route(current, to):
    route_data.view_stack.append(current)
    current.withdraw()  # Hide current window
    to.load()
    to.view()
    

def route_back(current):
    if len(route_data.view_stack) > 0:
        current.withdraw()
        to = route_data.view_stack.pop()
        to.deiconify()
        to.view()
    else:
        return