import geopy.distance

go_by_coordonates = (44.77840710385228,-0.5548664427742672)
location = (0.114911,43.836722)

# print(geopy.distance.geodesic(go_by_coordonates, location).km)

point1 = (2.593594, 46.343012)
point2 = (2.596969, 46.342436)
print(geopy.distance.geodesic(point1, point2).km)


def get_every_n_value(list, n):
    result = []
    for i in range(0, len(list), n):
        result.append(list[i])
    return result

def remove_elements_before_in_list(list,element):
    if element in list:
        index = list.index(element)
        list = list[index+1:]
    return list



it1 = [[-0.458737, 46.322087], [-0.45928, 46.32229], [-0.459465, 46.322349], [-0.459751, 46.322441], [-0.45984, 46.322472], [-0.45992, 46.322499], [-0.460002, 46.322406], [-0.460186, 46.322189], [-0.460558, 46.321768], [-0.4607, 46.321607], [-0.460877, 46.321411], [-0.460975, 46.321322], [-0.461088, 46.321255], [-0.461109, 46.321275], [-0.461117, 46.321282], [-0.461172, 46.321308], [-0.461216, 46.321321], [-0.461269, 46.321331], [-0.461313, 46.321332]]
it2 = [[-0.458737, 46.322087], [-0.45928, 46.32229], [-0.459465, 46.322349], [-0.459751, 46.322441], [-0.45984, 46.322472], [-0.45992, 46.322499], [-0.460002, 46.322406], [-0.460186, 46.322189], [-0.460558, 46.321768], [-0.4607, 46.321607], [-0.460877, 46.321411], [-0.460975, 46.321322]]
it3 = [[-0.458737, 46.322087], [-0.45928, 46.32229], [-0.459465, 46.322349],[-0.459751, 46.322441], [-0.45984, 46.322472]]
its = []
its.append(it2)
its.append(it3)

def create_unique_route(routes, route):
    for existing_route in routes:
        existing_route = get_every_n_value(existing_route,1)
        index_point = 0
        same_route = True
        while same_route or index_point==len(existing_route)-1:
            same_route = False
            for point in route :
                if geopy.distance.geodesic(point, existing_route[index_point]).km<0.05:
                    same_route=True
                    print(point)
                    route = remove_elements_before_in_list(route,point)
            index_point = index_point+1
    return route

test = create_unique_route(its,it1)
print(test)