def objToJson(name,path):
    with open(path+name.replace('"',"")+".obj","r") as file:
        vertex, faces = [], []
        for line in file:
            if line.startswith('v '):
                vertex.append([float(i) for i in line.split()[1:]] + [1])
            elif line.startswith('f'):
                faces_ = line.split()[1:]
                poly = []
                for face_ in faces_:
                    poly.append(int(face_.split("/")[0]))
                faces.append(poly)

    obj = name + ' : {'+'\n"vertexes" : \n\t'+str(vertex)+','+'\n"faces" : \n\t'+str(faces)+'\n}'
    return [{"vertexes":vertex,"faces":faces},obj]

path = "assets/item/car/"
name = '"NormalCar1"'
print(objToJson(name,path)[1]+",")