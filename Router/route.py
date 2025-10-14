import route_data, route_controller

def route(current, to):
    route_data.view_stack.append(current)
    # print(route_data.view_stack)
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
        print("no back available")