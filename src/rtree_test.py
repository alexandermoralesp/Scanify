#sudo apt install python3-rtree
#http://toblerity.org/rtree/class.html

from rtree import index

p = index.Property()
p.dimension = 2 #D
p.buffering_capacity = 3 #M
p.dat_extension = 'data'
p.idx_extension = 'index'
idx = index.Index('2d_index',properties=p)

#insertar puntos
idx.insert(0, (4, 5))
idx.insert(1, (3, 4))
idx.insert(2, (5, 7))
idx.insert(3, (6, 3))
idx.insert(4, (4, 1))

#retornar elementos de la interseccion con el rectangulo 
q = (2, 3, 4, 7)
lres = [n for n in idx.intersection(q)] 
print("Elementos en la region: ", lres)

#retornar los k=1 vecinos de (1,2)
q = (1, 2)
lres = list(idx.nearest(coordinates=q, num_results=2))
print("El vecino mas cercano de (1,2): ", lres)



